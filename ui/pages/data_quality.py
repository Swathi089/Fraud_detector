"""
ui/pages/data_quality.py
=======================
Data Quality Report page for the Fraud Detection System.
Displays data quality metrics including missing values, duplicates, and invalid values.
"""

import pandas as pd
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def data_quality_page():
    """
    Display the data quality report page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .quality-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .quality-good { color: #00c853; }
        .quality-warning { color: #ffab00; }
        .quality-bad { color: #ff5252; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="quality-title">🔍 Data Quality Report</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Analyze data quality issues including missing values, duplicates, and invalid entries.")
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

        total_rows = len(df)
        total_cols = len(df.columns)

        # Overall quality score
        st.subheader("📊 Overall Data Quality")

        # Calculate quality metrics
        missing_total = df.isnull().sum().sum()
        missing_pct = (missing_total / (total_rows * total_cols)) * 100

        duplicates = df.duplicated().sum()
        dup_pct = (duplicates / total_rows) * 100

        # Quality score (simple calculation)
        quality_score = 100 - min(100, missing_pct * 2 + dup_pct)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if quality_score >= 80:
                st.metric(
                    "Quality Score", f"{quality_score:.1f}%", delta="Good", delta_color="normal")
            elif quality_score >= 60:
                st.metric(
                    "Quality Score", f"{quality_score:.1f}%", delta="Fair", delta_color="off")
            else:
                st.metric(
                    "Quality Score", f"{quality_score:.1f}%", delta="Poor", delta_color="inverse")

        with col2:
            st.metric("Missing Values", f"{missing_total:,}",
                      delta=f"{missing_pct:.2f}%", delta_color="inverse")

        with col3:
            st.metric("Duplicate Rows", f"{duplicates:,}",
                      delta=f"{dup_pct:.2f}%", delta_color="inverse")

        with col4:
            valid_rows = total_rows - \
                df.dropna().duplicated().sum() if df.dropna().duplicated().sum() > 0 else total_rows
            st.metric("Valid Rows", f"{valid_rows:,}",
                      delta=f"{(valid_rows/total_rows)*100:.1f}%")

        st.markdown("---")

        # Missing values analysis
        st.subheader("❌ Missing Values Analysis")

        missing_cols = df.isnull().sum()
        missing_cols = missing_cols[missing_cols >
                                    0].sort_values(ascending=False)

        if len(missing_cols) > 0:
            missing_df = pd.DataFrame({
                "Column": missing_cols.index,
                "Missing Count": missing_cols.values,
                "Missing %": [(v/total_rows)*100 for v in missing_cols.values]
            })
            st.dataframe(missing_df, use_container_width=True, hide_index=True)

            # Visual representation
            import plotly.express as px
            fig = px.bar(
                missing_df,
                x="Column",
                y="Missing %",
                title="Missing Values by Column",
                color="Missing %",
                color_continuous_scale=["#00c853", "#ffab00", "#ff5252"]
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("✅ No missing values found in the dataset!")

        st.markdown("---")

        # Duplicate analysis
        st.subheader("🔄 Duplicate Analysis")

        if duplicates > 0:
            st.warning(
                f"⚠️ Found {duplicates} duplicate rows ({(duplicates/total_rows)*100:.2f}%)")

            # Show duplicate examples
            dup_examples = df[df.duplicated(keep=False)].head(20)
            with st.expander("View Duplicate Rows"):
                st.dataframe(dup_examples, use_container_width=True)
        else:
            st.success("✅ No duplicate rows found!")

        st.markdown("---")

        # Invalid values analysis
        st.subheader("⚠️ Invalid Values Analysis")

        invalid_info = []

        # Check for negative values in Amount column
        if "Amount" in df.columns:
            neg_amount = (df["Amount"] < 0).sum()
            if neg_amount > 0:
                invalid_info.append(
                    {"Column": "Amount", "Issue": "Negative values", "Count": int(neg_amount)})

        # Check for invalid Class values (if exists)
        if "Class" in df.columns:
            invalid_class = (~df["Class"].isin([0, 1])).sum()
            if invalid_class > 0:
                invalid_info.append(
                    {"Column": "Class", "Issue": "Invalid class values (not 0 or 1)", "Count": int(invalid_class)})

        # Check for invalid Time values
        if "Time" in df.columns:
            neg_time = (df["Time"] < 0).sum()
            if neg_time > 0:
                invalid_info.append(
                    {"Column": "Time", "Issue": "Negative values", "Count": int(neg_time)})

        if len(invalid_info) > 0:
            invalid_df = pd.DataFrame(invalid_info)
            st.dataframe(invalid_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ No invalid values detected!")

        st.markdown("---")

        # Column-level quality
        st.subheader("📈 Column-Level Quality")

        col_quality = []
        for col in df.columns:
            null_pct = (df[col].isnull().sum() / total_rows) * 100
            unique_pct = (df[col].nunique() / total_rows) * 100

            # Determine quality status
            if null_pct == 0:
                status = "✅ Good"
            elif null_pct < 5:
                status = "⚠️ Fair"
            else:
                status = "❌ Poor"

            col_quality.append({
                "Column": col,
                "Missing %": f"{null_pct:.2f}%",
                "Unique %": f"{unique_pct:.2f}%",
                "Status": status
            })

        col_quality_df = pd.DataFrame(col_quality)
        st.dataframe(col_quality_df, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Recommendations
        st.subheader("💡 Recommendations")

        if missing_pct > 0:
            st.markdown(
                f"- Consider imputing missing values ({missing_pct:.2f}% of data)")

        if duplicates > 0:
            st.markdown(f"- Remove {duplicates} duplicate rows")

        if "Amount" in df.columns and (df["Amount"] < 0).sum() > 0:
            st.markdown("- Filter out negative Amount values")

        if "Time" in df.columns and (df["Time"] < 0).sum() > 0:
            st.markdown("- Filter out negative Time values")

        if quality_score >= 80:
            st.markdown("- Data quality is good for analysis!")
        else:
            st.markdown("- Consider data cleaning before analysis")

    except Exception as e:
        st.error(f"Error analyzing data quality: {str(e)}")


if __name__ == "__main__":
    data_quality_page()
