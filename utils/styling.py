"""
Styling Utils
Applies custom CSS styles for DietVision.ai
"""

# Import libraries
import streamlit as st

def apply_custom_styles():
    """Inject global CSS for consistent design."""
    st.markdown("""
    <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #81C784 0%, #4CAF50 30%, #FF9800 70%, #FF6F00 100%);
            background-attachment: fixed;
        }

        /* Main content area */
        .main .block-container {
            background: rgba(255, 255, 255, 0.9);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(15px);
        }

        /* Buttons */
        .stButton > button {
            border-radius: 25px;
            background: linear-gradient(45deg, #4CAF50, #8BC34A);
            color: white;
            border: none;
            padding: 0.5rem 2rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }

        /* Cards */
        .custom-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 5px 25px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        /* Footer */
        .footer {
            background: rgba(46, 125, 50, 0.9);
            color: white;
            text-align: center;
            padding: 1rem;
            border-radius: 15px;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
