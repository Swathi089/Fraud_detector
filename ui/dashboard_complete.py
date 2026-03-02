"""
ui/dashboard_complete.py
========================
COMPLETE Dashboard for the Fraud Detection System.
All features integrated in one dashboard with horizontal navigation bar.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from ui.styles import inject_design_system
from backend.report_generator import generate_report
from backend.api import run_analysis, get_dataset_info
from backend.auth import login, signup
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports

# Page configuration
st.set_page_config(
    page_title="Fraud Detection Analytics Portal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject design system
inject_design_system()

# ==================== SESSION STATE ====================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None
if "dataset_path" not in st.session_state:
    st.session_state["dataset_path"] = None
if "analysis_results" not in st.session_state:
    st.session_state["analysis_results"] = None
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard"

# ==================== SIDEBAR ====================


def render_sidebar():
    """Render the sidebar with navigation."""
    # Logo
    st.sidebar.markdown("""
        <div style="text-align: center; padding: 16px 0 24px;">
            <div style="font-size: 48px; margin-bottom: 8px;">🛡️</div>
            <div style="font-size: 20px; font-weight: 700; color: #00d4ff;">Fraud Detection</div>
            <div style="font-size: 12px; color: #6366f1;">Analytics Portal</div>
        </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")

    # User profile
    if st.session_state["logged_in"]:
        st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(99,102,241,0.1)); 
                        border-radius: 12px; padding: 16px; margin-bottom: 20px; text-align: center;">
                <div style="font-size: 40px;">👤</div>
                <div style="color: #fff; font-weight: 600;">User</div>
                <div style="color: #94a3b8; font-size: 12px;">{st.session_state.get('user_email', '')}</div>
            </div>
        """, unsafe_allow_html=True)

        # Navigation menu
        menu_items = [
            "📊 Dashboard",
            "📤 Upload Dataset",
            "📋 Dataset Overview",
            "✅ Data Quality",
            "📈 Statistics",
            "🚨 Fraud Distribution",
            "📉 Risk Percentiles",
            "⚖️ Rule-Based",
            "🌲 Isolation Forest",
            "🤖 ML Results",
            "📊 Confusion Matrix",
            "📈 Precision-Recall",
            "📑 Reports"
        ]

        st.session_state["current_page"] = st.sidebar.radio(
            "Navigation", menu_items)

        st.sidebar.markdown("---")

        # Logout button
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user_email"] = None
            st.session_state["dataset_path"] = None
            st.session_state["analysis_results"] = None
            st.rerun()
    else:
        st.sidebar.info("Please login to access the portal")

# ==================== AUTH PAGES ====================


def login_page():
    """Professional login page."""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 40px;
            background: linear-gradient(135deg, rgba(21,31,46,0.95), rgba(27,38,59,0.95));
            border-radius: 20px;
            border: 1px solid rgba(0,212,255,0.2);
        }
        .auth-title {
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 30px;
        }
        </style>
        <div class="auth-container">
            <div class="auth-title">🔐 Login</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input(
            "Password", type="password", placeholder="Enter your password")
        submit = st.form_submit_button("Sign In", use_container_width=True)

        if submit:
            if email and password:
                success, message = login(email, password)
                if success:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    st.success(f"✓ Welcome back!")
                    st.rerun()
                else:
                    st.error(f"✗ {message}")
            else:
                st.warning("Please enter email and password")

    if st.button("Create Account"):
        st.session_state["show_signup"] = True
        st.rerun()


def signup_page():
    """Professional signup page."""
    st.markdown("""
        <style>
        .auth-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 40px;
            background: linear-gradient(135deg, rgba(21,31,46,0.95), rgba(27,38,59,0.95));
            border-radius: 20px;
            border: 1px solid rgba(0,212,255,0.2);
        }
        .auth-title {
            text-align: center;
            font-size: 28px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 30px;
        }
        </style>
        <div class="auth-container">
            <div class="auth-title">📝 Sign Up</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("signup_form"):
        email = st.text_input("Email", placeholder="Enter your email")
        password = st.text_input(
            "Password", type="password", placeholder="Create a password")
        confirm = st.text_input(
            "Confirm Password", type="password", placeholder="Confirm your password")
        submit = st.form_submit_button(
            "Create Account", use_container_width=True)

        if submit:
            if email and password and confirm:
                if password != confirm:
                    st.error("✗ Passwords do not match")
                elif len(password) < 6:
                    st.error("✗ Password must be at least 6 characters")
                else:
                    success, message = signup(email, password)
                    if success:
                        st.success(f"✓ {message}")
                        st.info("Please login with your credentials")
                    else:
                        st.error(f"✗ {message}")
            else:
                st.warning("Please fill in all fields")

    if st.button("Already have an account? Login"):
        st.session_state["show_signup"] = False
        st.rerun()

# ==================== MAIN PAGES ====================


def page_dashboard():
    """Main dashboard page."""
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9)); 
                    border-radius: 16px; padding: 24px; margin-bottom: 24px; border: 1px solid rgba(0,212,255,0.15);">
            <h1 style="margin-bottom: 8px;">📊 Welcome to Fraud Detection Analytics</h1>
            <p style="color: #94a3b8; margin: 0;">Monitor, analyze, and detect fraudulent transactions with advanced ML-powered analytics</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick stats - UPDATED: Auto-detect from uploaded dataset
    col1, col2, col3, col4 = st.columns(4)

    total_txn = "N/A"
    fraud_txn = "N/A"
    fraud_pct = "N/A"
    risk_score = "N/A"
    fraud_col_detected = None

    # Try to get stats from uploaded dataset directly
    if st.session_state.get("dataset_path"):
        try:
            df = pd.read_csv(st.session_state["dataset_path"])
            total_txn = f"{len(df):,}"

            # Auto-detect fraud column
            for col in df.columns:
                if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'is_fraud']:
                    fraud_col_detected = col
                    break

            if fraud_col_detected:
                fraud_count = df[fraud_col_detected].sum() if df[fraud_col_detected].dtype in [
                    'int64', 'float64'] else (df[fraud_col_detected] == 1).sum()
                fraud_txn = f"{fraud_count:,}"
                fraud_pct = f"{(fraud_count/len(df)*100):.2f}%"

                # Store detected fraud column in session
                st.session_state["fraud_column"] = fraud_col_detected
        except Exception as e:
            st.warning(f"Could not read dataset: {str(e)}")

    # If analysis results exist, use them (they are more comprehensive)
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
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9)); 
                        border-radius: 12px; padding: 20px; border: 1px solid rgba(0,212,255,0.15);">
                <div style="font-size: 24px; margin-bottom: 8px;">📊</div>
                <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase;">Total Transactions</div>
                <div style="color: #fff; font-size: 28px; font-weight: 700;">{total_txn}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9)); 
                        border-radius: 12px; padding: 20px; border: 1px solid rgba(239,68,68,0.15);">
                <div style="font-size: 24px; margin-bottom: 8px;">⚠️</div>
                <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase;">Fraud Transactions</div>
                <div style="color: #ef4444; font-size: 28px; font-weight: 700;">{fraud_txn}</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9)); 
                        border-radius: 12px; padding: 20px; border: 1px solid rgba(245,158,11,0.15);">
                <div style="font-size: 24px; margin-bottom: 8px;">📈</div>
                <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase;">Fraud Percentage</div>
                <div style="color: #f59e0b; font-size: 28px; font-weight: 700;">{fraud_pct}</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9)); 
                        border-radius: 12px; padding: 20px; border: 1px solid rgba(0,212,255,0.15);">
                <div style="font-size: 24px; margin-bottom: 8px;">🎯</div>
                <div style="color: #94a3b8; font-size: 12px; text-transform: uppercase;">Risk Score</div>
                <div style="color: #00d4ff; font-size: 28px; font-weight: 700;">{risk_score}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📤 Upload Dataset", use_container_width=True):
            st.session_state["current_page"] = "📤 Upload Dataset"
            st.rerun()
    with col2:
        if st.button("📊 Run Analysis", use_container_width=True):
            if st.session_state.get("dataset_path"):
                with st.spinner("Running analysis..."):
                    results = run_analysis(st.session_state["dataset_path"])
                    st.session_state["analysis_results"] = results
                st.success("Analysis completed!")
            else:
                st.warning("Please upload a dataset first")
    with col3:
        if st.button("📑 Generate Report", use_container_width=True):
            st.session_state["current_page"] = "📑 Reports"
            st.rerun()

    # Status - UPDATED: Show more info about uploaded dataset
    st.markdown("---")
    st.markdown("### 📝 Status")

    if st.session_state.get("dataset_path"):
        st.success(
            f"✓ Dataset loaded: {os.path.basename(st.session_state['dataset_path'])}")
        # Show dataset info
        try:
            df = pd.read_csv(st.session_state["dataset_path"])
            st.info(
                f"📊 Dataset contains {len(df):,} rows and {len(df.columns)} columns")
            if fraud_col_detected:
                st.info(f"🔍 Detected fraud column: **{fraud_col_detected}**")
        except:
            pass
    else:
        st.info("No dataset uploaded. Go to Upload to add data.")

    if st.session_state.get("analysis_results"):
        st.success("✓ Analysis completed successfully")
    else:
        st.info("No analysis run yet. Run analysis for detailed insights.")


def page_upload():
    """Upload dataset page."""
    st.markdown("""
        <h1>📤 Upload Dataset</h1>
        <p style="color: #94a3b8;">Upload your transaction CSV file for fraud analysis</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        # Save the file
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state["dataset_path"] = file_path

        # Preview
        df = pd.read_csv(file_path)

        st.success(f"✓ File uploaded: {uploaded_file.name}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Rows", f"{len(df):,}")
        with col2:
            st.metric("Columns", f"{len(df.columns)}")
        with col3:
            st.metric("File Size", f"{os.path.getsize(file_path)/1024:.1f} KB")

        st.markdown("### 👀 Preview")
        st.dataframe(df.head(), use_container_width=True)

    st.markdown("---")

    # Sample data
    st.markdown("### 📁 Sample Dataset")
    if st.button("Use Sample Data (creditcard.csv)"):
        sample_path = "data/creditcard.csv"
        if os.path.exists(sample_path):
            st.session_state["dataset_path"] = sample_path
            st.success("Using sample dataset!")
            st.rerun()
        else:
            st.error("Sample file not found")


def page_dataset_overview():
    """Dataset overview page."""
    st.markdown("""
        <h1>📋 Dataset Overview</h1>
        <p style="color: #94a3b8;">View details about your uploaded dataset</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Basic info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", f"{len(df):,}")
        with col2:
            st.metric("Total Columns", len(df.columns))
        with col3:
            st.metric(
                "File Size", f"{os.path.getsize(st.session_state['dataset_path'])/1024:.1f} KB")

        st.markdown("---")

        # Columns
        st.markdown("### 📝 Column Information")
        col_info = []
        for col in df.columns:
            col_info.append({
                "Column": col,
                "Type": str(df[col].dtype),
                "Non-Null": df[col].count(),
                "Null": df[col].isnull().sum(),
                "Unique": df[col].nunique()
            })
        st.dataframe(pd.DataFrame(col_info), use_container_width=True)

        st.markdown("---")

        # Preview
        st.markdown("### 👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_data_quality():
    """Data quality page."""
    st.markdown("""
        <h1>✅ Data Quality Report</h1>
        <p style="color: #94a3b8;">Check for missing values, duplicates, and data quality issues</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Missing values
        st.markdown("### ❌ Missing Values")
        missing = df.isnull().sum()
        missing_df = pd.DataFrame(
            {"Column": missing.index, "Missing Count": missing.values, "Missing %": (missing/len(df)*100).values})
        st.dataframe(missing_df, use_container_width=True)

        st.markdown("---")

        # Duplicates
        st.markdown("### 🔄 Duplicates")
        dup_count = df.duplicated().sum()
        st.metric("Duplicate Rows", f"{dup_count:,}")

        st.markdown("---")

        # Data types
        st.markdown("### 📊 Data Types")
        type_counts = df.dtypes.value_counts()
        st.dataframe(pd.DataFrame({"Data Type": type_counts.index.astype(
            str), "Count": type_counts.values}), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_statistics():
    """Statistics page."""
    st.markdown("""
        <h1>📈 Statistical Summary</h1>
        <p style="color: #94a3b8;">Comprehensive statistical analysis of your data</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    if not st.session_state.get("analysis_results"):
        if st.button("🔄 Run Analysis"):
            with st.spinner("Running analysis..."):
                results = run_analysis(st.session_state["dataset_path"])
                st.session_state["analysis_results"] = results
            st.success("Analysis completed!")
            st.rerun()
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Numeric columns statistics
        numeric_cols = df.select_dtypes(include=['number']).columns

        if len(numeric_cols) > 0:
            st.markdown("### 📊 Descriptive Statistics")
            st.dataframe(df[numeric_cols].describe(), use_container_width=True)

            st.markdown("---")

            # Percentiles
            st.markdown("### 📉 Percentiles (90/95/99)")
            percentiles = df[numeric_cols].quantile([0.90, 0.95, 0.99])
            st.dataframe(percentiles, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_fraud_distribution():
    """Fraud distribution page - UPDATED: Works with uploaded dataset directly."""
    st.markdown("""
        <h1>🚨 Fraud Distribution</h1>
        <p style="color: #94a3b8;">Visualize fraud vs legitimate transactions</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Find fraud column - auto-detect
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'is_fraud']:
                fraud_col = col
                break

        if fraud_col:
            fraud_counts = df[fraud_col].value_counts().sort_index()

            col1, col2 = st.columns(2)

            with col1:
                # Pie chart
                labels = []
                for idx in fraud_counts.index:
                    if idx == 0 or idx == '0':
                        labels.append('Legitimate')
                    elif idx == 1 or idx == '1':
                        labels.append('Fraud')
                    else:
                        labels.append(f'Class {idx}')

                fig = px.pie(values=fraud_counts.values, names=labels,
                             title="Fraud Distribution",
                             color_discrete_sequence=['#10b981', '#ef4444'])
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Stats
                total = len(df)

                # Handle different encodings of fraud labels
                if 1 in fraud_counts.index:
                    fraud = fraud_counts.get(1, 0)
                elif '1' in fraud_counts.index:
                    fraud = fraud_counts.get('1', 0)
                else:
                    fraud = 0

                legit = total - fraud

                st.markdown(f"""
                <div style="background: rgba(21,31,46,0.9); border-radius: 12px; padding: 20px;">
                    <div style="color: #10b981; font-size: 24px; font-weight: 700;">{legit:,}</div>
                    <div style="color: #94a3b8;">Legitimate Transactions</div>
                    <div style="color: #ef4444; font-size: 24px; font-weight: 700; margin-top: 10px;">{fraud:,}</div>
                    <div style="color: #94a3b8;">Fraud Transactions</div>
                    <div style="color: #f59e0b; font-size: 18px; font-weight: 600; margin-top: 10px;">{(fraud/total*100):.2f}%</div>
                    <div style="color: #94a3b8;">Fraud Rate</div>
                </div>
                """, unsafe_allow_html=True)

            # Also show bar chart
            st.markdown("### 📊 Transaction Count by Class")
            fig2 = px.bar(x=labels, y=fraud_counts.values,
                          labels={'x': 'Class', 'y': 'Count'},
                          color=labels,
                          color_discrete_sequence=['#10b981', '#ef4444'])
            st.plotly_chart(fig2, use_container_width=True)

        else:
            st.info(
                "No fraud label column found in dataset. Looking for columns: 'Class', 'Fraud', 'IsFraud', 'Label', 'Is_Fraud'")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_risk_percentiles():
    """Risk percentiles page."""
    st.markdown("""
        <h1>📉 Risk Percentiles</h1>
        <p style="color: #94a3b8;">View risk score distribution at different percentile thresholds</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("analysis_results"):
        st.warning("Please run analysis first")
        return

    try:
        results = st.session_state["analysis_results"]

        if "fraud_analysis" in results and "risk_scores" in results["fraud_analysis"]:
            risk_scores = results["fraud_analysis"]["risk_scores"]

            st.markdown("### 🎯 Risk Score Percentiles")

            col1, col2, col3 = st.columns(3)

            with col1:
                p90 = risk_scores.get("percentile_90", 0)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(245,158,11,0.1), rgba(245,158,11,0.05)); 
                            border: 1px solid rgba(245,158,11,0.3); border-radius: 12px; padding: 20px; text-align: center;">
                    <div style="color: #f59e0b; font-size: 32px; font-weight: 700;">{p90:.2f}</div>
                    <div style="color: #94a3b8;">90th Percentile</div>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                p95 = risk_scores.get("percentile_95", 0)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.05)); 
                            border: 1px solid rgba(239,68,68,0.3); border-radius: 12px; padding: 20px; text-align: center;">
                    <div style="color: #ef4444; font-size: 32px; font-weight: 700;">{p95:.2f}</div>
                    <div style="color: #94a3b8;">95th Percentile</div>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                p99 = risk_scores.get("percentile_99", 0)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(220,38,38,0.1), rgba(220,38,38,0.05)); 
                            border: 1px solid rgba(220,38,38,0.3); border-radius: 12px; padding: 20px; text-align: center;">
                    <div style="color: #dc2626; font-size: 32px; font-weight: 700;">{p99:.2f}</div>
                    <div style="color: #94a3b8;">99th Percentile</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

            # Risk distribution
            if "risk_distribution" in risk_scores:
                st.markdown("### 📊 Risk Level Distribution")
                dist = risk_scores["risk_distribution"]
                dist_df = pd.DataFrame(list(dist.items()), columns=[
                                       "Risk Level", "Count"])
                fig = px.bar(dist_df, x="Risk Level", y="Count", color="Risk Level",
                             color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444', '#dc2626'])
                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_rule_based():
    """Rule-based detection page."""
    st.markdown("""
        <h1>⚖️ Rule-Based Detection</h1>
        <p style="color: #94a3b8;">Custom rules for fraud detection based on transaction patterns</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        st.markdown("### 🔍 Applied Rules")

        rules = [
            "High amount transactions (> 3 std deviations from mean)",
            "Unusual time patterns (transactions at odd hours)",
            "Multiple transactions in short time window",
            "Geographic anomalies"
        ]

        for i, rule in enumerate(rules, 1):
            st.markdown(f"""
            <div style="background: rgba(21,31,46,0.9); border-radius: 8px; padding: 12px; margin-bottom: 8px;">
                <span style="color: #00d4ff; font-weight: 600;">Rule {i}:</span> {rule}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Apply basic rules
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            # Simple rule: flag high amounts
            for col in ['Amount', 'amount', 'V1', 'V2', 'V3']:
                if col in df.columns:
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    threshold = mean_val + 3 * std_val
                    high_risk = df[df[col] > threshold]

                    st.markdown(
                        f"**{col}** - High risk (> 3σ): {len(high_risk)} transactions")

    except Exception as e:
        st.error(f"Error: {str(e)}")


def page_isolation_forest():
    """Isolation Forest page."""
    st.markdown("""
        <h1>🌲 Isolation Forest Detection</h1>
        <p style="color: #94a3b8;">Machine learning-based anomaly detection using Isolation Forest algorithm</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    st.info("Isolation Forest analysis requires scikit-learn. This module analyzes data for anomalies.")

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Simple anomaly scoring
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()

        if len(numeric_cols) > 0:
            st.markdown("### 📊 Anomaly Scores")

            # Calculate z-scores for each numeric column
            from sklearn.ensemble import IsolationForest
            from sklearn.preprocessing import StandardScaler

            # Prepare data
            X = df[numeric_cols].fillna(0)
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            # Fit Isolation Forest
            iso = IsolationForest(contamination=0.1, random_state=42)
            predictions = iso.fit_predict(X_scaled)
            scores = iso.decision_function(X_scaled)

            # Results
            anomalies = (predictions == -1).sum()
            st.metric("Detected Anomalies", f"{anomalies:,}")

            # Distribution
            fig = px.histogram(x=scores, nbins=50, title="Anomaly Score Distribution",
                               labels={"x": "Anomaly Score", "y": "Count"})
            fig.add_vline(x=0, line_dash="dash", line_color="red")
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"ML analysis not available: {str(e)}")


def page_ml_results():
    """ML Results page."""
    st.markdown("""
        <h1>🤖 Machine Learning Results</h1>
        <p style="color: #94a3b8;">Results from various ML models for fraud detection</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    st.info("ML model training and evaluation")

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        # Find fraud column
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label']:
                fraud_col = col
                break

        if fraud_col and df[fraud_col].nunique() == 2:
            # Binary classification
            from sklearn.model_selection import train_test_split
            from sklearn.linear_model import LogisticRegression
            from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

            numeric_cols = df.select_dtypes(
                include=['number']).columns.tolist()
            numeric_cols = [c for c in numeric_cols if c != fraud_col]

            if len(numeric_cols) > 0:
                X = df[numeric_cols].fillna(0)
                y = df[fraud_col]

                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.2, random_state=42)

                # Train model
                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Metrics
                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, zero_division=0)
                rec = recall_score(y_test, y_pred, zero_division=0)
                f1 = f1_score(y_test, y_pred, zero_division=0)

                st.markdown("### 📊 Model Performance")

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Accuracy", f"{acc:.4f}")
                with col2:
                    st.metric("Precision", f"{prec:.4f}")
                with col3:
                    st.metric("Recall", f"{rec:.4f}")
                with col4:
                    st.metric("F1 Score", f"{f1:.4f}")
        else:
            st.info(
                "Dataset needs a binary 'Class' or 'Fraud' column for ML evaluation")

    except Exception as e:
        st.warning(f"ML analysis: {str(e)}")


def page_confusion_matrix():
    """Confusion Matrix page."""
    st.markdown("""
        <h1>📊 Confusion Matrix</h1>
        <p style="color: #94a3b8;">Visualize model performance with confusion matrix</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        st.markdown("### 📖 What is a Confusion Matrix?")
        st.markdown("""
        A confusion matrix shows the performance of a classification model:
        - **True Positive (TP):** Correctly predicted fraud
        - **True Negative (TN):** Correctly predicted legitimate
        - **False Positive (FP):** Legitimate predicted as fraud
        - **False Negative (FN):** Fraud predicted as legitimate
        """)

        st.markdown("---")

        # Generate sample confusion matrix
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label']:
                fraud_col = col
                break

        if fraud_col:
            from sklearn.metrics import confusion_matrix
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler

            numeric_cols = df.select_dtypes(
                include=['number']).columns.tolist()
            numeric_cols = [c for c in numeric_cols if c != fraud_col]

            if len(numeric_cols) > 0:
                X = df[numeric_cols].fillna(0)
                y = df[fraud_col]

                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                from sklearn.model_selection import train_test_split
                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.2, random_state=42)

                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                cm = confusion_matrix(y_test, y_pred)

                # Heatmap
                fig = px.imshow(cm, text_auto=True,
                                labels=dict(x="Predicted",
                                            y="Actual", color="Count"),
                                x=['Legitimate', 'Fraud'],
                                y=['Legitimate', 'Fraud'],
                                color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

                # Explanation
                tn, fp, fn, tp = cm.ravel()
                st.markdown(f"""
                **Results:**
                - True Negatives: {tn:,}
                - False Positives: {fp:,}
                - False Negatives: {fn:,}
                - True Positives: {tp:,}
                """)

    except Exception as e:
        st.warning(f"Confusion matrix: {str(e)}")


def page_precision_recall():
    """Precision-Recall page."""
    st.markdown("""
        <h1>📈 Precision-Recall Curve</h1>
        <p style="color: #94a3b8;">Understand the trade-off between precision and recall</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("### 📖 Understanding Precision vs Recall")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Precision**
        - Of all predicted frauds, how many are actually fraud?
        - High precision = fewer false alarms
        - Formula: TP / (TP + FP)
        """)

    with col2:
        st.markdown("""
        **Recall**
        - Of all actual frauds, how many did we catch?
        - High recall = missing fewer frauds
        - Formula: TP / (TP + FN)
        """)

    st.markdown("---")

    if not st.session_state.get("dataset_path"):
        st.warning("Please upload a dataset first")
        return

    try:
        df = pd.read_csv(st.session_state["dataset_path"])

        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label']:
                fraud_col = col
                break

        if fraud_col:
            from sklearn.metrics import precision_recall_curve, auc
            from sklearn.linear_model import LogisticRegression
            from sklearn.preprocessing import StandardScaler
            from sklearn.model_selection import train_test_split

            numeric_cols = df.select_dtypes(
                include=['number']).columns.tolist()
            numeric_cols = [c for c in numeric_cols if c != fraud_col]

            if len(numeric_cols) > 0:
                X = df[numeric_cols].fillna(0)
                y = df[fraud_col]

                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                X_train, X_test, y_train, y_test = train_test_split(
                    X_scaled, y, test_size=0.2, random_state=42)

                model = LogisticRegression(max_iter=1000)
                model.fit(X_train, y_train)
                y_proba = model.predict_proba(X_test)[:, 1]

                precision, recall, thresholds = precision_recall_curve(
                    y_test, y_proba)
                pr_auc = auc(recall, precision)

                # Plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=recall, y=precision,
                              mode='lines', name=f'PR Curve (AUC={pr_auc:.3f})'))
                fig.add_trace(go.Scatter(
                    x=[0, 1], y=[1, 0], mode='lines', name='Random', line=dict(dash='dash')))

                fig.update_layout(
                    title="Precision-Recall Curve",
                    xaxis_title="Recall",
                    yaxis_title="Precision",
                    legend=dict(x=0, y=1)
                )

                st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.warning(f"Precision-Recall: {str(e)}")


def page_reports():
    """Reports page."""
    st.markdown("""
        <h1>📑 Generate Reports</h1>
        <p style="color: #94a3b8;">Download comprehensive fraud detection reports</p>
    """, unsafe_allow_html=True)
    st.markdown("---")

    # Check if we have either analysis results or dataset path
    has_analysis = st.session_state.get("analysis_results") is not None
    has_dataset = st.session_state.get("dataset_path") is not None

    if not has_analysis and not has_dataset:
        st.warning("Please upload a dataset first")
        return

    # If no analysis but has dataset, offer to run analysis or generate basic report
    if not has_analysis and has_dataset:
        st.info(
            "Run analysis first for comprehensive reports, or generate a basic report from the dataset.")

        if st.button("Run Analysis First", type="primary"):
            with st.spinner("Running analysis..."):
                try:
                    results = run_analysis(st.session_state["dataset_path"])
                    st.session_state["analysis_results"] = results
                    st.success("Analysis completed!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")

        st.markdown("---")
        st.markdown("### Or generate a basic report from the dataset:")

    # Use analysis results if available, otherwise build from dataset
    if has_analysis:
        results = st.session_state["analysis_results"]
    else:
        # Build basic stats from dataset
        results = {}
        try:
            df = pd.read_csv(st.session_state["dataset_path"])

            # Find fraud column
            fraud_col = None
            for col in df.columns:
                if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'is_fraud']:
                    fraud_col = col
                    break

            if fraud_col:
                fraud_count = df[fraud_col].sum() if df[fraud_col].dtype in [
                    'int64', 'float64'] else (df[fraud_col] == 1).sum()
                total_count = len(df)
                results = {
                    "total_transactions": total_count,
                    "fraud_transactions": int(fraud_count),
                    "non_fraud_transactions": int(total_count - fraud_count),
                    "fraud_percentage": float(fraud_count / total_count * 100),
                    "data_summary": {
                        "total_rows": total_count,
                        "total_columns": len(df.columns),
                        "numerical_columns": list(df.select_dtypes(include=['number']).columns)
                    }
                }
            else:
                results = {
                    "total_transactions": len(df),
                    "data_summary": {
                        "total_rows": len(df),
                        "total_columns": len(df.columns),
                        "numerical_columns": list(df.select_dtypes(include=['number']).columns)
                    }
                }
        except Exception as e:
            st.error(f"Error reading dataset: {str(e)}")
            return

    # Generate report
    st.markdown("### Generate New Report")

    col1, col2 = st.columns(2)

    with col1:
        report_format = st.selectbox("Format", ["PDF", "CSV", "TXT"])

    with col2:
        filename = st.text_input("Filename", "fraud_report")

    if st.button("Generate Report"):
        try:
            output_path = generate_report(
                results, format=report_format.lower())
            st.success(f"Report generated: {os.path.basename(output_path)}")

            # Download
            with open(output_path, "rb") as f:
                st.download_button(
                    label="Download Report",
                    data=f.read(),
                    file_name=os.path.basename(output_path),
                    mime="application/pdf" if report_format == "PDF" else "text/plain"
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.markdown("---")

    # Report info
    st.markdown("### Report Contents")
    st.markdown("""
    - Executive Summary
    - Dataset Overview
    - Fraud Statistics
    - Risk Score Analysis (if analysis run)
    - Risk Distribution (if analysis run)
    - Detailed Statistics (if analysis run)
    - Recommendations
    """)

# ==================== MAIN APP ====================


def main():
    """Main application."""
    render_sidebar()

    if not st.session_state["logged_in"]:
        # Show login/signup
        if st.session_state.get("show_signup", False):
            signup_page()
        else:
            login_page()
    else:
        # Route to current page
        page = st.session_state.get("current_page", "📊 Dashboard")

        if page == "📊 Dashboard":
            page_dashboard()
        elif page == "📤 Upload Dataset":
            page_upload()
        elif page == "📋 Dataset Overview":
            page_dataset_overview()
        elif page == "✅ Data Quality":
            page_data_quality()
        elif page == "📈 Statistics":
            page_statistics()
        elif page == "🚨 Fraud Distribution":
            page_fraud_distribution()
        elif page == "📉 Risk Percentiles":
            page_risk_percentiles()
        elif page == "⚖️ Rule-Based":
            page_rule_based()
        elif page == "🌲 Isolation Forest":
            page_isolation_forest()
        elif page == "🤖 ML Results":
            page_ml_results()
        elif page == "📊 Confusion Matrix":
            page_confusion_matrix()
        elif page == "📈 Precision-Recall":
            page_precision_recall()
        elif page == "📑 Reports":
            page_reports()


if __name__ == "__main__":
    main()
