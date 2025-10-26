"""
Utility functions for UI components.
"""

import streamlit as st
from Backend.Chatbot.chatbot import chatbot_ui


def floating_chat():
    """Renders a floating chat bubble that toggles Ella's chat window."""
    if "show_chat" not in st.session_state:
        st.session_state["show_chat"] = False

    # --- Floating button + popup CSS ---
    st.markdown("""
        <style>
        .chat-button {
            position: fixed;
            bottom: 25px;
            right: 25px;
            background-color: #FF6F00;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 28px;
            text-align: center;
            line-height: 60px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0,0,0,0.25);
            z-index: 100;
            transition: all 0.3s ease;
        }
        .chat-button:hover {
            background-color: #E65C00;
            transform: scale(1.05);
        }
        .chat-popup {
            position: fixed;
            bottom: 100px;
            right: 25px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 15px;
            width: 380px;
            max-height: 550px;
            overflow: hidden;
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            z-index: 99;
            animation: slideUp 0.3s ease;
        }
        @keyframes slideUp {
            from { transform: translateY(40px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Actual floating button ---
    # Use a unique key so it doesn’t conflict across pages
    if st.button("💬", key="floating_chat_button"):
        st.session_state["show_chat"] = not st.session_state["show_chat"]

    # Move button to bottom-right using CSS (Streamlit positions it inline by default)
    st.markdown("""
        <style>
        div[data-testid="stButton"][key="floating_chat_button"] {
            position: fixed;
            bottom: 25px;
            right: 25px;
            z-index: 100;
        }
        div[data-testid="stButton"][key="floating_chat_button"] > button {
            background-color: #FF6F00 !important;
            color: white !important;
            border: none !important;
            border-radius: 50% !important;
            width: 60px !important;
            height: 60px !important;
            font-size: 26px !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.25) !important;
        }
        div[data-testid="stButton"][key="floating_chat_button"] > button:hover {
            background-color: #E65C00 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Show chat popup when toggled ---
    if st.session_state["show_chat"]:
        st.session_state["chat_context"] = "floating"
        st.markdown('<div class="chat-popup">', unsafe_allow_html=True)
        chatbot_ui(compact=True) # compact mode for smaller popup
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.session_state["chat_context"] = "default"
