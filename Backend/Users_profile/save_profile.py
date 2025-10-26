"""
This module provides functionality to save or update user profile information.
It includes functions to update user details and store profile pictures.
"""

# Import libraries
import pandas as pd
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Define function to save or update user profile
def save_user_profile(user_info, path="users.csv"):
    try:
        if gspread and "vertex" in st.secrets:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(st.secrets["vertex"], scopes=SCOPES)
            client = gspread.authorize(creds)
            sheet_id = st.secrets["vertex"]["spreadsheet_id"]

            target_sheet_name = "user profile"

            # Open or create the "User profile" sheet
            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]

            if target_sheet_name in worksheet_names:
                # Open the sheet even if capitalization differs
                sheet = next(ws for ws in spreadsheet.worksheets() if ws.title.lower().strip() == target_sheet_name)
            else:
                # Create the sheet only if it truly doesn't exist
                sheet = spreadsheet.add_worksheet(title="User Profile", rows="1000", cols="20")

            # Extract core fields
            full_name = user_info.get("name", "")
            first_name, last_name = (full_name.split(" ", 1) + [""])[:2]
            email = user_info.get("email", "")
            picture = user_info.get("picture", "")
            signin_method = "Google OAuth"
            signup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Add header if sheet empty
            if not sheet.get_all_values():
                sheet.append_row([
                    "First Name", "Last Name", "Email", "Picture",
                    "Signup Date", "Sign-in Method", "Last Active"
                ])

            # Read all existing rows
            existing = sheet.get_all_values()
            rows = existing[1:] if len(existing) > 1 else []
            existing_emails = [r[2] for r in rows] if rows else []

            if email in existing_emails:
                # Update existing user
                row_index = existing_emails.index(email) + 2  # +2 for header offset
                new_values = [
                    first_name, last_name, email, picture,
                    signup_date, signin_method, last_active
                ]
                sheet.update(f"A{row_index}:G{row_index}", [new_values])
                return "🔄 User profile updated in 'User profile' sheet."
            else:
                # Add new user
                sheet.append_row([
                    first_name, last_name, email, picture,
                    signup_date, signin_method, last_active
                ])
                return "✅ User saved to 'User profile' sheet."

    except Exception as e:
        st.warning(f"⚠️ Google Sheets save failed, falling back to local CSV. Error: {e}")

    # Fallback: Save locally (CSV)
    full_name = user_info.get("name", "")
    first_name, last_name = (full_name.split(" ", 1) + [""])[:2]
    df = pd.DataFrame([{
        "First Name": first_name,
        "Last Name": last_name,
        "Email": user_info.get("email", ""),
        "Picture": user_info.get("picture", ""),
        "Signup Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Sign-in Method": "Google OAuth",
        "Last Active": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        df.to_csv(path, index=False)
        return "✅ User saved locally (new file)."

    try:
        existing = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        df.to_csv(path, index=False)
        return "✅ User saved locally (recreated file)."

    # Update or append locally
    if 'Email' in existing.columns:
        if user_info.get('email') in existing['Email'].values:
            existing.loc[existing['Email'] == user_info.get('email'), df.columns] = df.values
            existing.to_csv(path, index=False)
            return "🔄 User profile updated locally."
        else:
            df.to_csv(path, mode='a', header=False, index=False)
            return "✅ User appended to local CSV."
    else:
        df.to_csv(path, index=False)
        return "⚠️ CSV missing email column — recreated file."
