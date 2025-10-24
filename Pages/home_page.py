"""
Home Page
Display a welcome message and brief overview of the app features.
"""

# Import libraries
import streamlit as st

# Define function to show home page
def show_home_page(user): 
    # Render home page content
    st.title("🍽️ Welcome to DietVision.ai!")

    # Greeting
    if user and isinstance(user, dict):
        st.markdown(f"### 👋 Hello, **{user.get('name', 'User')}!**")
        if user.get("picture"):
            st.image(user["picture"], width=100)
    else:
        st.warning("Please sign in to access all features.")
        return  # stop rendering below if user is missing

    # Intro text
    st.markdown("""
    <div class="custom-card">
        <h3 style="color:#FF6F00;">🥬🥕🍅🥦 Your AI-Powered Nutrition Assistant</h3>
        <p style="font-size:1.1rem;">
        DietVision.ai helps you understand your meals with AI-powered food recognition,
        personalized insights, and smart nutrition tracking. Discover what's in your food with the power of artificial intelligence. 
        Upload photos, get nutritional insights, and chat with Ella, your personal nutrition assistant! 
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feature summary cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="custom-card">
            <h4>📸 Smart Food Recognition</h4>
            <p>Upload photos of your meals for instant nutritional analysis.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="custom-card">
            <h4>📊 Nutrition Dashboard</h4>
            <p>Track your calories, macros, and trends in one place.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="custom-card">
            <h4>🤖 Chat with Ella</h4>
            <p>Ask questions and get nutrition advice from your AI assistant.</p>
        </div>
        """, unsafe_allow_html=True)

