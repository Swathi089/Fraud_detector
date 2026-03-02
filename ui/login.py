"""
ui/login.py
===========
Login page for the Fraud Detection System.
Provides a professional login interface.
"""

import sys
import os

# Add project root to Python path FIRST
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import after sys.path is set
from backend.auth import login
import streamlit as st


def login_page():
    """
    Display the login page with professional UI.
    """
    # Professional CSS styling
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }
        
        .stTextInput > div > div > input {
            background: rgba(30, 41, 59, 0.8) !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }
        
        .stTextInput label {
            color: #e2e8f0 !important;
        }
        
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Two-column layout
    col_left, col_right = st.columns([1, 1], gap="medium")

    # Left Panel - Welcome
    with col_left:
        st.markdown("""
            <div style="background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-radius: 12px; padding: 32px; height: 100%; min-height: 400px; display: flex; flex-direction: column; justify-content: center; border: 1px solid #334155;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <span style="font-size: 28px;">🔐</span>
                </div>
                <h1 style="font-size: 26px; font-weight: 700; color: #f8fafc; margin-bottom: 10px;">Welcome Back</h1>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 24px;">Sign in to access the Fraud Detection Portal</p>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 14px;">🛡️</span>
                        <span style="color: #cbd5e1; font-size: 13px;">Real-time fraud detection</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 14px;">📊</span>
                        <span style="color: #cbd5e1; font-size: 13px;">Advanced analytics dashboard</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <span style="font-size: 14px;">🔍</span>
                        <span style="color: #cbd5e1; font-size: 13px;">ML-powered risk assessment</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Right Panel - Login Form
    with col_right:
        st.markdown("""
            <div style="background: #1e293b; border-radius: 12px; padding: 32px; height: 100%; min-height: 400px; border: 1px solid #334155;">
                <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;">
                    <h2 style="font-size: 18px; font-weight: 600; color: #f8fafc; margin-bottom: 4px;">Sign In</h2>
                    <p style="color: #94a3b8; font-size: 12px; margin: 0;">Enter your credentials to continue</p>
                </div>
        """, unsafe_allow_html=True)

        # Login form
        with st.form("login_form"):
            email = st.text_input("Email Address", placeholder="name@company.com")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submit_button = st.form_submit_button("Sign In", type="primary", use_container_width=True)

            if submit_button:
                if email and password:
                    success, message = login(email, password)
                    if success:
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = email
                        st.session_state["show_dashboard"] = True
                        st.session_state["landing_page_action"] = None
                        st.session_state["show_login_after_signup"] = False
                        st.success("Welcome back! Redirecting to dashboard...")
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")
                else:
                    st.warning("Please enter both email and password")

        st.markdown("</div>", unsafe_allow_html=True)

    # Sign Up button
    if st.button("Create Account", key="go_to_signup_btn", use_container_width=True):
        st.session_state["landing_page_action"] = "signup"
        st.rerun()

    # Back to home button
    if st.button("Back to Home", key="back_to_home_login"):
        st.session_state["landing_page_action"] = None
        st.session_state["show_dashboard"] = False
        st.rerun()


if __name__ == "__main__":
    login_page()
