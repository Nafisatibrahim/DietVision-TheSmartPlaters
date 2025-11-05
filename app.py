"""
DietVision.ai - Main application
Handles dynamic page navigation
"""

# Import libraries
import streamlit as st
import pandas as pd
import requests
import os
import json
from Backend.Users_profile.user import oauth2  # Import OAuth2Component
from utils.state_manager import init_session_state  # Import session state initializer
from utils.styling import apply_custom_styles     # Import custom styling function
from utils.ui_components import floating_chat  # Import floating chat component
from Pages import home_page, upload_analyze_page, chat_page, profile_page
from Backend.Chatbot.chatbot import chatbot_ui  # Import chatbot UI
from Backend.Users_profile.save_profile import save_user_profile, load_user_profile
from Backend.Users_profile.save_preferences import save_user_preferences, load_user_preferences

from dotenv import load_dotenv

# Load nutrient database into session state
@st.cache_data
def load_nutrient_database():
    return pd.read_csv("Datasets/Nutrient_Database.csv")

# Load user profile and preferences
@st.cache_data
def load_user_data(email):
    try:
        profile = load_user_profile(email)
        prefs = load_user_preferences(email)
        return profile, prefs
    except Exception as e:
        st.warning(f"⚠️ Could not load user data: {e}")
        return None, None

load_dotenv()
# Automatically choose redirect URI based on environment
if os.getenv("LOCAL_DEV", "false").lower() == "true":
    redirect_uri = "http://localhost:8501"
else:
    redirect_uri = "https://diet-vision-smartplaters.streamlit.app"

# Define main entry point for DietVision.ai app
def main():
    # Initialize session state and apply custom styles
    init_session_state()
    apply_custom_styles()

    # Load nutrient database into session state if not already loaded
    if "nutrient_database" not in st.session_state:
        st.session_state["nutrient_database"] = load_nutrient_database()

    # Restore cached token if available
    if "auth_token_cached" in st.session_state and "token" not in st.session_state:
        st.session_state["token"] = st.session_state["auth_token_cached"]
    
    # Try loading cached token from file (persists after refresh)
    if "token" not in st.session_state and os.path.exists("token_cache.json"):
        try:
            with open("token_cache.json", "r") as f:
                cached = json.load(f)
            st.session_state["token"] = cached
        except Exception:
            pass

    # Add intro before authentication
        if "token" not in st.session_state:
            st.markdown("""
                <div style="background-color:#FF6F00;padding:10px;border-radius:10px;margin-bottom:20px;">
                    <h2 style="color:white;">🍽️ Welcome to DietVision.ai!</h2>
                    <p style="color:white;font-size:1.1rem;">
                        Your AI-powered nutrition assistant. Upload meal photos, get instant nutritional analysis, 
                        and chat with Ella for personalized diet advice! 💬
                    </p> 
                </div>
            """, unsafe_allow_html=True)

            st.markdown("Please sign in with your Google account to continue.")

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

            # Save token to local file (so it persists after refresh)
            with open("token_cache.json", "w") as f:
                json.dump(st.session_state.token, f)

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
        user_info = st.session_state["user"]

        # Save or update user profile in Google Sheets
        if "user_saved" not in st.session_state:
            try:
                save_user_profile({
                    "name": user_info.get("name", ""),
                    "email": user_info.get("email", ""),
                    "picture": user_info.get("picture", "")
                })
                st.session_state["user_saved"] = True  # mark as saved
            except Exception as e:
                st.warning(f"⚠️ Unable to sync with Google Sheets. Error: {e}")

    # 🔄 Load user profile and preferences after login
    email = user_info.get("email", "")
    if email:
        profile, prefs = load_user_data(email)

        if profile:
            st.session_state["user_info"] = profile
        if prefs:
            st.session_state["user_preferences"] = prefs
            st.session_state["user_profile"] = prefs  # alias for profile_page

        if (profile or prefs) and "profile_restored" not in st.session_state:
            st.toast("✅ Welcome back! Your profile has been restored.", icon="🌿")
            st.session_state["profile_restored"] = True

                
    else:
        # Handle failed user info fetch
        st.warning("🔒 Session expired. Please sign in again.")
        for key in ["token", "auth_token_cached", "user"]:
            st.session_state.pop(key, None)
        if os.path.exists("token_cache.json"):
            os.remove("token_cache.json")
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
        profile_page.show_profile_page(user)

    # Add bubble chat feature
    floating_chat()

    # Sign out button
    if st.sidebar.button("🚪 Sign Out"):
        for key in ["token", "auth_token_cached", "user"]:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Signed out successfully. Please sign in again.")
        st.rerun()

    # Sidebar Footer - Social Links
    with st.sidebar:
        st.sidebar.markdown(
            """
            <div class="sidebar-footer">
                Created with ❤️ by <strong>Nafisat Ibrahim</strong><br><br>
                <a href="https://www.linkedin.com/in/nafisatibrahim/" target="_blank" style="text-decoration: none; margin: 0 6px;">
                    <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/linkedin.svg" width="18" style="vertical-align: middle;"/> 
                    <span style="color:#0077b5;">LinkedIn</span>
                </a><br>
                <a href="https://github.com/Nafisatibrahim" target="_blank" style="text-decoration: none; margin: 0 6px;">
                    <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/github.svg" width="18" style="vertical-align: middle;"/> 
                    <span style="color:#333;">GitHub</span>
                </a><br>
                <a href="https://medium.com/@nafisatibrahim" target="_blank" style="text-decoration: none; margin: 0 6px;">
                    <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/medium.svg" width="18" style="vertical-align: middle;"/> 
                    <span style="color:#000;">Medium</span>
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# Run the app
if __name__ == "__main__":
    main()