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
import pandas as pd

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

# Helpers function
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

# Create model chat session
def _get_chat():
    """Start or reuse Ella's persistent chat with personalized context."""
    if "ella_chat" not in st.session_state:
        # Get recent chat history
        hist = _recent_history(st.session_state.get("messages", []))

        # Get user context (profile + preferences + last meal)
        context_turn = _user_context_turn()

        # Merge the user context into Ella's system prompt
        personalized_instruction = (
            f"{ELLA_SYSTEM_PROMPT}\n\n"
            f"---\n"
            f"Below is the user's current profile context. Use this information "
            f"to personalize your nutrition advice naturally, as if you already know them.\n"
            f"Never repeat this data back unless relevant to the user’s question.\n\n"
            f"{context_turn['parts'][0]}"
        )

        # Create a new personalized model for this user session
        personalized_model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=personalized_instruction,
            generation_config=generation_config
        )

        # Start chat with user-specific context
        st.session_state.ella_chat = personalized_model.start_chat(history=hist)

    return st.session_state.ella_chat


# Build user context
def _user_context_turn():
    """Create a structured summary of the current user's profile, preferences, and last meal."""
    user_info = st.session_state.get("user_info", {})
    prefs = st.session_state.get("user_preferences", {})
    meal = st.session_state.get("last_prediction", {})

    context_parts = []

    # Basic identity
    name = user_info.get("name") or "User"
    context_parts.append(f"User name: {name}")

    # Demographics
    if prefs.get("age"):
        context_parts.append(f"Age: {prefs['age']}")
    if prefs.get("sex"):
        context_parts.append(f"Sex: {prefs['sex']}")
    if prefs.get("country"):
        context_parts.append(f"Country: {prefs['country']}")

    # Health and diet
    if prefs.get("health_conditions"):
        context_parts.append("Health conditions: " + ", ".join(prefs["health_conditions"]))
    if prefs.get("dietary_preferences"):
        context_parts.append("Dietary preferences: " + ", ".join(prefs["dietary_preferences"]))
    if prefs.get("goals"):
        context_parts.append("Goals: " + ", ".join(prefs["goals"]))

    # Last analyzed meal
    if meal:
        context_parts.append(
            f"Last analyzed meal: {meal.get('food_name', 'unknown')} "
            f"({meal.get('confidence', 0)}% confidence)"
        )

    # Build final text
    context_text = " | ".join(context_parts)
    return {"role": "user", "parts": [f"SESSION CONTEXT: {context_text}"]}

# Fetch food nutrient info
def get_food_info(food_name: str):
    """Fetch nutrient info for a specific food from the loaded database."""
    if "nutrient_database" not in st.session_state:
        return None

    df = st.session_state["nutrient_database"]
    match = df[df["Food Class"].str.lower() == food_name.lower()]
    return match.iloc[0].to_dict() if not match.empty else None

def generate_response(prompt: str) -> str:
    try:
        # Check if the question matches a food in the database
        import re
        match = re.search(r"(?:what(?:'s| is)?|how much).*?\b(in|of)\b\s+([a-zA-Z_ ]+)", prompt.lower())
        if match:
            food_name = match.group(2).strip()
            food_info = get_food_info(food_name)
            if food_info:
                return (
                    f"🍽️ **{food_info['Food Class'].replace('_',' ').title()} (per {food_info['Portion Size']})**\n\n"
                    f"- Calories: {food_info['Calories']} kcal\n"
                    f"- Protein: {food_info['Protein']} g\n"
                    f"- Fat: {food_info['Fat']} g\n"
                    f"- Carbs: {food_info['Carbs']} g\n"
                    f"- Fiber: {food_info['Fiber']} g\n"
                    f"- Sugar: {food_info['Sugar']} g\n"
                    f"- Tags: {food_info['Tags']}"
                )

        # Fallback to Gemini reasoning if no match
        chat = _get_chat()
        resp = chat.send_message(
            prompt,
            generation_config={**generation_config, "max_output_tokens": 1024}
        )

        # Extract text safely
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

        # Auto-retry shorter if needed
        retry = chat.send_message("Please answer briefly (≤3 sentences). " + prompt,
                                  generation_config={**generation_config, "max_output_tokens": 1536})
        return (getattr(retry, "text", "") or "⚠️ I couldn’t generate a reply.").strip()

    except Exception as e:
        return f"⚠️ Error generating response: {e}"


def chatbot_ui(compact: bool = False):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    _ = _get_chat()  # ensure the chat session exists with recent history

    if "chat_context" not in st.session_state:
        st.session_state.chat_context = st.session_state.get("nav", "main")

    # render prior messages…
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    placeholder = "Ask Ella anything..." if compact else \
        "Ask Ella anything about nutrition, meals, or food choices..."

    unique_chat_key = f"chat_input_{st.session_state.get('chat_context', 'default')}_{st.session_state.get('nav', 'main')}"
    if prompt := st.chat_input(placeholder, key=unique_chat_key):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            reply = generate_response(prompt)
            st.markdown(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chatbot_ui()
