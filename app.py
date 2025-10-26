"""
DietVision.ai - Main application
Handles dynamic page navigation
"""

# Import libraries
import streamlit as st
import requests
import os
from Backend.Users_profile.user import oauth2  # Import OAuth2Component
from utils.state_manager import init_session_state  # Import session state initializer
from utils.styling import apply_custom_styles     # Import custom styling function
from utils.ui_components import floating_chat  # Import floating chat component
from Pages import home_page, upload_analyze_page, chat_page
from Backend.Chatbot.chatbot import chatbot_ui  # Import chatbot UI
from dotenv import load_dotenv

load_dotenv()
# Automatically choose redirect URI based on environment
if os.getenv("LOCAL_DEV", "false").lower() == "true":
    redirect_uri = "http://localhost:8501"
else:
    redirect_uri = "https://diet-vision-smartplaters.streamlit.app"

# Define main entry point for DietVision.ai app
def main():
    init_session_state()
    apply_custom_styles()

    # Restore cached token if available
    if "auth_token_cached" in st.session_state and "token" not in st.session_state:
        st.session_state["token"] = st.session_state["auth_token_cached"]

    # Authentication: handles sign-in
    if "token" not in st.session_state:
        result = oauth2.authorize_button(
            "Sign in with Google",
            redirect_uri,
            "openid email profile",
            key="google_oauth_button"
        )

        # If authentication was successful, store token in session state
        if result and "token" in result:
            st.session_state.token = result.get("token")

            # Save the token locally in Streamlit's session
            st.session_state["auth_token_cached"] = st.session_state.token
            st.rerun()

        return

    # Retrieve access token
    token = st.session_state["token"]
    if not token:
        st.error("⚠️ Authentication failed. Please sign in again.")
        if "token" in st.session_state:
            del st.session_state["token"]
        st.rerun()
        return
    
    access_token = token.get("access_token") if isinstance(token, dict) else None
    if not access_token:
        st.error("⚠️ Invalid access token. Please sign in again.")
        del st.session_state["token"]
        st.rerun()
        return
    
    # Fetch user info from Google API using the access token
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    if resp.ok:
        st.session_state["user"] = resp.json()
    else:
        st.error("❌ Failed to fetch user info. Please sign in again.")
        del st.session_state["token"]
        st.rerun()
        return

    # Get logged user info
    user = st.session_state.get("user", {})
   
    # Add side bar navigation
    st.sidebar.title("🍽️ DietVision.ai")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigate",
        ["🏠 Home", "🍽️ Upload & Analyze", "📊 Dashboard", "🤖 Chat", "👤 Profile"],
        key="nav"
    )

    st.sidebar.markdown("---")
    st.sidebar.info("AI-powered nutrition assistant. Prototype version.")

    # Sign out button
    if st.sidebar.button("🚪 Sign Out"):
        for key in ["token", "auth_token_cached", "user"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Signed out successfully. Please sign in again.")
        st.rerun()

    # 🧩 Navigation: Page routing to corresponding functions
    if page == "🏠 Home":
        home_page.show_home_page(user)
    elif page == "🍽️ Upload & Analyze":
        upload_analyze_page.show_upload_analyze_page(user)
    elif page == "📊 Dashboard":
        st.info("Dashboard page coming soon...")
    elif page == "🤖 Chat":
        chat_page.show_chat_page(user)
    elif page == "👤 Profile":
        st.info("Profile page coming soon...")

    # Add bubble chat feature
    floating_chat()

# Run the app
if __name__ == "__main__":
    main()