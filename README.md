# DietVision-TheSmartPlaters
## Women in AI Canada Hackathon 2025
AI-powered nutrition assistant that detects food and recommends healthier alternatives.


Google authentication (OAuth2Component)
User info fetched from Google API
User data persisted locally in users.csv
Session management (sign in/out, refresh token)



"""def show_home_page(user):
    st.title("🏠 Home")
    st.write(f"Welcome, {user.get('name')}!")
    st.write("This is the home page of DietVision.ai. Use the sidebar to navigate through the app.")
    st.write("Feel free to explore the features we offer to help you with your nutrition and healthy habits.")
    st.write("Stay tuned for more updates and features coming soon!")   
    st.write("Here are some quick links to get you started:")
    st.markdown("- [🍽️ Upload & Analyze](#) - Upload your meals and get nutritional analysis."
                "\n- [📊 Dashboard](#) - View your nutrition dashboard and track your progress."
                "\n- [🤖 Chat with Ella](#) - Get personalized nutrition advice from our AI assistant."
                "\n- [👤 Profile](#) - View and edit your profile information.")
    

    st.info("Tip: Use the sidebar to navigate between pages.")
    
"""

Step 3: Next Upgrade Options

Once the base chatbot works, we can add:

🔗 Context awareness (e.g., user’s last meal analysis, health goals)

💾 User profiles (store chats or preferences in a JSON/DB)

🧠 Specialized prompts (“explain macros”, “suggest a breakfast plan”)

🧑‍🎤 Custom UI (avatar, header, toggle between chatbot and analysis view)


prompt = f"User just analyzed a plate with {detected_food}. Give short feedback and healthy alternatives."
generate_response(prompt)

<div class="chat-button" onclick="window.parent.postMessage('toggle_chat', '*')">
    <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="32"/>
</div>

background-color: #4CAF50;
