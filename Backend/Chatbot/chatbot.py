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
    "max_output_tokens": 512,
    "temperature": 0.6,
    "top_p": 0.8,
    "top_k": 40
}

# Define the model to be used
model = genai.GenerativeModel(
    model_name = "gemini-2.5-flash",
    generation_config=generation_config
    )

def generate_response(prompt):
    #Generate a response from the Gemini model based on the given prompt.
    try:
        system_prompt = (
            "You are DietVision.ai, a friendly and concise AI nutrition assistant. "
            "Reply in under 3 sentences unless the user explicitly asks for a longer explanation. "
            "Avoid lists or bullet points unless requested. "
            "Be warm, conversational, and direct."
        )
        # Combine style + user message into one prompt
        full_prompt = f"{system_prompt}\nUser: {prompt}"
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error generating response: {e}"
    
def chatbot_ui(compact: bool = False):
    """Displays Ella chat UI. Compact=True makes it fit smaller popups."""

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Adjust placeholder based on mode
    placeholder = (
        "Ask Ella anything..." if compact
        else "Ask Ella anything about nutrition, meals, or food choices..."
    )

    # User input (with unique key per context)
    if prompt := st.chat_input(
        placeholder,
        key=f"chat_input_{st.session_state.get('chat_context', 'default')}"
    ):
        # Append user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            response = generate_response(prompt)
            st.markdown(response)

        # Save assistant response
        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    chatbot_ui()
