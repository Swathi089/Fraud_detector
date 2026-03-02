"""
ui/upload.py
============
Upload page for the Fraud Detection System.
Provides file upload and dataset preview functionality.
"""

import pandas as pd
import streamlit as st
from backend.api import get_dataset_info
from ui.styles import inject_design_system
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Upload directory
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_page():
    """
    Display the upload page with professional UI.
    """
    # Inject design system
    inject_design_system()

    # CSS
    st.markdown("""
        <style>
        .upload-header { text-align: center; margin-bottom: 24px; }
        .upload-title { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
        .upload-subtitle { color: #94a3b8; font-size: 14px; }
        .upload-success { background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px; margin: 16px 0; }
        .metric-box { background: rgba(21, 31, 46, 0.95); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 12px; padding: 16px; text-align: center; }
        .metric-value { color: #00d4ff; font-size: 24px; font-weight: 700; }
        .metric-label { color: #94a3b8; font-size: 12px; margin-top: 4px; }
        .sample-card { background: rgba(21, 31, 46, 0.95); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 16px; padding: 24px; text-align: center; transition: all 0.3s ease; }
        .sample-card:hover { border-color: #00d4ff; transform: translateY(-3px); }
        .sample-icon { font-size: 48px; margin-bottom: 12px; }
        .sample-title { color: #ffffff; font-weight: 600; font-size: 16px; margin-bottom: 8px; }
        .sample-desc { color: #94a3b8; font-size: 13px; margin-bottom: 16px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="upload-header">
            <h1 style="margin-bottom: 8px;">📤 Upload Dataset</h1>
            <p class="upload-subtitle">Upload your transaction data in CSV format for fraud analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file containing transaction data"
    )

    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state["dataset_path"] = file_path

        st.markdown(f"""
            <div class="upload-success">
                <span>✅</span> <strong>File uploaded successfully:</strong> {uploaded_file.name}
            </div>
        """, unsafe_allow_html=True)

        try:
            df_preview = pd.read_csv(file_path, nrows=10)
            st.markdown("### 📊 Dataset Preview")
            st.dataframe(df_preview, use_container_width=True)
            st.markdown("---")

            st.markdown("### ℹ️ Dataset Information")
            df_full = pd.read_csv(file_path)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{len(df_full):,}</div>
                        <div class="metric-label">Total Rows</div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{len(df_full.columns)}</div>
                        <div class="metric-label">Columns</div>
                    </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                    <div class="metric-box">
                        <div class="metric-value">{os.path.getsize(file_path)/1024:.1f} KB</div>
                        <div class="metric-label">File Size</div>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("**📋 Columns:**")
            columns_df = pd.DataFrame({
                "Column": df_full.columns,
                "Type": [str(df_full[c].dtype) for c in df_full.columns],
                "Non-Null": [df_full[c].count() for c in df_full.columns],
                "Null": [df_full[c].isnull().sum() for c in df_full.columns]
            })
            st.dataframe(columns_df, use_container_width=True)

            st.session_state["dataset_info"] = {
                "filename": uploaded_file.name,
                "path": file_path,
                "rows": len(df_full),
                "columns": len(df_full.columns),
                "column_names": list(df_full.columns)
            }

            st.markdown("---")
            st.markdown("### 🚀 Next Steps")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Go to Statistics", use_container_width=True):
                    st.rerun()
            with col2:
                if st.button("📑 Generate Report", use_container_width=True):
                    st.rerun()

        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    else:
        st.markdown("---")
        st.markdown("### 📁 Sample Dataset")

        sample_path = "data/creditcard.csv"
        if os.path.exists(sample_path):
            st.markdown("""
                <div class="sample-card">
                    <div class="sample-icon">📊</div>
                    <div class="sample-title">Credit Card Fraud Dataset</div>
                    <div class="sample-desc">Use our pre-loaded sample dataset for testing</div>
                </div>
            """, unsafe_allow_html=True)

            if st.button("Use Sample Data", use_container_width=True):
                st.session_state["dataset_path"] = sample_path
                st.success("Using sample dataset!")
                st.rerun()
        else:
            st.warning("No sample dataset found")

    # Current dataset section
    if "dataset_path" in st.session_state and st.session_state["dataset_path"]:
        st.markdown("---")
        st.markdown("### 📂 Current Dataset")
        current_path = st.session_state["dataset_path"]
        st.success(f"✓ Loaded: {os.path.basename(current_path)}")

        if st.button("Clear Dataset"):
            st.session_state["dataset_path"] = None
            st.session_state["analysis_results"] = None
            st.rerun()


if __name__ == "__main__":
    upload_page()
