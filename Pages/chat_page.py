"""
Chat Page
Display the chat interface for interacting with the AI nutrition assistant.
"""

# Import libraries
import pandas as pd
import streamlit as st
from Backend.Chatbot.chatbot import chatbot_ui  # Import chatbot UI

st.write(st.session_state.get("last_prediction"))

# Display the chat interface
def show_chat_page(user):
    st.title("🤖 Chat with Ella – Your AI Nutrition Assistant")
    st.sidebar.title("🍽️ DietVision.ai Chat")

    # Call the chatbot UI function to render the chat interface
    if user and isinstance(user, dict):
        st.markdown(f"### 👋 Hi, **{user.get('name', 'User')}!**")
        if user.get("picture"):
            st.image(user["picture"], width=100)
    else:
        st.warning("Please sign in to chat.")
        return
    
    # Show any last prediction if available
    if "last_prediction" in st.session_state:
        st.write(f"🍱 Last analyzed meal: **{st.session_state['last_prediction']}**")

    # Intro
    st.markdown("""
        Welcome to **Ella**, your friendly AI-powered nutrition assistant.  
        Ask questions about meals, ingredients, healthier substitutions, or balanced eating tips.  
        Ella will analyze your request and give personalized, evidence-based advice. 🌿
        ---
    """)

    # Render the chatbot UI
    chatbot_ui(compact=False)


if __name__ == "__main__":
    show_chat_page()
