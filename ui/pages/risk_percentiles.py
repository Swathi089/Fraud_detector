"""
ui/pages/risk_percentiles.py
==========================
Risk Percentiles page for the Fraud Detection System.
Displays risk percentiles at 90, 95, and 99 levels.
"""

import pandas as pd
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def risk_percentiles_page():
    """
    Display the risk percentiles page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .percentile-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="percentile-title">📊 Risk Percentiles</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "View risk score distributions at various percentile levels (90th, 95th, 99th).")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    # Check if analysis has been run
    if "analysis_results" not in st.session_state or not st.session_state.get("analysis_results"):
        st.warning("⚠️ No analysis results available. Please run analysis first.")
        if st.button("Go to Statistics"):
            st.rerun()
        return

    try:
        # Load data
        df = pd.read_csv(st.session_state["dataset_path"])

        # Calculate risk scores if not already in analysis
        if "risk_score" not in df.columns:
            # Simple risk calculation
            if "Amount" in df.columns:
                df["risk_score"] = 0
                # Amount-based risk
                df.loc[df["Amount"] > 10000,
                       "risk_score"] = df["risk_score"] + 40
                df.loc[(df["Amount"] > 5000) & (df["Amount"] <= 10000),
                       "risk_score"] = df["risk_score"] + 30
                df.loc[(df["Amount"] > 1000) & (df["Amount"] <= 5000),
                       "risk_score"] = df["risk_score"] + 20
                df.loc[(df["Amount"] > 500) & (df["Amount"] <= 1000),
                       "risk_score"] = df["risk_score"] + 10
                df.loc[df["Amount"] <= 500, "risk_score"] = df["risk_score"] + 5

                # Time-based risk (if available)
                if "Time" in df.columns:
                    df.loc[(df["Time"] < 3600) | (df["Time"] > 82800),
                           "risk_score"] = df["risk_score"] + 20
                    df.loc[~((df["Time"] < 3600) | (df["Time"] > 82800)),
                           "risk_score"] = df["risk_score"] + 10

                # Add random variation
                import numpy as np
                df["risk_score"] = df["risk_score"] + \
                    np.random.randint(0, 20, size=len(df))
                df["risk_score"] = df["risk_score"].clip(0, 100)

        # Calculate percentiles
        percentiles = [50, 75, 90, 95, 99]
        risk_percentile_values = {}

        for p in percentiles:
            risk_percentile_values[p] = df["risk_score"].quantile(p / 100)

        # Display percentiles
        st.subheader("📈 Risk Score Percentiles")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric("50th (Median)", f"{risk_percentile_values[50]:.1f}")

        with col2:
            st.metric("75th", f"{risk_percentile_values[75]:.1f}")

        with col3:
            st.metric("90th", f"{risk_percentile_values[90]:.1f}")

        with col4:
            st.metric("95th", f"{risk_percentile_values[95]:.1f}")

        with col5:
            st.metric("99th", f"{risk_percentile_values[99]:.1f}")

        st.markdown("---")

        # Percentile explanations
        st.subheader("💡 Percentile Explanations")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("""
            **90th Percentile**
            
            90% of transactions have a risk score at or below this value.
            
            Transactions above this threshold are in the top 10% of risk.
            """)

        with col2:
            st.warning("""
            **95th Percentile**
            
            95% of transactions have a risk score at or below this value.
            
            Transactions above this threshold are in the top 5% of risk.
            """)

        with col3:
            st.error("""
            **99th Percentile**
            
            99% of transactions have a risk score at or below this value.
            
            Transactions above this threshold are in the top 1% of risk (highest risk).
            """)

        st.markdown("---")

        # High risk transactions
        st.subheader("🚨 High Risk Transactions (Above 95th Percentile)")

        threshold_95 = risk_percentile_values[95]
        high_risk = df[df["risk_score"] >= threshold_95]

        st.write(f"Number of high-risk transactions: **{len(high_risk):,}**")

        if len(high_risk) > 0:
            st.dataframe(high_risk.head(20), use_container_width=True)

        st.markdown("---")

        # Risk distribution histogram
        st.subheader("📊 Risk Score Distribution")

        import plotly.express as px

        fig = px.histogram(
            df,
            x="risk_score",
            nbins=50,
            title="Risk Score Distribution",
            color_discrete_sequence=["#00d4ff"]
        )

        # Add percentile lines
        for p in [90, 95, 99]:
            fig.add_vline(
                x=risk_percentile_values[p],
                line_dash="dash",
                line_color="#ff5252",
                annotation_text=f"{p}th"
            )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            xaxis_title="Risk Score",
            yaxis_title="Count"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Summary table
        st.markdown("---")
        st.subheader("📋 Percentile Summary")

        summary_data = {
            "Percentile": ["50th (Median)", "75th", "90th", "95th", "99th"],
            "Risk Score": [f"{v:.1f}" for v in risk_percentile_values.values()],
            "Interpretation": [
                "Middle value - 50% below, 50% above",
                "Upper quartile - 75% below",
                "High risk threshold - 90% below",
                "Very high risk - 95% below",
                "Critical risk - 99% below"
            ]
        }

        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error calculating risk percentiles: {str(e)}")


if __name__ == "__main__":
    risk_percentiles_page()
