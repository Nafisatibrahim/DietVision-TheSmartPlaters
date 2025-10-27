"""
Backend module for interacting with the Gemini language model to generate chatbot responses.
"""

# Import libraries
import os
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GRPC_CPP_MIN_LOG_LEVEL"] = "3"

import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from a .env file
load_dotenv()
genai.configure(api_key=st.secrets["GENAI_API_KEY"] if "GENAI_API_KEY" in st.secrets else os.getenv("GENAI_API_KEY"))

# Define generation controls
generation_config = {
    "max_output_tokens": 1024,
    "temperature": 0.6,
    "top_p": 0.8,
    "top_k": 40
}

# Load Ella’s behavior manifesto from file
with open("Backend/Chatbot/ella_behavior.md", "r", encoding="utf-8") as f:
    ELLA_SYSTEM_PROMPT = f.read()

# Define the model to be used
model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    system_instruction=ELLA_SYSTEM_PROMPT,
    generation_config=generation_config
    )

# --- helpers ---
def _to_gemini_turn(msg):
    role = "user" if msg["role"] == "user" else "model"   # assistant → model
    return {"role": role, "parts": [msg["content"]]}

def _recent_history(messages, max_turns=8, max_chars=3500):
    hist = []
    total = 0
    for m in reversed(messages):
        if m["role"] not in ("user", "assistant"):
            continue
        s = m["content"]
        if total + len(s) > max_chars or len(hist) // 2 >= max_turns:
            break
        hist.append(_to_gemini_turn(m))
        total += len(s)
    return list(reversed(hist))

# create model once (you already do this) with system_instruction=ELLA_SYSTEM_PROMPT

def _get_chat():
    # Build (or reuse) a persistent Gemini chat object with recent history
    if "ella_chat" not in st.session_state:
        hist = _recent_history(st.session_state.get("messages", []))
        st.session_state.ella_chat = model.start_chat(history=hist)
    return st.session_state.ella_chat

def generate_response(prompt: str) -> str:
    try:
        chat = _get_chat()
        # send message on the persistent session so Gemini sees history
        resp = chat.send_message(
            prompt,
            generation_config={**generation_config, "max_output_tokens": 1024}
        )

        # extract text robustly
        try:
            if getattr(resp, "text", None):
                return resp.text.strip()
        except Exception:
            pass
        if getattr(resp, "candidates", None):
            for c in resp.candidates:
                if c.content and getattr(c.content, "parts", None):
                    parts = [getattr(p, "text", "") for p in c.content.parts if getattr(p, "text", None)]
                    if parts:
                        return " ".join(parts).strip()

        # auto-retry shorter if needed
        retry = chat.send_message("Please answer briefly (≤3 sentences). " + prompt,
                                  generation_config={**generation_config, "max_output_tokens": 1536})
        return (getattr(retry, "text", "") or "⚠️ I couldn’t generate a reply.").strip()

    except Exception as e:
        return f"⚠️ Error generating response: {e}"

def chatbot_ui(compact: bool = False):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    _ = _get_chat()  # ensure the chat session exists with recent history

    # render prior messages…
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    placeholder = "Ask Ella anything..." if compact else \
        "Ask Ella anything about nutrition, meals, or food choices..."

    if prompt := st.chat_input(placeholder, key=f"chat_input_{st.session_state.get('chat_context','default')}"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            reply = generate_response(prompt)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chatbot_ui()
