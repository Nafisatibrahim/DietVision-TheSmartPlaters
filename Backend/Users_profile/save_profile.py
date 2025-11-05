"""
This module provides functionality to save/load user profile information.
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


def load_user_profile(email, path="users.csv"):
    """
    Load user profile from Google Sheets or local CSV.
    
    Args:
        email (str): User's email
        path (str): CSV fallback file path
        
    Returns:
        dict: User profile data or None if not found
    """
    # Try Google Sheets first
    try:
        client, sheet_id = get_sheets_client()
        if client and sheet_id:
            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]
            
            if "user profile" in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() 
                           if ws.title.lower().strip() == "user profile")
                
                all_data = sheet.get_all_values()
                if len(all_data) > 1:
                    headers = all_data[0]
                    rows = all_data[1:]
                    
                    # Find user by email (email is in column 2, index 2)
                    for row in rows:
                        if len(row) > 2 and row[2] == email:
                            return {
                                'name': f"{row[0]} {row[1]}".strip(),
                                'first_name': row[0],
                                'last_name': row[1],
                                'email': row[2],
                                'picture': row[3] if len(row) > 3 else '',
                                'signup_date': row[4] if len(row) > 4 else '',
                                'signin_method': row[5] if len(row) > 5 else '',
                                'last_active': row[6] if len(row) > 6 else ''
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
                    'name': f"{row.get('First Name', '')} {row.get('Last Name', '')}".strip(),
                    'first_name': row.get('First Name', ''),
                    'last_name': row.get('Last Name', ''),
                    'email': row.get('Email', ''),
                    'picture': row.get('Picture', ''),
                    'signup_date': row.get('Signup Date', ''),
                    'signin_method': row.get('Sign-in Method', ''),
                    'last_active': row.get('Last Active', '')
                }
    except Exception as e:
        print(f"Error loading from CSV: {e}")
    
    return None


def save_user_profile(user_info, path="users.csv"):
    """
    Save or update user profile in Google Sheets or CSV.
    
    Args:
        user_info (dict): User information
        path (str): CSV fallback file path
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Try Google Sheets first
    try:
        client, sheet_id = get_sheets_client()
        if client and sheet_id:
            spreadsheet = client.open_by_key(sheet_id)
            worksheet_names = [ws.title.lower().strip() for ws in spreadsheet.worksheets()]
            
            # Get or create sheet
            if "user profile" in worksheet_names:
                sheet = next(ws for ws in spreadsheet.worksheets() 
                           if ws.title.lower().strip() == "user profile")
            else:
                sheet = spreadsheet.add_worksheet(title="User Profile", rows=1000, cols=20)
            
            # Extract core fields
            full_name = user_info.get("name", "")
            first_name, last_name = (full_name.split(" ", 1) + [""])[:2]
            email = user_info.get("email", "")
            picture = user_info.get("picture", "")
            signin_method = "Google OAuth"
            signup_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            last_active = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if not email:
                return (False, "⚠️ Email is required")
            
            # Add header if sheet empty
            if not sheet.get_all_values():
                sheet.append_row([
                    "First Name", "Last Name", "Email", "Picture",
                    "Signup Date", "Sign-in Method", "Last Active"
                ])
            
            # Read existing data
            existing = sheet.get_all_values()
            rows = existing[1:] if len(existing) > 1 else []
            existing_emails = [r[2] for r in rows if len(r) > 2]
            
            if email in existing_emails:
                # Update existing user
                row_index = existing_emails.index(email) + 2
                new_values = [
                    first_name, last_name, email, picture,
                    signup_date, signin_method, last_active
                ]
                sheet.update(range_name=f"A{row_index}:G{row_index}", values=[new_values])
                return (True, "🔄 Profile updated in Google Sheets")
            else:
                # Add new user
                sheet.append_row([
                    first_name, last_name, email, picture,
                    signup_date, signin_method, last_active
                ])
                return (True, "✅ Profile saved to Google Sheets")
                
    except Exception as e:
        # Continue to CSV fallback if Google Sheets fails
        pass
    
    # Fallback to local CSV
    try:
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
            return (True, "✅ Profile saved locally (CSV)")
        
        existing = pd.read_csv(path)
        if 'Email' in existing.columns:
            if user_info.get('email') in existing['Email'].values:
                existing.loc[existing['Email'] == user_info.get('email'), df.columns] = df.values
                existing.to_csv(path, index=False)
                return (True, "🔄 Profile updated locally (CSV)")
            else:
                df.to_csv(path, mode='a', header=False, index=False)
                return (True, "✅ Profile saved locally (CSV)")
        else:
            df.to_csv(path, index=False)
            return (True, "✅ Profile saved locally (CSV)")
            
    except Exception as e:
        return (False, f"❌ Error saving profile: {str(e)}")
