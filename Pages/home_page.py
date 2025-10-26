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
        full_name = user.get("name", "User")
        first_name = full_name.split(" ")[0] if full_name else "User"  # get only the first name

        st.markdown(f"### 👋 Hello, **{first_name}!**")
        
        with st.sidebar:
            st.markdown("---")
            st.markdown(f"### **{user.get('name', 'User')}**")

            if user.get("picture"):
                st.image(
                    user["picture"],
                    width=100,
                    caption="Logged in",
                    use_container_width=False,
                )
            st.markdown("---")

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
    st.markdown("""
    <div class="feature-container">
        <div class="feature-box">
            <h3>📸 Smart Food Recognition</h3>
            <p>Upload photos of your meals for instant nutritional analysis.</p>
        </div>
        <div class="feature-box">
            <h3>📊 Nutrition Dashboard</h3>
            <p>Track your calories, macros, and trends in one place.</p>
        </div>
        <div class="feature-box">
            <h3>🤖 Chat with Ella</h3>
            <p>Ask questions and get nutrition advice from your AI assistant.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Footer - Social Links
    with st.sidebar:
        st.markdown("---")
        st.markdown(
            """
            <div style="text-align: center; font-size: 0.9rem; line-height: 1.6;">
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


