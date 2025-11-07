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

    # Demo Video Section
    st.markdown("---")
    st.markdown("""
    <div class="demo-section">
        <h3>🎥 Watch the Demo</h3>
        <p style="color: #555; margin-bottom: 1rem;">See DietVision.ai in action! Watch how easy it is to track your nutrition.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Video player
    demo_video_path = "Assets/dietvision-demo-video.mp4"
    
    try:
        video_file = open(demo_video_path, 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        video_file.close()
    except FileNotFoundError:
        st.info("📹 Demo video coming soon! Upload your demo_video.mp4 to the attached_assets folder.")
    
    # How to Use Instructions
    st.markdown("---")
    st.markdown("""
    <div class="instructions-card">
        <h3>📖 How to Use DietVision.ai</h3>
        <div class="instruction-step">
            <strong>Step 1: Upload Your Food 📸</strong><br>
            Go to the "Upload & Analyze" page and upload a photo of your meal. You can also use the camera button to take a picture directly!
        </div>
        <div class="instruction-step">
            <strong>Step 2: Get AI Analysis 🤖</strong><br>
            Click "Analyze Food" and our AI will identify your meal and provide detailed nutritional information including calories, protein, carbs, and more.
        </div>
        <div class="instruction-step">
            <strong>Step 3: Log Your Meals 📝</strong><br>
            Save your analyzed meals to track your nutrition over time. All your meals will be stored in your personal dashboard.
        </div>
        <div class="instruction-step">
            <strong>Step 4: View Your Dashboard 📊</strong><br>
            Check your nutrition dashboard to see your daily, weekly, and monthly progress with interactive charts and statistics.
        </div>
        <div class="instruction-step">
            <strong>Step 5: Chat with Ella 💬</strong><br>
            Ask Ella, your AI nutrition assistant, any questions about your diet, meal planning, or nutrition advice!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Social Links Section
    st.markdown("---")
    st.markdown("### 🔗 Connect With Me")
    st.markdown("""
    <div class="social-links-container">
        <a href="https://www.linkedin.com/in/nafisatibrahim" target="_blank" class="social-link">
            💼 LinkedIn
        </a>
        <a href="https://github.com/Nafisatibrahim" target="_blank" class="social-link">
            💻 GitHub
        </a>
        <a href="https://medium.com/@nafisat.ibrahim" target="_blank" class="social-link">
            ✍️ Medium
        </a>
        <a href="YOUR_POWERPOINT_URL" target="_blank" class="social-link">
            📊 PowerPoint Slides
        </a>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; color: #666; margin-top: 1rem; font-size: 0.9rem;">
        Built with ❤️ • Feel free to connect and share feedback!
    </p>
    """, unsafe_allow_html=True)