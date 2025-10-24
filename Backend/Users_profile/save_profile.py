"""
This module provides functionality to save user profile information.
It includes functions to update user details and store profile pictures.
"""

# Import libraries
import pandas as pd
import os

# Define function to save user profile
def save_user_profile(user_info, path="users.csv"):
    # Save new user info to a CSV file
    df = pd.DataFrame([user_info])

    # legacy behavior (was previously a triple-quoted block) — keep as comment:
    # if os.path.exists(path):
    #     existing = pd.read_csv(path)
    #     if user_info['email'] in existing['email'].values:
    #         df.to_csv(path, mode='a', header=False, index=False)
    # else:
    #     df.to_csv(path, index=False)

    # If file doesn't exist or is empty → create it fresh
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        df.to_csv(path, index=False)
        return

    # Try to read existing file, skip errors if it's corrupted
    try:
        existing = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        # Recreate file if corrupted/empty
        df.to_csv(path, index=False)
        return

    # Append only if this user isn't already in the file
    if 'email' in existing.columns:
        if user_info.get('email') not in existing['email'].values:
            df.to_csv(path, mode='a', header=False, index=False)
    else:
        # File had no 'email' column (unexpected) — overwrite
        df.to_csv(path, index=False)