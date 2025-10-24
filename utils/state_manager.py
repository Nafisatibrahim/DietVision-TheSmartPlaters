"""
State management utilities for the DietVision app.
Includes functions to initialize and manage Streamlit session state.
"""

# Import libraries
import streamlit as st

# Define function to initialize session state
def init_session_state():
    # Initialize all required session variables if not already set.
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'meal_history' not in st.session_state:
        st.session_state.meal_history = []
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'last_prediction' not in st.session_state:
        st.session_state.last_prediction = None
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}