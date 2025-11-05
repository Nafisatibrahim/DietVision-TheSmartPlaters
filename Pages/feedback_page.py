"""
Feedback Page
Collect user feedback on the AI nutrition assistant and meal analysis.
"""

# Import libraries
import streamlit as st
from google.oauth2.service_account import Credentials
import gspread
from datetime import datetime


def save_feedback_to_sheets(user_email, feedback_text):
    """Save feedback to Google Sheets (same service account as profile)."""
    try:
        if "vertex" in st.secrets:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(st.secrets["vertex"], scopes=SCOPES)
            client = gspread.authorize(creds)
            sheet_id = st.secrets["vertex"]["spreadsheet_id"]

            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]

            # Create or open "Feedback" sheet
            if "feedback" in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() if ws.title.lower().strip() == "feedback")
            else:
                sheet = spreadsheet.add_worksheet(title="Feedback", rows=1000, cols=10)
                sheet.append_row(["Timestamp", "User Email", "Feedback"])

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet.append_row([timestamp, user_email, feedback_text])

            return True, "✅ Feedback saved!"
        else:
            return False, "⚠️ Google Sheets credentials not found."
    except Exception as e:
        return False, f"❌ Error saving feedback: {e}"


def show_feedback_page(user):
    """Displays the Feedback Page."""
    st.title("💬 Feedback & Suggestions")

    # Check authentication
    if not user or not isinstance(user, dict):
        st.warning("⚠️ Please sign in to provide feedback.")
        return

    # Header
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        border-left: 6px solid #4CAF50;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    ">
        <h3 style="color:#2E7D32; margin:0;">🌿 Help Us Improve DietVision.ai</h3>
        <p style="color:#555; margin-top:0.5rem;">
            Your input helps us design better features, enhance nutrition insights,
            and improve AI accuracy. Thank you for contributing! 💚
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Feedback box
    feedback = st.text_area(
        "Share your feedback:",
        placeholder="Tell us what you think about the app, dashboard, predictions, or new features you’d love to see.",
        height=150
    )

    # Rating (optional for prototype)
    st.markdown("### ⭐ How would you rate your experience?")
    rating = st.slider("Select a rating", 1, 5, 4, help="1 = Needs improvement, 5 = Excellent experience")

    # Submit button
    if st.button("📩 Submit Feedback"):
        if feedback.strip():
            success, message = save_feedback_to_sheets(
                user.get("email", "anonymous@dietvision.ai"),
                f"Rating: {rating}/5 | {feedback.strip()}"
            )
            if success:
                st.success(message)
                st.balloons()
            else:
                st.error(message)
        else:
            st.warning("⚠️ Please write some feedback before submitting.")

    # Additional info
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("""
    💡 Your feedback is confidential and helps guide our future updates.  
    Future releases will include real-time analytics, persistent meal tracking, and smart nutrition insights.
    """)
