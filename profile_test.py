"""
Profile Page
Display user's information and account details.
"""

import streamlit as st
import base64

def show_profile_page(user):
    st.title("👤 Your Profile")

    if not user or not isinstance(user, dict):
        st.warning("⚠️ Please sign in to view your profile.")
        return

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

            if st.button("💾 Save Changes"):
                st.success("✅ Profile updated successfully!")
                user["name"] = st.session_state.editable_name
                user["bio"] = st.session_state.editable_bio
                user["picture"] = st.session_state.uploaded_profile_pic

                # (Optional) You can later update Google Sheets here with save_user_profile()

    st.markdown("<br>", unsafe_allow_html=True)

    # Account Settings Section 
    with st.expander("⚙️ Account Settings (coming soon)"):
        st.write("""
        - Manage password & security  
        - Delete account or clear history  
        - Connect fitness APIs  
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    st.info("💡 Tip: You can change your name, bio, or profile photo — all updates stay saved in this session. This profile data is fetched securely using your Google OAuth login. DietVision only has access to your name, email, and profile picture.")

if __name__ == "__main__":
    show_profile_page(st.session_state.get("user", {}))