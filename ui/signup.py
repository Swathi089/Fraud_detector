"""
ui/signup.py
============
Signup page for the Fraud Detection System.
Provides a professional registration interface with two-column layout.
Left side: Welcome message | Right side: Credentials form
"""

import sys
import os

# Add project root to Python path FIRST
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import after sys.path is set
from backend.auth import signup
from ui.styles import inject_design_system
import streamlit as st


def signup_page():
    """
    Display the signup page with professional UI - two column layout.
    Left: Welcome message | Right: Signup credentials form
    """
    # Configure page
    st.set_page_config(
        page_title="Sign Up - Fraud Detection System",
        page_icon="🛡️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Inject design system
    inject_design_system()

    # Professional CSS styling
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
        }
        
        .stTextInput > div > div > input {
            background: rgba(30, 41, 59, 0.8) !important;
            color: #f8fafc !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            padding: 12px 14px !important;
            font-size: 14px !important;
            transition: all 0.2s ease !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #8b5cf6 !important;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.15) !important;
            outline: none !important;
            background: rgba(30, 41, 59, 1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #64748b !important;
        }
        
        .stTextInput label {
            color: #e2e8f0 !important;
            font-weight: 500 !important;
            font-size: 13px !important;
            font-family: 'Inter', sans-serif !important;
            margin-bottom: 6px !important;
        }
        
        .stCheckbox label {
            color: #94a3b8 !important;
            font-size: 12px !important;
        }
        
        .stFormSubmitButton > button {
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            font-family: 'Inter', sans-serif !important;
            width: 100% !important;
            transition: all 0.2s ease !important;
        }
        
        .stFormSubmitButton > button:hover {
            background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.4) !important;
        }
        
        .auth-link {
            color: #8b5cf6 !important;
            text-decoration: none !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            cursor: pointer !important;
        }
        
        .auth-link:hover {
            color: #a78bfa !important;
        }
        
        .divider {
            display: flex;
            align-items: center;
            margin: 16px 0;
        }
        
        .divider::before, .divider::after {
            content: '';
            flex: 1;
            height: 1px;
            background: #334155;
        }
        
        .divider span {
            padding: 0 12px;
            color: #64748b;
            font-size: 12px;
        }
        
        @media (max-width: 768px) {
            .left-panel, .right-panel {
                padding: 20px !important;
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # Two-column professional layout
    col_left, col_right = st.columns([1, 1], gap="medium")

    # Left Panel - Welcome Message
    with col_left:
        st.markdown("""
            <div class="left-panel" style="background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%); border-radius: 12px; padding: 32px; height: 100%; min-height: 480px; display: flex; flex-direction: column; justify-content: center; border: 1px solid #334155;">
                <div style="width: 60px; height: 60px; background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 20px;">
                    <span style="font-size: 28px;">🛡️</span>
                </div>
                <h1 style="font-size: 26px; font-weight: 700; color: #f8fafc; margin-bottom: 10px; font-family: 'Inter', sans-serif;">Create Account</h1>
                <p style="color: #94a3b8; font-size: 14px; margin-bottom: 24px; font-family: 'Inter', sans-serif; line-height: 1.5;">Join the Fraud Detection Portal today</p>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 32px; height: 32px; background: rgba(139, 92, 246, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 14px;">🛡️</span></div>
                        <span style="color: #cbd5e1; font-size: 13px; font-family: 'Inter', sans-serif;">Advanced fraud detection</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 32px; height: 32px; background: rgba(236, 72, 153, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 14px;">📊</span></div>
                        <span style="color: #cbd5e1; font-size: 13px; font-family: 'Inter', sans-serif;">Real-time analytics</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 32px; height: 32px; background: rgba(139, 92, 246, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 14px;">🔍</span></div>
                        <span style="color: #cbd5e1; font-size: 13px; font-family: 'Inter', sans-serif;">ML-powered insights</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 32px; height: 32px; background: rgba(236, 72, 153, 0.15); border-radius: 8px; display: flex; align-items: center; justify-content: center;"><span style="font-size: 14px;">📈</span></div>
                        <span style="color: #cbd5e1; font-size: 13px; font-family: 'Inter', sans-serif;">Interactive dashboards</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Right Panel - Signup Form
    with col_right:
        st.markdown("""
            <div class="right-panel" style="background: #1e293b; border-radius: 12px; padding: 32px; height: 100%; min-height: 480px; border: 1px solid #334155;">
                <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 8px; padding: 8px 12px; margin-bottom: 20px;">
                </div>
        """, unsafe_allow_html=True)

        # Signup form
        with st.form("signup_form"):
            email = st.text_input(
                "Email Address",
                placeholder="name@company.com"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="••••••••"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="••••••••"
            )

            agree_terms = st.checkbox(
                "I agree to the Terms and Conditions"
            )

            submit_button = st.form_submit_button(
                "Create Account",
                type="primary"
            )

            if submit_button:
                if not email or not password or not confirm_password:
                    st.warning("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif not agree_terms:
                    st.warning("Please agree to the Terms and Conditions")
                else:
                    success, message = signup(email, password)
                    if success:
                        st.session_state["signup_success"] = True
                        st.session_state["signup_message"] = message
                        st.session_state["landing_page_action"] = "login"
                        st.success(f"Account created successfully! {message}")
                        st.rerun()
                    else:
                        st.error(f"Error: {message}")

        st.markdown("""
                <div class="divider"><span>or</span></div>
                
                <p style="text-align: center; color: #64748b; font-size: 13px; font-family: 'Inter', sans-serif;">
                    Already have an account? <a href="#" class="auth-link">Sign in</a>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Handle login navigation
    if "go_to_login" in st.session_state and st.session_state["go_to_login"]:
        st.session_state["landing_page_action"] = "login"
        st.session_state["go_to_login"] = False
        st.rerun()


if __name__ == "__main__":
    signup_page()
