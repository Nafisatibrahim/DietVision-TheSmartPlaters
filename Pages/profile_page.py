"""
Profile Page
Display user's information and account details.
"""

import streamlit as st
import base64
from datetime import datetime
from Backend.Users_profile.save_profile import save_user_profile, load_user_profile
from Backend.Users_profile.save_preferences import save_user_preferences, load_user_preferences

def show_profile_page(user):
    st.title("👤 Your Profile")

    # Check if user is signed in
    if not user or not isinstance(user, dict):
        st.warning("⚠️ Please sign in to view your profile.")
        return

    # Get user info from session
    st.session_state["user_info"] = user

    # User info
    full_name = user.get("name", "Unknown User")
    email = user.get("email", "No email available")
    picture = user.get("picture", None)

    # Store editable info in session_state if not already there
    if "editable_name" not in st.session_state:
        st.session_state.editable_name = full_name
    if "editable_bio" not in st.session_state:
        st.session_state.editable_bio = "Nutrition enthusiast exploring smarter eating habits 🌱"
    if "uploaded_profile_pic" not in st.session_state:
        st.session_state.uploaded_profile_pic = picture
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {}

    # Load existing profile from Google Sheets on first page visit
    if 'profile_loaded' not in st.session_state:
        st.session_state.profile_loaded = True
        
        saved_prefs = load_user_preferences(email)
        if saved_prefs:
            st.session_state.user_profile = saved_prefs
            st.info("✅ Loaded your profile from Google Sheets!")

    # Profile Header
    st.markdown("""
        <div style="
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
            text-align: center;
        ">
            <h2 style="color:#2E7D32;">🌿 Welcome back!</h2>
            <p style="font-size:1.1rem; color:#555;">Here's your account information.</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Profile Card
    col1, col2 = st.columns([1, 2], gap="medium") 
    with col1:
        # Display profile picture
        if st.session_state.uploaded_profile_pic:
            st.image(st.session_state.uploaded_profile_pic, width=150)
        else:
            st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=150)

        # Allow uploading new picture
        uploaded_file = st.file_uploader("Upload new profile picture", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

        if uploaded_file:
            # Convert to base64 (or save locally)
            img_bytes = uploaded_file.read()
            base64_img = "data:image/png;base64," + base64.b64encode(img_bytes).decode()
            st.session_state.uploaded_profile_pic = base64_img
            st.success("✅ Profile picture updated successfully!")

    with col2:
        st.markdown("### ✏️ Edit Information")
        st.session_state.editable_name = st.text_input("Full Name", st.session_state.editable_name)
        st.session_state.editable_bio = st.text_area("Bio", st.session_state.editable_bio, height=100)
        st.text_input("Email", email, disabled=True)

        if st.button("💾 Save Changes", key="save_changes"):
            st.success("✅ Profile updated successfully!")
            user["name"] = st.session_state.editable_name
            user["bio"] = st.session_state.editable_bio
            user["picture"] = st.session_state.uploaded_profile_pic

            # Save to Google Sheets with proper error handling
            success, message = save_user_profile(user)
            if success:
                st.success("✅ Profile updated successfully!")
                st.info(message)
            else:
                st.error(f"❌ Save failed: {message}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ------------------ 🧍 Personal, Dietary, and Health Information ------------------
    st.markdown("## 🌱 Health & Nutrition Preferences")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("🎂 Age", min_value=1, max_value=120, 
                             value=st.session_state.user_profile.get('age', 25))
        
        sex = st.selectbox("⚧ Sex", ["Male", "Female", "Other", "Prefer not to say"],
                          index=0 if 'sex' not in st.session_state.user_profile else 
                          ["Male", "Female", "Other", "Prefer not to say"].index(
                              st.session_state.user_profile['sex']))
        
        country = st.selectbox("🌍 Country", 
                              ["United States", "Canada", "United Kingdom", "Australia", "India", "Other"],
                              index=0 if 'country' not in st.session_state.user_profile else 
                              ["United States", "Canada", "United Kingdom", "Australia", "India", "Other"].index(
                                  st.session_state.user_profile.get('country', 'United States')))
    
    with col2:
        ethnicity = st.selectbox("🌎 Race/Ethnicity", 
                                ["Asian", "Black/African American", "Hispanic/Latino", "White/Caucasian", 
                                 "Native American", "Pacific Islander", "Mixed", "Other", "Prefer not to say"],
                                index=0 if 'ethnicity' not in st.session_state.user_profile else 
                                ["Asian", "Black/African American", "Hispanic/Latino", "White/Caucasian", 
                                 "Native American", "Pacific Islander", "Mixed", "Other", "Prefer not to say"].index(
                                     st.session_state.user_profile.get('ethnicity', 'Asian')))
        
        cuisine = st.multiselect("🍜 Preferred Cuisines", 
                                ["American", "Italian", "Chinese", "Indian", "Mexican", "Japanese", 
                                 "Mediterranean", "Thai", "French", "Korean", "Other"],
                                default=st.session_state.user_profile.get('cuisine', []))
        
        activity_level = st.selectbox("🏃‍♀️ Activity Level",
                                     ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"],
                                     index=0 if 'activity_level' not in st.session_state.user_profile else 
                                     ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"].index(
                                         st.session_state.user_profile.get('activity_level', 'Moderately Active')))
    
    # Health conditions
    st.markdown("### 🏥 Health Information")
    health_conditions = st.multiselect("Health Conditions (Optional)",
                                      ["Diabetes", "High Cholesterol", "High Blood Pressure", "Heart Disease",
                                       "Food Allergies", "Celiac Disease", "Lactose Intolerance", "Other", "None"],
                                      default=st.session_state.user_profile.get('health_conditions', []))
    
    # Goals
    st.markdown("### 🎯 Nutrition Goals")
    goals = st.multiselect("What are your goals?",
                          ["Weight Loss", "Weight Gain", "Muscle Building", "General Health", 
                           "Heart Health", "Diabetes Management", "Athletic Performance", "Other"],
                          default=st.session_state.user_profile.get('goals', []))
    
    # Dietary preferences
    dietary_preferences = st.multiselect("🥗 Dietary Preferences",
                                        ["Vegetarian", "Vegan", "Keto", "Paleo", "Low-Carb", 
                                         "Mediterranean", "Gluten-Free", "Dairy-Free", "None"],
                                        default=st.session_state.user_profile.get('dietary_preferences', []))
    
    # Save profile
    if st.button("💾 Save Profile", key="save_profile"):
        st.session_state.user_profile = {
            "age": age,
            "sex": sex,
            "country": country,
            "ethnicity": ethnicity,
            "cuisine": cuisine,
            "activity_level": activity_level,
            "health_conditions": health_conditions,
            "goals": goals,
            "dietary_preferences": dietary_preferences,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with st.spinner("Saving to Google Sheets..."):
            # Save with proper error handling
            profile_success, profile_msg = save_user_profile(user)
            prefs_success, prefs_msg = save_user_preferences(
                email=email,
                preferences=st.session_state.user_profile
            )

            # Only show success if BOTH operations succeeded
            if profile_success and prefs_success:
                st.success("✅ Profile and preferences saved!")
                st.info(f"📊 {profile_msg}")
                st.info(f"💚 {prefs_msg}")
            else:
                # Show specific errors
                if not profile_success:
                    st.error(f"❌ Profile save failed: {profile_msg}")
                else:
                    st.info(f"✅ {profile_msg}")
                    
                if not prefs_success:
                    st.error(f"❌ Preferences save failed: {prefs_msg}")
                else:
                    st.info(f"✅ {prefs_msg}")


        # Make the new data visible to the chatbot
        st.session_state["user_info"] = user # OAuth user details
        st.session_state["user_preferences"] = st.session_state.user_profile

        # Reset Ella’s chat so the next message includes updated context
        st.session_state.pop("ella_chat", None)

    # Display current profile
    if st.session_state.user_profile:
        st.markdown("### 👤 Current Profile Summary")
        profile = st.session_state.user_profile
        
        st.markdown(f"""
        <div class="custom-card">
            <p><strong>Age:</strong> {profile.get('age', 'Not set')}</p>
            <p><strong>Sex:</strong> {profile.get('sex', 'Not set')}</p>
            <p><strong>Country:</strong> {profile.get('country', 'Not set')}</p>
            <p><strong>Activity Level:</strong> {profile.get('activity_level', 'Not set')}</p>
            <p><strong>Goals:</strong> {', '.join(profile.get('goals', ['Not set']))}</p>
            <p><strong>Dietary Preferences:</strong> {', '.join(profile.get('dietary_preferences', ['Not set']))}</p>
        </div>
        """, unsafe_allow_html=True)

    # Account Settings Section
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("⚙️ Account Settings (coming soon)"):
        st.write("""
        - Manage password & security  
        - Delete account or clear history  
        - Connect fitness APIs  
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Tip: You can change your name, bio, or preferences — all updates stay saved in this session. This profile data is fetched securely using your Google OAuth login.")
