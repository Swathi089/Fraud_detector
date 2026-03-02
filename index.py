



"""
index.py
========
Landing page for the Fraud Detection System.
Provides an introduction and navigation to Login/Signup pages.
"""

import streamlit as st
from ui.styles import inject_design_system
from ui.dashboard_complete import main as dashboard_main
import sys
import os

# Add project root to Python path FIRST
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Now import after sys.path is set


# Configure page
st.set_page_config(
    page_title="Fraud Detection Analytics Portal - Home",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject design system CSS
inject_design_system()

# Additional landing page specific styles
st.markdown("""
    <style>
    /* Hide sidebar on landing page */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Remove default Streamlit padding */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
    }

    /* Full width mode */
    .stApp {
        max-width: 100% !important;
    }

    /* Hero Section */
    .hero-container {
        min-height: 85vh;
        display: flex;
        align-items: center;
        padding: 60px 40px;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }

    .hero-content {
        max-width: 1400px;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 60px;
        align-items: center;
        width: 100%;
    }

    .hero-text {
        color: white;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(102, 126, 234, 0.5);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 13px;
        color: #a5b4fc;
        margin-bottom: 20px;
    }

    .hero-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #fff 0%, #a5b4fc 50%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .hero-desc {
        font-size: 18px;
        color: #c7d2fe;
        line-height: 1.7;
        margin-bottom: 35px;
        max-width: 500px;
    }

    .hero-stats {
        display: flex;
        gap: 40px;
        margin-bottom: 35px;
    }

    .stat-box {
        text-align: center;
    }

    .stat-number {
        font-size: 32px;
        font-weight: 800;
        color: #818cf8;
        display: block;
    }

    .stat-text {
        font-size: 13px;
        color: #a5b4fc;
    }

    /* Right side - Features */
    .features-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
    }

    .features-title {
        font-size: 24px;
        font-weight: 700;
        color: white;
        margin-bottom: 25px;
        text-align: center;
    }

    .feature-item {
        display: flex;
        align-items: flex-start;
        gap: 15px;
        padding: 18px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }

    .feature-item:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateX(5px);
    }

    .feature-icon {
        font-size: 28px;
        min-width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
    }

    .feature-info h4 {
        color: white;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 5px;
    }

    .feature-info p {
        color: #a5b4fc;
        font-size: 13px;
        line-height: 1.5;
        margin: 0;
    }

    /* How it works section */
    .how-it-works {
        padding: 80px 40px;
        background: #0f0c29;
        text-align: center;
    }

    .section-title {
        font-size: 36px;
        font-weight: 700;
        color: white;
        margin-bottom: 50px;
    }

    .steps-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
        max-width: 1200px;
        margin: 0 auto;
    }

    .step-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 30px 20px;
        text-align: center;
    }

    .step-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
        color: white;
        margin: 0 auto 20px;
    }

    .step-card h4 {
        color: white;
        font-size: 18px;
        margin-bottom: 10px;
    }

    .step-card p {
        color: #a5b4fc;
        font-size: 14px;
        line-height: 1.5;
    }

    /* CTA Section */
    .cta-section {
        padding: 80px 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        text-align: center;
    }

    .cta-section h2 {
        font-size: 36px;
        font-weight: 700;
        color: white;
        margin-bottom: 15px;
    }

    .cta-section p {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.9);
    }

    /* Footer */
    .footer {
        padding: 30px;
        background: #0f0c29;
        text-align: center;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }

    .footer p {
        color: #64748b;
        font-size: 14px;
    }

    /* Responsive */
    @media (max-width: 968px) {
        .hero-content {
            grid-template-columns: 1fr;
            text-align: center;
        }
        
        .hero-stats {
            justify-content: center;
        }
        
        .hero-desc {
            margin: 0 auto 35px;
        }
        
        .steps-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .hero-container {
            min-height: auto;
            padding: 40px 20px;
        }
    }

    @media (max-width: 576px) {
        .hero-title {
            font-size: 36px;
        }
        
        .steps-grid {
            grid-template-columns: 1fr;
        }
        
        .hero-stats {
            flex-direction: column;
            gap: 20px;
        }
    }
    </style>
""", unsafe_allow_html=True)


def show_landing_page():
    """
    Display the landing page with introduction and navigation.
    """
    # Initialize session state for page navigation
    if "landing_page_action" not in st.session_state:
        st.session_state["landing_page_action"] = None

    # Initialize show_login_after_signup if not exists
    if "show_login_after_signup" not in st.session_state:
        st.session_state["show_login_after_signup"] = False

    # Top right buttons for navigation
    col1, col2 = st.columns([8, 2])
    with col2:
        # Check if user just signed up - auto-redirect to login
        if st.session_state.get("show_login_after_signup", False):
            st.session_state["landing_page_action"] = "login"
            st.rerun()

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔐 Login", key="top_login_btn"):
                st.session_state["landing_page_action"] = "login"
                st.session_state["show_login_after_signup"] = False
                st.rerun()
        with c2:
            if st.button("📝 Sign Up", key="top_signup_btn"):
                st.session_state["landing_page_action"] = "signup"
                st.rerun()

    # Check if user wants to go to login or signup
    action = st.session_state.get("landing_page_action")

    if action == "login":
        login_page()
        return
    elif action == "signup":
        signup_page()
        return

    # Check if user wants to go to dashboard
    if st.session_state.get("show_dashboard", False):
        from ui.dashboard_new import main as dashboard_main
        dashboard_main()
        return

    # Check if user is logged in
    if st.session_state.get("logged_in", False):
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
                <div style="text-align: left; padding: 10px 20px;">
                    <span style="color: #818cf8; font-size: 14px;">👤 {st.session_state.get('user_email', 'User')}</span>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("🚪 Logout", key="landing_logout_btn"):
                st.session_state["logged_in"] = False
                st.session_state["user_email"] = None
                st.session_state["landing_page_action"] = None
                st.session_state["show_dashboard"] = False
                st.rerun()

        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("📊 Go to Dashboard", key="go_to_dashboard_from_landing", use_container_width=True):
                from ui.dashboard_new import main as dashboard_main
                dashboard_main()
                return
        st.markdown("---")

    # Hero Section
    st.markdown("""
        <div class="hero-container">
            <div class="hero-content">
                <div class="hero-text">
                    <span class="hero-badge">🛡️ AI-Powered Security</span>
                    <h1 class="hero-title">Fraud Detection Analytics</h1>
                    <p class="hero-desc">
                        Protect your business with advanced machine learning algorithms. 
                        Detect fraudulent transactions in real-time with 99.7% accuracy.
                    </p>
                    <div class="hero-stats">
                        <div class="stat-box">
                            <span class="stat-number">99.7%</span>
                            <span class="stat-text">Accuracy</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-number">Real-time</span>
                            <span class="stat-text">Detection</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-number">24/7</span>
                            <span class="stat-text">Monitoring</span>
                        </div>
                    </div>
                </div>
                <div class="features-card">
                    <h3 class="features-title">🚀 Key Features</h3>
                    <div class="feature-item">
                        <span class="feature-icon">📊</span>
                        <div class="feature-info">
                            <h4>Advanced Analytics</h4>
                            <p>Interactive dashboards with real-time fraud metrics</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🤖</span>
                        <div class="feature-info">
                            <h4>ML-Powered Detection</h4>
                            <p>Isolation Forest and rule-based algorithms</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📈</span>
                        <div class="feature-info">
                            <h4>Risk Scoring</h4>
                            <p>Advanced percentiles to identify high-risk transactions</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📑</span>
                        <div class="feature-info">
                            <h4>Professional Reports</h4>
                            <p>Generate detailed PDF reports for stakeholders</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">🔒</span>
                        <div class="feature-info">
                            <h4>Secure Authentication</h4>
                            <p>Protect your data with secure user login</p>
                        </div>
                    </div>
                    <div class="feature-item">
                        <span class="feature-icon">📤</span>
                        <div class="feature-info">
                            <h4>Easy Data Upload</h4>
                            <p>Upload CSV files and get instant results</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # How It Works Section
    st.markdown("""
        <div class="how-it-works">
            <h2 class="section-title">💡 How It Works</h2>
            <div class="steps-grid">
                <div class="step-card">
                    <div class="step-number">1</div>
                    <h4>Create Account</h4>
                    <p>Sign up for free to access the platform</p>
                </div>
                <div class="step-card">
                    <div class="step-number">2</div>
                    <h4>Upload Data</h4>
                    <p>Upload your transaction data in CSV format</p>
                </div>
                <div class="step-card">
                    <div class="step-number">3</div>
                    <h4>Analyze Results</h4>
                    <p>View comprehensive fraud analysis and ML insights</p>
                </div>
                <div class="step-card">
                    <div class="step-number">4</div>
                    <h4>Generate Reports</h4>
                    <p>Export professional PDF reports for stakeholders</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # CTA Section
    st.markdown("""
        <div class="cta-section">
            <h2>Ready to Detect Fraud?</h2>
            <p>Join thousands of users protecting their transactions with AI-powered fraud detection</p>
        </div>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            <p>© 2024 Fraud Detection Analytics Portal. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_landing_page()
