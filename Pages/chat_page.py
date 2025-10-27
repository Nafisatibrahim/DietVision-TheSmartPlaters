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

    # Call the chatbot UI function to render the chat interface
    if user and isinstance(user, dict):
        st.markdown(f"### 👋 Hi, **{user.get('name', 'User')}!**")
        if user.get("picture"):
            st.image(user["picture"], width=100)
    else:
        st.warning("Please sign in to chat.")
        return
    
    # Show any last prediction if available
    pred = st.session_state.get("last_prediction")
    if pred:
        food = pred.get("food_name")
        conf = pred.get("confidence")
        st.markdown(f"**🍱 Last analyzed meal:** {food}  "
                    f"{f'· {conf:.2f}% confidence' if conf is not None else ''}")

        # (Optional) show only top-5 alternatives in an expander
        top5 = pred.get("top5")
        if top5:
            with st.expander("See top-5 alternatives"):
                for name, score in top5:
                    st.write(f"- {name} — {score*100:.1f}%")

    # Intro
    st.markdown("""
        <style>
        /* Normalize paragraph text */
        div.stMarkdown p {
            font-size: 16px !important;
            line-height: 1.6 !important;
            color: #2E2E2E !important;
        }
        </style>
        """, unsafe_allow_html=True)


    # Render the chatbot UI
    chatbot_ui(compact=False)


if __name__ == "__main__":
    show_chat_page(st.session_state.get("user", {}))
