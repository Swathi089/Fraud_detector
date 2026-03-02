"""
ui/dashboard_new.py
===================
Main dashboard for the Fraud Detection System.
Provides navigation and layout for the Streamlit UI.
"""

from ui.report import report_page
from ui.statistics import statistics_page
from ui.upload import upload_page
from ui.signup import signup_page
from ui.login import login_page
from ui.styles import inject_design_system
from ui.pages.dataset_overview import dataset_overview_page
from ui.pages.data_quality import data_quality_page
from ui.pages.fraud_analysis import fraud_analysis_page
from ui.pages.risk_percentiles import risk_percentiles_page
from ui.pages.rule_based import rule_based_page
from ui.pages.isolation_forest import isolation_forest_page
from ui.pages.ml_results import ml_results_page
from ui.pages.confusion_matrix import confusion_matrix_page
from ui.pages.precision_recall import precision_recall_page
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """
    Main function to run the dashboard.
    """
    # Configure page
    st.set_page_config(
        page_title="Fraud Detection Analytics Portal",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Inject design system CSS
    inject_design_system()

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if "user_email" not in st.session_state:
        st.session_state["user_email"] = None

    if "dataset_path" not in st.session_state:
        st.session_state["dataset_path"] = None

    if "analysis_results" not in st.session_state:
        st.session_state["analysis_results"] = None

    # Sidebar navigation
    render_sidebar()

    if not st.session_state["logged_in"]:
        render_login_prompt()
    else:
        render_main_content()


def render_sidebar():
    """Render the sidebar with navigation."""
    # Sidebar logo
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 16px 0 24px;">
            <div style="font-size: 40px; margin-bottom: 8px;">🛡️</div>
            <div style="font-size: 18px; font-weight: 700; color: #00d4ff;">Fraud Detection</div>
            <div style="font-size: 11px; color: #6366f1;">Analytics Portal</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    if not st.session_state["logged_in"]:
        menu = st.sidebar.radio(
            "Navigation",
            ["Login", "Signup"]
        )

        if menu == "Login":
            login_page()
        elif menu == "Signup":
            signup_page()
    else:
        # User profile section in sidebar
        st.sidebar.markdown(f"""
            <div class="sidebar-profile">
                <div class="sidebar-avatar">👤</div>
                <div class="sidebar-name">User</div>
                <div class="sidebar-email">{st.session_state['user_email']}</div>
            </div>
        """, unsafe_allow_html=True)

        menu = st.sidebar.radio(
            "Navigation",
            [
                "Dashboard",
                "Dataset Overview",
                "Data Quality",
                "Statistics",
                "Fraud Distribution",
                "Risk Percentiles",
                "Rule-Based Detection",
                "Isolation Forest",
                "ML Results",
                "Confusion Matrix",
                "Precision-Recall",
                "Reports"
            ]
        )

        # Navigation actions
        handle_navigation(menu)


def handle_navigation(menu):
    """Handle navigation actions."""
    # Logout and Home buttons at bottom of sidebar
    st.sidebar.markdown("---")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    with col2:
        if st.button("🏠 Home", use_container_width=True):
            go_home()

    # Route to selected page
    if menu == "Dashboard":
        render_dashboard_page()
    elif menu == "Upload":
        upload_page()
    elif menu == "Dataset Overview":
        dataset_overview_page()
    elif menu == "Data Quality":
        data_quality_page()
    elif menu == "Statistics":
        statistics_page()
    elif menu == "Fraud Distribution":
        fraud_analysis_page()
    elif menu == "Risk Percentiles":
        risk_percentiles_page()
    elif menu == "Rule-Based Detection":
        rule_based_page()
    elif menu == "Isolation Forest":
        isolation_forest_page()
    elif menu == "ML Results":
        ml_results_page()
    elif menu == "Confusion Matrix":
        confusion_matrix_page()
    elif menu == "Precision-Recall":
        precision_recall_page()
    elif menu == "Reports":
        report_page()


def logout():
    """Logout the user."""
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    st.session_state["dataset_path"] = None
    st.session_state["analysis_results"] = None
    st.session_state["show_dashboard"] = False
    st.session_state["landing_page_action"] = None
    st.rerun()


def go_home():
    """Go to home/landing page."""
    st.session_state["show_dashboard"] = False
    st.session_state["landing_page_action"] = None
    st.rerun()


def render_login_prompt():
    """Render login prompt for unauthenticated users."""
    st.markdown("""
        <div style="text-align: center; padding: 80px 20px;">
            <div style="font-size: 64px; margin-bottom: 24px;">🔒</div>
            <h2 style="color: #f8fafc; margin-bottom: 12px;">Authentication Required</h2>
            <p style="color: #94a3b8; max-width: 500px; margin: 0 auto;">
                Please login or sign up to access the Fraud Detection Portal.
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state["landing_page_action"] = "login"
            st.rerun()
    with col2:
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state["landing_page_action"] = "signup"
            st.rerun()


def render_main_content():
    """Render the main dashboard content."""
    pass  # Content is rendered in handle_navigation


def render_dashboard_page():
    """Render the main dashboard page."""
    # Welcome section
    st.markdown("""
        <div class="glass-card" style="margin-bottom: 24px; padding: 24px !important;">
            <h1 style="margin-bottom: 8px;">Welcome to Fraud Detection Analytics</h1>
            <p style="color: #94a3b8; margin: 0;">Monitor, analyze, and detect fraudulent transactions with advanced ML-powered analytics</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick stats
    st.markdown("### 📊 Quick Stats")

    col1, col2, col3, col4 = st.columns(4)

    total_txn = "N/A"
    fraud_txn = "N/A"
    fraud_pct = "N/A"
    risk_score = "N/A"

    if st.session_state.get("analysis_results"):
        results = st.session_state["analysis_results"]
        if "fraud_analysis" in results:
            fa = results["fraud_analysis"]
            total_txn = f"{fa.get('total_transactions', 0):,}"
            fraud_txn = f"{fa.get('fraud_transactions', 0):,}"
            fraud_pct = f"{fa.get('fraud_percentage', 0):.2f}%"
            if "risk_scores" in fa:
                risk_score = f"{fa['risk_scores'].get('average_risk_score', 0):.1f}"

    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-icon">📊</div>
                <div class="metric-label">Total Transactions</div>
                <div class="metric-value">""" + total_txn + """</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-icon">⚠️</div>
                <div class="metric-label">Fraud Transactions</div>
                <div class="metric-value" style="color: #ef4444 !important;">""" + fraud_txn + """</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-icon">📈</div>
                <div class="metric-label">Fraud Percentage</div>
                <div class="metric-value" style="color: #f59e0b !important;">""" + fraud_pct + """</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-label">Risk Score</div>
                <div class="metric-value" style="color: #00d4ff !important;">""" + risk_score + """</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Features section - Vertical Layout
    st.markdown("### 🚀 Features")

    st.markdown("""
        <div class="glass-card" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 28px; margin-right: 16px;">📤</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 4px;">Upload Dataset</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        Upload CSV files with transaction data. Preview your dataset before analysis.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 28px; margin-right: 16px;">📊</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 4px;">Statistics & Analytics</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        View comprehensive fraud statistics with interactive charts and visualizations.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 28px; margin-right: 16px;">🛡️</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 4px;">Fraud Detection</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        Advanced ML-powered risk scoring algorithm with automatic fraud flagging.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card">
            <div style="display: flex; align-items: center;">
                <div style="font-size: 28px; margin-right: 16px;">📑</div>
                <div>
                    <div style="font-size: 16px; font-weight: 600; color: #f8fafc; margin-bottom: 4px;">Reports</div>
                    <div style="font-size: 13px; color: #94a3b8; line-height: 1.5;">
                        Generate professional PDF reports, export to CSV, or download for offline analysis.
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick actions
    st.markdown("### ⚡ Quick Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Upload New Dataset", use_container_width=True):
            st.session_state["menu"] = "Upload"
            st.rerun()

    with col2:
        if st.button("📈 View Statistics", use_container_width=True):
            st.session_state["menu"] = "Statistics"
            st.rerun()

    with col3:
        if st.button("📑 Generate Report", use_container_width=True):
            st.session_state["menu"] = "Reports"
            st.rerun()

    # Recent activity
    st.markdown("---")
    st.markdown("### 📝 Recent Activity")

    if st.session_state.get("dataset_path"):
        st.success(
            f"✓ Dataset uploaded: {os.path.basename(st.session_state['dataset_path'])}")
    else:
        st.info("No dataset uploaded yet. Use the Upload option to get started.")

    if st.session_state.get("analysis_results"):
        st.success("✓ Analysis completed successfully")
    else:
        st.info(
            "No analysis run yet. Upload a dataset and run analysis to see results.")


if __name__ == "__main__":
    main()
