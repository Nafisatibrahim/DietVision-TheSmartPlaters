"""
Utility functions for UI components.
"""

import streamlit as st
from Backend.Chatbot.chatbot import chatbot_ui


def floating_chat():
    """Adds a chat button at the bottom of the sidebar that opens Ella's chat window on the main page."""
    if "show_chat" not in st.session_state:
        st.session_state["show_chat"] = False

    # --- Sidebar button at the bottom ---
    with st.sidebar:
        st.markdown("<br><br><br><br><br><br><br>", unsafe_allow_html=True)  # spacing
        st.markdown("---")
        st.markdown("<div style='text-align:center;'>", unsafe_allow_html=True)
        if st.button("💬 Chat with Ella", key="sidebar_chat_button"):
            st.session_state["show_chat"] = not st.session_state["show_chat"]
        st.markdown("</div>", unsafe_allow_html=True)

    # --- If toggled, show popup on main page ---
    if st.session_state["show_chat"]:
        st.markdown(
            """
            <style>
            .chat-popup {
                position: fixed;
                bottom: 90px;
                right: 40px;
                background: #ffffff;
                border: 1px solid #ddd;
                border-radius: 15px;
                width: 400px;
                max-height: 550px;
                overflow: hidden;
                box-shadow: 0 8px 16px rgba(0,0,0,0.3);
                z-index: 9999;
                animation: fadeInUp 0.3s ease;
            }
            @keyframes fadeInUp {
                from { opacity: 0; transform: translateY(20px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .chat-close {
                text-align: right;
                padding: 6px 10px 0 0;
                font-size: 18px;
                cursor: pointer;
                color: #FF6F00;
                font-weight: bold;
            }
            .chat-close:hover {
                color: #E65C00;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="chat-popup">', unsafe_allow_html=True)
        st.markdown('<div class="chat-close" onclick="window.parent.postMessage({type:\'close_chat\'}, \'*\')">✖</div>', unsafe_allow_html=True)
        chatbot_ui()
        st.markdown('</div>', unsafe_allow_html=True)

        # Add JS listener to close chat
        from streamlit_javascript import st_javascript
        event = st_javascript("""
            await new Promise(resolve => {
                window.addEventListener("message", e => {
                    if (e.data?.type === "close_chat") resolve("close_chat");
                }, {once: true});
            });
        """)
        if event == "close_chat":
            st.session_state["show_chat"] = False
