"""
This module saves/loads users' extended health and nutrition preferences.
Uses Google Sheets as primary storage with CSV fallback.
"""

import pandas as pd
import os
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


def get_sheets_client():
    """Get Google Sheets client and spreadsheet ID."""
    try:
        if "vertex" in st.secrets:
            SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_info(st.secrets["vertex"], scopes=SCOPES)
            client = gspread.authorize(creds)
            sheet_id = st.secrets["vertex"]["spreadsheet_id"]
            return client, sheet_id
        return None, None
    except Exception as e:
        return None, None


def load_user_preferences(email, path="user_preferences.csv"):
    """
    Load user preferences from Google Sheets or local CSV.
    
    Args:
        email (str): User's email
        path (str): CSV fallback file path
        
    Returns:
        dict: User preferences or None if not found
    """
    # Try Google Sheets first
    try:
        client, sheet_id = get_sheets_client()
        if client and sheet_id:
            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]
            
            if "health & preferences" in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() 
                           if ws.title.lower().strip() == "health & preferences")
                
                all_data = sheet.get_all_values()
                if len(all_data) > 1:
                    headers = all_data[0]
                    rows = all_data[1:]
                    
                    # Find user by email (email is first column)
                    for row in rows:
                        if row[0] == email:
                            return {
                                'age': int(row[1]) if row[1] and row[1].isdigit() else 25,
                                'sex': row[2] if len(row) > 2 else '',
                                'country': row[3] if len(row) > 3 else '',
                                'ethnicity': row[4] if len(row) > 4 else '',
                                'cuisine': [x.strip() for x in row[5].split(", ") if x.strip()] if len(row) > 5 and row[5] else [],
                                'activity_level': row[6] if len(row) > 6 else '',
                                'health_conditions': [x.strip() for x in row[7].split(", ") if x.strip()] if len(row) > 7 and row[7] else [],
                                'goals': [x.strip() for x in row[8].split(", ") if x.strip()] if len(row) > 8 and row[8] else [],
                                'dietary_preferences': [x.strip() for x in row[9].split(", ") if x.strip()] if len(row) > 9 and row[9] else [],
                                'updated_at': row[10] if len(row) > 10 else ''
                            }
    except Exception as e:
        print(f"Error loading from Google Sheets: {e}")
    
    # Fallback to local CSV
    try:
        if os.path.exists(path):
            df = pd.read_csv(path)
            user_data = df[df['Email'] == email]
            if not user_data.empty:
                row = user_data.iloc[0]
                return {
                    'age': int(row.get('Age', 25)) if pd.notna(row.get('Age')) else 25,
                    'sex': row.get('Sex', ''),
                    'country': row.get('Country', ''),
                    'ethnicity': row.get('Ethnicity', ''),
                    'cuisine': [x.strip() for x in str(row.get('Cuisine', '')).split(", ") if x.strip()] if row.get('Cuisine') else [],
                    'activity_level': row.get('Activity Level', ''),
                    'health_conditions': [x.strip() for x in str(row.get('Health Conditions', '')).split(", ") if x.strip()] if row.get('Health Conditions') else [],
                    'goals': [x.strip() for x in str(row.get('Goals', '')).split(", ") if x.strip()] if row.get('Goals') else [],
                    'dietary_preferences': [x.strip() for x in str(row.get('Dietary Preferences', '')).split(", ") if x.strip()] if row.get('Dietary Preferences') else [],
                    'updated_at': row.get('Updated At', '')
                }
    except Exception as e:
        print(f"Error loading from CSV: {e}")
    
    return None


def save_user_preferences(email, preferences, path="user_preferences.csv"):
    """
    Save or update user preferences in Google Sheets or CSV.
    
    Args:
        email (str): User's email (unique identifier)
        preferences (dict): Dictionary of health/nutrition preferences
        path (str): CSV fallback file path
        
    Returns:
        tuple: (success: bool, message: str)
    """
    if not email:
        return (False, "⚠️ Email is required")
    
    # Try Google Sheets first
    try:
        client, sheet_id = get_sheets_client()
        if client and sheet_id:
            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]
            
            # Get or create sheet
            if "health & preferences" in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() 
                           if ws.title.lower().strip() == "health & preferences")
            else:
                sheet = spreadsheet.add_worksheet(title="Health & Preferences", rows=1000, cols=25)
            
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
            emails = [r[0] for r in rows if len(r) > 0]
            
            if email in emails:
                # Update existing
                row_index = emails.index(email) + 2
                new_values = [[
                    email, age, sex, country, ethnicity, cuisine, activity,
                    health, goals, diet, updated
                ]]
                sheet.update(range_name=f"A{row_index}:K{row_index}", values=new_values)
                return (True, "🔄 Preferences updated in Google Sheets")
            else:
                # Append new
                sheet.append_row([
                    email, age, sex, country, ethnicity, cuisine, activity,
                    health, goals, diet, updated
                ])
                return (True, "✅ Preferences saved to Google Sheets")
                
    except Exception as e:
        # Continue to CSV fallback if Google Sheets fails
        pass
    
    # Fallback to local CSV
    try:
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
            return (True, "✅ Preferences saved locally (CSV)")
        
        existing = pd.read_csv(path)
        if "Email" in existing.columns and email in existing["Email"].values:
            existing.loc[existing["Email"] == email, df.columns] = df.values
            existing.to_csv(path, index=False)
            return (True, "🔄 Preferences updated locally (CSV)")
        else:
            df.to_csv(path, mode="a", header=False, index=False)
            return (True, "✅ Preferences saved locally (CSV)")
            
    except Exception as e:
        return (False, f"❌ Error saving preferences: {str(e)}")
