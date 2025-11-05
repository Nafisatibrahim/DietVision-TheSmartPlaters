"""
This module saves or updates users' extended health and nutrition preferences
to Google Sheets (sheet: "Health & Preferences") with a CSV fallback.
"""

import pandas as pd
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


def save_user_preferences(email, preferences, path="user_preferences.csv"):
    """
    Save or update extended user preferences in Google Sheets or locally.
    Args:
        email (str): User's email (unique identifier)
        preferences (dict): Dictionary of fields like age, sex, country, etc.
        path (str): Local fallback CSV file path
    """

    try:
        if gspread and "vertex" in st.secrets:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(st.secrets["vertex"], scopes=SCOPES)
            client = gspread.authorize(creds)
            sheet_id = st.secrets["vertex"]["spreadsheet_id"]

            spreadsheet = client.open_by_key(sheet_id)
            target_sheet_name = "Health & Preferences"

            # Check if sheet exists
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]
            if target_sheet_name.lower() in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() if ws.title.lower().strip() == target_sheet_name.lower())
            else:
                sheet = spreadsheet.add_worksheet(title=target_sheet_name, rows="1000", cols="25")

            # Add header if empty
            if not sheet.get_all_values():
                sheet.append_row([
                    "Email", "Age", "Sex", "Country", "Ethnicity", "Cuisine",
                    "Activity Level", "Health Conditions", "Goals",
                    "Dietary Preferences", "Updated At"
                ])

            # Extract data
            age = preferences.get("age", "")
            sex = preferences.get("sex", "")
            country = preferences.get("country", "")
            ethnicity = preferences.get("ethnicity", "")
            cuisine = ", ".join(preferences.get("cuisine", []))
            activity = preferences.get("activity_level", "")
            health = ", ".join(preferences.get("health_conditions", []))
            goals = ", ".join(preferences.get("goals", []))
            diet = ", ".join(preferences.get("dietary_preferences", []))
            updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Read existing data
            existing = sheet.get_all_values()
            rows = existing[1:] if len(existing) > 1 else []
            emails = [r[0] for r in rows] if rows else []

            if email in emails:
                # Update existing
                row_index = emails.index(email) + 2
                new_values = [[
                    email, age, sex, country, ethnicity, cuisine, activity,
                    health, goals, diet, updated
                ]]
                sheet.update(f"A{row_index}:K{row_index}", new_values)
                return "🔄 Preferences updated in Google Sheets."
            else:
                # Append new
                sheet.append_row([
                    email, age, sex, country, ethnicity, cuisine, activity,
                    health, goals, diet, updated
                ])
                return "✅ Preferences saved to Google Sheets."

    except Exception as e:
        st.warning(f"⚠️ Google Sheets save failed, saving locally instead. Error: {e}")

    # ========== Fallback to Local CSV ==========
    df = pd.DataFrame([{
        "Email": email,
        "Age": preferences.get("age", ""),
        "Sex": preferences.get("sex", ""),
        "Country": preferences.get("country", ""),
        "Ethnicity": preferences.get("ethnicity", ""),
        "Cuisine": ", ".join(preferences.get("cuisine", [])),
        "Activity Level": preferences.get("activity_level", ""),
        "Health Conditions": ", ".join(preferences.get("health_conditions", [])),
        "Goals": ", ".join(preferences.get("goals", [])),
        "Dietary Preferences": ", ".join(preferences.get("dietary_preferences", [])),
        "Updated At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])

    if not os.path.exists(path):
        df.to_csv(path, index=False)
        return "✅ Preferences saved locally (new file)."

    try:
        existing = pd.read_csv(path)
        if "Email" in existing.columns and email in existing["Email"].values:
            existing.loc[existing["Email"] == email, df.columns] = df.values
            existing.to_csv(path, index=False)
            return "🔄 Preferences updated locally."
        else:
            df.to_csv(path, mode="a", header=False, index=False)
            return "✅ Preferences appended locally."
    except Exception as e:
        df.to_csv(path, index=False)
        return f"⚠️ Local save fallback triggered. Error: {e}"
