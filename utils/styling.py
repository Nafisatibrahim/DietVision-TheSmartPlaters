"""
Styling Utils
Applies custom CSS styles for DietVision.ai
"""

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

        /* Responsive Feature Section */
        .feature-container {
            display: flex;
            flex-wrap: nowrap;
            justify-content: center;
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .feature-box {
            background: rgba(255, 255, 255, 0.98);
            border-radius: 15px;
            padding: 1.2rem;
            flex: 1 1 300px;
            width: 30%;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }

        .feature-box:hover {
            transform: translateY(-4px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }

        .feature-box h3 {
            color: #2E7D32;
            font-size: 1.2rem;
            margin-bottom: 0.5rem;
        }

        .feature-box p {
            color: #333;
            font-size: 0.95rem;
        }

        /* 📱 Mobile responsiveness */
        @media (max-width: 768px) {
            .feature-box {
                flex: 1 1 100%;
                min-width: 90%;
                max-width: 95%;
                padding: 1rem;
            }
            .feature-box h3 {
                font-size: 1.1rem;
            }
            .feature-box p {
                font-size: 0.9rem;
            }
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
                
        /* --- Sidebar layout fixes --- */
        section[data-testid="stSidebar"] {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100vh; /* take full screen height */
            overflow-y: hidden !important; /* hide scroll */
            padding-bottom: 1rem;
        }

        /* Sidebar inner content */
        section[data-testid="stSidebar"] > div:first-child {
            flex-grow: 1;
            overflow-y: auto; /* allow content to scroll internally only if window too small */
        }

        /* Footer stays pinned */
        .sidebar-footer {
            text-align: center;
            font-size: 0.9rem;
            line-height: 1.6;
            margin-top: auto;
}

    </style>
    """, unsafe_allow_html=True)
