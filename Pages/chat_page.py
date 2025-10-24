"""

"""

# Import libraries
import pandas as pd
import streamlit as st

# Define function to display chatbot
def show_chat_page(user):
    st.title("🤖 Chat with Ella")
    st.write(f"Hello, {user.get('name')}! How can I assist you with your nutrition today?")
    st.write("This is where you can chat with Ella, your personal AI nutrition assistant.")
    st.write("Feel free to ask questions about healthy eating, meal suggestions, or any nutrition-related topics.")
    st.write("Ella is here to help you make informed dietary choices and support your wellness journey.")
    st.markdown("### 💬 Start a conversation with Ella!")
    st.text_area("Type your message here...", height=150)
    st.markdown("---")
    st.info("Note: Ella is an AI assistant and not a substitute for professional medical advice.")
    st.markdown("Use the sidebar to navigate to other sections of the app.")

    message = st.text_input("Ask Ella something:")
    if st.button("Send"):
        st.success(f"Ella says: That's a great question, {user.get('name')}! 🌟 (Mock reply)")