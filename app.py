import streamlit as st
from Chatbot.backend import generate_response

# Page setup
st.set_page_config(page_title="DietVAision.ai Chatbot", page_icon="🥗")

# App title
st.title("🥗 DietVision.ai Chatbot")
st.write("Your personal AI nutrition assistant — powered by Gemini!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display past messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me about nutrition, meal plans, or healthy habits! Type your question here...")

if user_input:
    # Display user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get Gemini reply from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            ai_reply = generate_response(user_input)
            st.markdown(ai_reply, unsafe_allow_html=True)

    # Save AI reply to history
    st.session_state["messages"].append({"role": "assistant", "content": ai_reply})