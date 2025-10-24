"""
User authentication and profile management using Google OAuth2 in Streamlit.
Enables users to sign in with Google, fetches their profile information,
"""
import streamlit as st
from streamlit_oauth import OAuth2Component
from httpx_oauth.oauth2 import BaseOAuth2
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

# Create a custom OAuth2 client
class GoogleOAuth2(BaseOAuth2):
    def __init__(self, client_id, client_secret, authorize_url, token_url, revoke_url):
        super().__init__(
            client_id=client_id,
            client_secret=client_secret,
            authorize_endpoint=authorize_url,
            access_token_endpoint=token_url,  
            revoke_token_endpoint=revoke_url,
            revoke_token_auth_method="client_secret_post",  
        )

# Instantiate custom client
custom_oauth_client = GoogleOAuth2(
    CLIENT_ID,
    CLIENT_SECRET,
    AUTHORIZE_URL,
    TOKEN_URL,
    REVOKE_TOKEN_URL
)

# Pass that custom client to OAuth2Component
oauth2 = OAuth2Component(oauth_client=custom_oauth_client)
