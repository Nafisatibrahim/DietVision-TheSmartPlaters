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