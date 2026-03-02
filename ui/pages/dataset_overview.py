"""
ui/pages/dataset_overview.py
===========================
Dataset Overview page for the Fraud Detection System.
Displays information about the uploaded dataset including rows, columns,
column types, and data preview.
"""

import pandas as pd
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def dataset_overview_page():
    """
    Display the dataset overview page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .overview-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .info-card { background: linear-gradient(135deg, rgba(21,31,46,0.9), rgba(27,38,59,0.9));
            border-radius: 16px; padding: 20px; border: 1px solid rgba(0,212,255,0.15); }
        .column-badge { background: rgba(0,212,255,0.15); border-radius: 8px; padding: 8px 16px;
            margin: 4px; display: inline-block; color: #00d4ff; font-size: 13px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="overview-title">📋 Dataset Overview</h1>',
                unsafe_allow_html=True)
    st.markdown("View detailed information about your uploaded dataset.")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    try:
        # Load dataset
        df = pd.read_csv(st.session_state["dataset_path"])

        # Basic info
        st.subheader("📊 Basic Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Rows", f"{len(df):,}")

        with col2:
            st.metric("Total Columns", f"{len(df.columns)}")

        with col3:
            st.metric(
                "File Size", f"{os.path.getsize(st.session_state['dataset_path'])/1024:.1f} KB")

        with col4:
            # Detect if fraud column exists
            fraud_col = None
            for col in df.columns:
                if col.lower() in ['class', 'fraud', 'isfraud', 'label']:
                    fraud_col = col
                    break
            st.metric("Fraud Column", fraud_col if fraud_col else "Not Found")

        st.markdown("---")

        # Dataset purpose detection
        st.subheader("🎯 Dataset Purpose")

        purpose = "Unknown"
        columns_lower = [c.lower() for c in df.columns]

        if any('credit' in c or 'card' in c for c in columns_lower):
            purpose = "Credit Card Transactions"
        elif any('bank' in c or 'transfer' in c for c in columns_lower):
            purpose = "Bank Transfer Data"
        elif any('amount' in c and 'time' in c for c in columns_lower):
            purpose = "Financial Transactions"

        st.info(f"📌 Detected Dataset Type: **{purpose}**")

        st.markdown("---")

        # Column information
        st.subheader("📝 Column Information")

        # Create column info dataframe
        col_info = []
        for col in df.columns:
            col_type = str(df[col].dtype)
            non_null = df[col].count()
            null_count = df[col].isnull().sum()
            unique_count = df[col].nunique()

            col_info.append({
                "Column": col,
                "Type": col_type,
                "Non-Null": non_null,
                "Null": null_count,
                "Unique": unique_count
            })

        col_info_df = pd.DataFrame(col_info)
        st.dataframe(col_info_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Data preview
        st.subheader("👀 Data Preview (First 10 Rows)")

        st.dataframe(df.head(10), use_container_width=True)

        # Show column names as badges
        st.markdown("---")
        st.subheader("🏷️ All Columns")

        cols = df.columns.tolist()
        for i in range(0, len(cols), 4):
            row_cols = cols[i:i+4]
            cols_html = " ".join(
                [f'<span class="column-badge">{c}</span>' for c in row_cols])
            st.markdown(cols_html, unsafe_allow_html=True)

        # Data types summary
        st.markdown("---")
        st.subheader("📈 Data Types Summary")

        type_counts = df.dtypes.value_counts()
        type_df = pd.DataFrame(
            {"Data Type": type_counts.index.astype(str), "Count": type_counts.values})
        st.dataframe(type_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")


if __name__ == "__main__":
    dataset_overview_page()
