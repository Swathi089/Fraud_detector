"""
ui/signup.py
============
Signup page for the Fraud Detection System.
Provides a modern, professional registration interface.
"""

from backend.auth import signup
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def signup_page():
    """
    Display the signup page.
    """
    # Custom CSS for signup page
    st.markdown("""
        <style>
        .signup-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 30px;
            background-color: #16213e;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .signup-title {
            text-align: center;
            color: #ffffff;
            margin-bottom: 30px;
        }
        .signup-subtitle {
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

    st.markdown('<h1 class="signup-title">📝 Sign Up</h1>',
                unsafe_allow_html=True)
    st.markdown('<p class="signup-subtitle">Create an account to access the fraud detection system.</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    # Signup form
    with st.form("signup_form"):
        email = st.text_input(
            "📧 Email",
            placeholder="Enter your email address",
            help="Enter a valid email address"
        )

        password = st.text_input(
            "🔑 Password",
            type="password",
            placeholder="Enter your password",
            help="Password must be at least 6 characters"
        )

        confirm_password = st.text_input(
            "🔑 Confirm Password",
            type="password",
            placeholder="Confirm your password",
            help="Re-enter your password"
        )

        # Terms and conditions
        agree_terms = st.checkbox(
            "I agree to the Terms and Conditions",
            help="You must agree to the terms to create an account"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        submit_button = st.form_submit_button(
            "🚀 Create Account",
            type="primary",
            use_container_width=True
        )

        if submit_button:
            if not email or not password or not confirm_password:
                st.warning("Please fill in all fields")
            elif password != confirm_password:
                st.error("✗ Passwords do not match")
            elif len(password) < 6:
                st.error("✗ Password must be at least 6 characters")
            elif not agree_terms:
                st.warning("Please agree to the Terms and Conditions")
            else:
                success, message = signup(email, password)

                if success:
                    st.success(f"✓ {message}")
                    st.info("Please login with your credentials")
                else:
                    st.error(f"✗ {message}")

    st.markdown("---")

    # Login link
    st.markdown("""
    <div style="text-align: center; color: #a0a0a0;">
        Already have an account? <a href="#" onclick="window.location.href='?page=Login'">Login</a>
    </div>
    """, unsafe_allow_html=True)

    # Info
    st.markdown("---")
    st.info("""
    **Why sign up?**
    - Access to fraud detection analytics
    - Upload and analyze your datasets
    - Generate professional reports
    - View interactive visualizations
    """)


if __name__ == "__main__":
    signup_page()
