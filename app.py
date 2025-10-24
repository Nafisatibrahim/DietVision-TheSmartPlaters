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
from Pages import home_page, upload_analyze_page
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

    # Authentication: handles sign-in
    if "token" not in st.session_state:
        result = oauth2.authorize_button(
            "Sign in with Google",
            redirect_uri,
            "openid email profile",
            key="google_oauth_button"
        )

        if result and "token" in result:
            st.session_state.token = result.get("token")
            st.rerun()
        return

    # Retrieve access token
    token = st.session_state["token"]
    access_token = token.get("access_token") if isinstance(token, dict) else None

    if not access_token:
        st.error("⚠️ Authentication failed. Please sign in again.")
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

    # Get logged user ingo
    user = st.session_state.get("user")
   
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

    # 🧩 Navigation: Page routing to corresponding functions
    if page == "🏠 Home":
        home_page.show_home_page(user)
    elif page == "🍽️ Upload & Analyze":
        upload_analyze_page.show_upload_analyze_page(user)
    elif page == "📊 Dashboard":
        st.info("Dashboard page coming soon...")
    elif page == "🤖 Chat":
        st.info("Chat page coming soon...")
    elif page == "👤 Profile":
        st.info("Profile page coming soon...")
    

if __name__ == "__main__":
    main()