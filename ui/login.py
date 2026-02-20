"""
ui/login.py
===========
Login page for the Fraud Detection System.
Provides a modern, professional login interface.
"""

from backend.auth import login
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def login_page():
    """
    Display the login page.
    """
    # Custom CSS for login page
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 30px;
            background-color: #16213e;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .login-title {
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
        }
        .login-subtitle {
            text-align: center;
            color: #a0a0a0;
            margin-bottom: 20px;
        }
        .stTextInput > div > div > input {
            background-color: #1a1a2e;
            color: #ffffff;
            border: 1px solid #e94560;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="login-title">🔒 Login</h1>', unsafe_allow_html=True)
    st.markdown('<p class="login-subtitle">Welcome back! Please login to continue.</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    # Login form
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email",
            placeholder="Enter your email address",
            help="Enter your registered email address"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password",
            help="Enter your password"
        )

        col1, col2 = st.columns([1, 2])

        with col1:
            remember_me = st.checkbox("Remember me")

        with col2:
            st.markdown(
                "<div style='text-align: right; padding-top: 5px;'>", unsafe_allow_html=True)
            forgot_password = st.markdown("[Forgot Password?](#)")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        submit_button = st.form_submit_button(
            "🚀 Login",
            type="primary",
            use_container_width=True
        )

        if submit_button:
            if email and password:
                success, message = login(email, password)

                if success:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.success(f"✓ {message}")
                    st.rerun()
                else:
                    st.error(f"✗ {message}")
            else:
                st.warning("Please enter both email and password")

    st.markdown("---")

    # Sign up link
    st.markdown("""
    <div style="text-align: center; color: #a0a0a0;">
        Don't have an account? <a href="#" onclick="window.location.href='?page=Signup'">Sign up</a>
    </div>
    """, unsafe_allow_html=True)

    # Demo credentials info
    st.markdown("---")
    st.info("""
    **Demo Credentials:**
    - Sign up with any email and password (min 6 characters)
    - Or use the sample dataset at: `data/creditcard.csv`
    """)


if __name__ == "__main__":
    login_page()
