"""
User authentication and profile management using Google OAuth2 in Streamlit.
Enables users to sign in with Google, fetches their profile information,
"""
import streamlit as st
from streamlit_oauth import OAuth2Component
from dotenv import load_dotenv
import os
import requests
from .save_profile import save_user_profile

# Load environment variables
load_dotenv(dotenv_path="./.env") # load .env from project root

# Google OAuth2 endpoints
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

# Credentials
CLIENT_ID = st.secrets["CLIENT_ID"] if "CLIENT_ID" in st.secrets else os.getenv("CLIENT_ID")
CLIENT_SECRET = st.secrets["CLIENT_SECRET"] if "CLIENT_SECRET" in st.secrets else os.getenv("CLIENT_SECRET")
REDIRECT_URI = (
     "https://diet-vision-smartplaters.streamlit.app"
     if not os.getenv("LOCAL_DEV")
     else "http://localhost:8501"
 )
SCOPE = "openid email profile"

# Create OAuth2Component instance
oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    REFRESH_TOKEN_URL,
    REVOKE_TOKEN_URL
)

# Use for debugging purposes
"""# Load environment variables
load_dotenv(dotenv_path="../../.env")

# Google OAuth2 endpoints
AUTHORIZE_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_TOKEN_URL = "https://oauth2.googleapis.com/token"
REVOKE_TOKEN_URL = "https://oauth2.googleapis.com/revoke"

# Credentials
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8501"
SCOPE = "openid email profile"

# Create OAuth2Component instance
oauth2 = OAuth2Component(
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    REFRESH_TOKEN_URL,
    REVOKE_TOKEN_URL
)

st.title("DietVision.ai User Profile — Sign in with Google")

# Use Streamlit session state to persist the token
if "token" not in st.session_state:
    result = oauth2.authorize_button("Sign in with Google", REDIRECT_URI, SCOPE)
    if result and "token" in result:
        st.session_state.token = result.get("token")
        st.rerun()
else:
    token = st.session_state["token"]
    st.success("You’re signed in! 🎉")
    # st.json(token)

    # Extract access token
    access_token = token.get("access_token") if isinstance(token, dict) else None

    if access_token:
        # Fetch user info from Google API using the access token
        resp = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=10,
        )
        if resp.ok:
            user_info = resp.json()
            st.image(user_info.get("picture"), width=100)
            st.write("👤 Name:", user_info.get("name"))
            st.write("📧 Email:", user_info.get("email"))
            st.session_state["user"] = user_info

            # Save to CSV
            save_user_profile(user_info)
            st.success("Profile saved successfully!")
        else:
            st.error("❌ Failed to fetch user info: " + resp.text)
    else:
        st.error("⚠️ No access token found. Please log in again.")
        del st.session_state["token"]
        st.rerun()

    # Add a refresh button and logout button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Token"):
            new_token = oauth2.refresh_token(token)
            if new_token:
                st.session_state.token = new_token
                st.rerun()
            else:
                st.error("Failed to refresh token.")

    with col2:
        if st.button("🚪 Logout"):
            oauth2.revoke_token(token)
            del st.session_state["token"]
            st.rerun()
"""