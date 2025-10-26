"""
This module provides functionality to save user profile information.
It includes functions to update user details and store profile pictures.
"""

# Import libraries
import pandas as pd
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Define function to save user profile
def save_user_profile(user_info, path="users.csv"):
    # Save new user info to a CSV file
    try:
        if gspread and "vertex" in st.secrets:
            st.write("🟢 Connecting to Google Sheets...")  # TEMP debug
            creds = Credentials.from_service_account_info(st.secrets["vertex"])
            client = gspread.authorize(creds)
            sheet_id = st.secrets["vertex"]["spreadsheet_id"]
            st.write(f"✅ Using sheet ID: {sheet_id}")  # TEMP debug
            sheet = client.open_by_key(sheet_id).sheet1

            # Add header row if sheet is empty
            if not sheet.get_all_values():
                st.write("🟡 Creating headers...")
                sheet.append_row(["Name", "Email", "Picture"])

            # Prevent duplicate emails
            existing = sheet.get_all_values()
            existing_emails = [r[1] for r in existing[1:]] if len(existing) > 1 else []
            if user_info.get("email") not in existing_emails:
                sheet.append_row([
                    user_info.get("name", ""),
                    user_info.get("email", ""),
                    user_info.get("picture", "")
                ])
                st.success("✅ User saved to Google Sheets!")
            else:
                st.info("ℹ️ User already exists in Google Sheets.")
            return "✅ User saved to Google Sheets."

    except Exception as e:
        st.warning(f"⚠️ Google Sheets save failed, falling back to local CSV. Error: {e}")

    # Fallback: Save to local CSV
    df = pd.DataFrame([user_info])

    # Create new file if missing or empty
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        df.to_csv(path, index=False)
        return "✅ User saved locally (new file)."

    # Try reading existing data
    try:
        existing = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        df.to_csv(path, index=False)
        return "✅ User saved locally (recreated file)."

    # Append only if not already present
    if 'email' in existing.columns:
        if user_info.get('email') not in existing['email'].values:
            df.to_csv(path, mode='a', header=False, index=False)
            return "✅ User appended to local CSV."
        else:
            return "ℹ️ User already exists in local CSV."
    else:
        df.to_csv(path, index=False)
        return "⚠️ CSV missing email column — recreated file."
