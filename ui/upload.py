"""
ui/upload.py
============
Upload page for the Fraud Detection System.
Provides file upload and dataset preview functionality.
"""

from backend.api import get_dataset_info
import streamlit as st
import sys
import os
import pandas as pd

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Upload directory
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def upload_page():
    """
    Display the upload page with file upload and preview.
    """
    st.title("📤 Upload Dataset")
    st.markdown("Upload your transaction data in CSV format for fraud analysis.")

    st.markdown("---")

    # File uploader
    st.subheader("Upload CSV File")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Upload a CSV file containing transaction data. The file should have columns like Time, Amount, Class, etc."
    )

    if uploaded_file is not None:
        # Save the file
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.session_state["dataset_path"] = file_path
        st.success(f"✓ File uploaded successfully: {uploaded_file.name}")

        st.markdown("---")

        # Dataset preview
        st.subheader("📊 Dataset Preview")

        try:
            # Read first few rows for preview
            df_preview = pd.read_csv(file_path, nrows=10)

            st.markdown(f"**First 10 rows of {uploaded_file.name}:**")
            st.dataframe(df_preview, use_container_width=True)

            # Dataset info
            st.markdown("---")
            st.subheader("ℹ️ Dataset Information")

            # Get full dataset info
            df_full = pd.read_csv(file_path)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Total Rows", f"{len(df_full):,}")

            with col2:
                st.metric("Total Columns", len(df_full.columns))

            with col3:
                st.metric(
                    "File Size", f"{os.path.getsize(file_path) / 1024:.1f} KB")

            # Column information
            st.markdown("**Columns:**")
            columns_df = pd.DataFrame({
                "Column": df_full.columns,
                "Type": [str(df_full[col].dtype) for col in df_full.columns],
                "Non-Null": [df_full[col].count() for col in df_full.columns],
                "Null": [df_full[col].isnull().sum() for col in df_full.columns]
            })
            st.dataframe(columns_df, use_container_width=True)

            # Store info in session state
            st.session_state["dataset_info"] = {
                "filename": uploaded_file.name,
                "path": file_path,
                "rows": len(df_full),
                "columns": len(df_full.columns),
                "column_names": list(df_full.columns)
            }

            st.markdown("---")

            # Proceed to analysis
            st.subheader("🚀 Next Steps")

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
        # Show sample data option
        st.markdown("---")
        st.subheader("📁 Sample Dataset")

        sample_path = "data/creditcard.csv"

        if os.path.exists(sample_path):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.info(f"Sample dataset available at: `{sample_path}`")

            with col2:
                if st.button("Use Sample Data", use_container_width=True):
                    st.session_state["dataset_path"] = sample_path
                    st.success("Using sample dataset!")
                    st.rerun()
        else:
            st.warning("No sample dataset found")

    # Show current dataset info
    if "dataset_path" in st.session_state and st.session_state["dataset_path"]:
        st.markdown("---")
        st.subheader("📂 Current Dataset")

        current_path = st.session_state["dataset_path"]
        st.success(f"✓ Loaded: {os.path.basename(current_path)}")

        if st.button("Clear Dataset"):
            st.session_state["dataset_path"] = None
            st.session_state["analysis_results"] = None
            st.rerun()


if __name__ == "__main__":
    upload_page()
