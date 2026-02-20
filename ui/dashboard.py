"""
ui/dashboard.py
===============
Main dashboard for the Fraud Detection System.
Provides navigation and layout for the Streamlit UI.
"""

# Add project root to Python path - MUST be at the very top before any imports
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import from ui package and other modules
from ui.login import login_page
from ui.signup import signup_page
from ui.upload import upload_page
from ui.statistics import statistics_page
from ui.report import report_page



import streamlit as st


# Configure page
st.set_page_config(
    page_title="Fraud Detection Analytics Portal",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern look
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #1a1a2e;
        --secondary-color: #16213e;
        --accent-color: #e94560;
        --text-color: #ffffff;
        --background-color: #0f0f1a;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--primary-color);
    }
    
    /* Card styling */
    .metric-card {
        background-color: #16213e;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #e94560;
        margin: 10px 0;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #e94560;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
    }
    
    /* Header styling */
    h1, h2, h3 {
        color: #ffffff;
    }
    
    /* Info boxes */
    .stAlert {
        background-color: #16213e;
        border-left: 4px solid #e94560;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """
    Main function to run the dashboard.
    """
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
    st.sidebar.title("🔒 Fraud Detection")
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
        menu = st.sidebar.radio(
            "Navigation",
            ["Dashboard", "Upload", "Statistics", "Reports"]
        )

        if menu == "Dashboard":
            # Main dashboard content
            st.title("🔒 Fraud Detection Analytics Portal")
            st.markdown("---")

            # Welcome message
            st.markdown(f"### Welcome, {st.session_state['user_email']}!")
            st.markdown(
                "Welcome to the Fraud Detection Analytics Portal. Use the navigation menu to get started.")

            # Quick stats
            st.markdown("---")
            st.subheader("📊 Quick Stats")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric(
                    label="Total Transactions",
                    value=f"{st.session_state['analysis_results']['data_summary']['total_transactions']:,}"
                    if st.session_state.get("analysis_results") else "N/A",
                    delta=None
                )

            with col2:
                st.metric(
                    label="Fraudulent Transactions",
                    value=f"{st.session_state['analysis_results']['fraud_analysis']['fraud_count']:,}"
                    if st.session_state.get("analysis_results") else "N/A",
                    delta=None
                )

            with col3:
                st.metric(
                    label="Fraud Percentage",
                    value=f"{st.session_state['analysis_results']['fraud_analysis']['fraud_percentage']:.2f}%"
                    if st.session_state.get("analysis_results") else "N/A",
                    delta=None
                )

            with col4:
                st.metric(
                    label="Risk Score",
                    value=f"{st.session_state['analysis_results']['fraud_analysis']['risk_scores']['average_risk_score']:.1f}"
                    if st.session_state.get("analysis_results") and 'risk_scores' in st.session_state.get("analysis_results", {}).get("fraud_analysis", {}) else "N/A",
                    delta=None
                )

            st.markdown("---")

            # Feature overview
            st.subheader("📋 Feature Overview")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                ### 🔼 Upload Dataset
                - Upload CSV files with transaction data
                - Preview dataset before analysis
                - Supported formats: CSV
                
                ### 📊 Statistics & Analytics
                - View fraud statistics
                - Interactive charts and visualizations
                - Risk score distribution
                """)

            with col2:
                st.markdown("""
                ### 🎯 Fraud Detection
                - Advanced risk scoring algorithm
                - Automatic fraud flagging
                - Risk level classification (Low/Medium/High)
                
                ### 📑 Reports
                - Generate PDF reports
                - Export to CSV format
                - Download for offline analysis
                """)

            st.markdown("---")

            # Quick actions
            st.subheader("⚡ Quick Actions")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("📤 Upload New Dataset", use_container_width=True):
                    st.rerun()

            with col2:
                if st.button("📈 View Statistics", use_container_width=True):
                    st.rerun()

            with col3:
                if st.button("📑 Generate Report", use_container_width=True):
                    st.rerun()

            # Recent activity (placeholder)
            st.markdown("---")
            st.subheader("📝 Recent Activity")

            if st.session_state.get("dataset_path"):
                st.success(
                    f"✓ Dataset uploaded: {os.path.basename(st.session_state['dataset_path'])}")
            else:
                st.info(
                    "No dataset uploaded yet. Use the Upload option to get started.")

            if st.session_state.get("analysis_results"):
                st.success("✓ Analysis completed successfully")
            else:
                st.info(
                    "No analysis run yet. Upload a dataset and run analysis to see results.")

        elif menu == "Upload":
            upload_page()
        elif menu == "Statistics":
            statistics_page()
        elif menu == "Reports":
            report_page()


if __name__ == "__main__":
    main()
