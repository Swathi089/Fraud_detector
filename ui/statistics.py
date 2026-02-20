"""
ui/statistics.py
================
Statistics page for the Fraud Detection System.
Provides fraud analysis, visualizations, and detailed statistics.
"""

from backend.api import run_analysis
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def statistics_page():
    """
    Display the statistics page with fraud analysis and visualizations.
    """
    st.title("📊 Fraud Statistics & Analytics")
    st.markdown("View detailed fraud analysis and interactive visualizations.")

    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")

        if st.button("Go to Upload"):
            st.rerun()

        return

    # Run analysis button
    if st.button("🔄 Run Analysis", type="primary"):
        with st.spinner("Running fraud analysis..."):
            try:
                results = run_analysis(st.session_state["dataset_path"])
                st.session_state["analysis_results"] = results
                st.success("✓ Analysis completed successfully!")
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

    # Display results if available
    if "analysis_results" in st.session_state and st.session_state["analysis_results"]:
        results = st.session_state["analysis_results"]

        # Get fraud analysis data
        fraud_analysis = results.get("fraud_analysis", {})

        # Display summary metrics
        st.subheader("📈 Summary Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Transactions",
                value=f"{fraud_analysis.get('total_transactions', 0):,}",
                delta=None
            )

        with col2:
            st.metric(
                label="Fraud Transactions",
                value=f"{fraud_analysis.get('fraud_transactions', 0):,}",
                delta=f"{fraud_analysis.get('fraud_percentage', 0):.2f}%",
                delta_color="inverse"
            )

        with col3:
            st.metric(
                label="Non-Fraud Transactions",
                value=f"{fraud_analysis.get('non_fraud_transactions', 0):,}",
                delta=None
            )

        with col4:
            if "risk_scores" in fraud_analysis:
                avg_risk = fraud_analysis["risk_scores"].get(
                    "average_risk_score", 0)
                st.metric(
                    label="Average Risk Score",
                    value=f"{avg_risk:.1f}",
                    delta=None
                )

        st.markdown("---")

        # Visualizations
        st.subheader("📊 Visualizations")

        # Fraud vs Non-Fraud pie chart
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Fraud Distribution**")

            # Create pie chart data
            fraud_count = fraud_analysis.get("fraud_transactions", 0)
            non_fraud_count = fraud_analysis.get("non_fraud_transactions", 0)

            if fraud_count > 0 or non_fraud_count > 0:
                fig_pie = px.pie(
                    values=[fraud_count, non_fraud_count],
                    names=["Fraud", "Non-Fraud"],
                    title="Fraud vs Non-Fraud Transactions",
                    color_discrete_sequence=["#e94560", "#16213e"]
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white"
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        # Risk distribution bar chart
        with col2:
            st.markdown("**Risk Level Distribution**")

            if "risk_scores" in fraud_analysis and "risk_distribution" in fraud_analysis["risk_scores"]:
                risk_dist = fraud_analysis["risk_scores"]["risk_distribution"]

                if risk_dist:
                    fig_bar = px.bar(
                        x=list(risk_dist.keys()),
                        y=list(risk_dist.values()),
                        title="Transactions by Risk Level",
                        color=list(risk_dist.keys()),
                        color_discrete_sequence=[
                            "#2ecc71", "#f39c12", "#e74c3c"]
                    )
                    fig_bar.update_layout(
                        xaxis_title="Risk Level",
                        yaxis_title="Count",
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # Detailed statistics
        st.subheader("📋 Detailed Statistics")

        # Risk score details
        if "risk_scores" in fraud_analysis:
            risk_scores = fraud_analysis["risk_scores"]

            st.markdown("**Risk Score Analysis**")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Min Risk Score",
                          f"{risk_scores.get('min_risk_score', 0):.1f}")

            with col2:
                st.metric("Max Risk Score",
                          f"{risk_scores.get('max_risk_score', 0):.1f}")

            with col3:
                st.metric("Avg Risk Score",
                          f"{risk_scores.get('average_risk_score', 0):.1f}")

            with col4:
                st.metric("Std Risk Score",
                          f"{risk_scores.get('std_risk_score', 0):.1f}")

        # Amount statistics for fraud vs non-fraud
        if "detailed_statistics" in fraud_analysis:
            detailed = fraud_analysis["detailed_statistics"]

            st.markdown("---")
            st.markdown("**Amount Statistics**")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("*Fraud Transactions*")
                if "fraud_amount" in detailed:
                    fraud_amount = detailed["fraud_amount"]
                    st.write(
                        f"Average: ${fraud_amount.get('average', 0):,.2f}")
                    st.write(f"Total: ${fraud_amount.get('total', 0):,.2f}")
                    st.write(f"Min: ${fraud_amount.get('min', 0):,.2f}")
                    st.write(f"Max: ${fraud_amount.get('max', 0):,.2f}")

            with col2:
                st.markdown("*Non-Fraud Transactions*")
                if "non_fraud_amount" in detailed:
                    non_fraud_amount = detailed["non_fraud_amount"]
                    st.write(
                        f"Average: ${non_fraud_amount.get('average', 0):,.2f}")
                    st.write(
                        f"Total: ${non_fraud_amount.get('total', 0):,.2f}")
                    st.write(f"Min: ${non_fraud_amount.get('min', 0):,.2f}")
                    st.write(f"Max: ${non_fraud_amount.get('max', 0):,.2f}")

        # Raw data expander
        with st.expander("📄 View Raw Analysis Results"):
            st.json(results)

        # Download data
        st.markdown("---")
        st.subheader("💾 Export Data")

        col1, col2 = st.columns(2)

        with col1:
            # Convert to CSV
            if st.button("Export as CSV", use_container_width=True):
                try:
                    # Create a summary dataframe
                    summary_data = {
                        "Metric": [
                            "Total Transactions",
                            "Fraud Transactions",
                            "Non-Fraud Transactions",
                            "Fraud Percentage",
                            "Average Risk Score"
                        ],
                        "Value": [
                            fraud_analysis.get("total_transactions", 0),
                            fraud_analysis.get("fraud_transactions", 0),
                            fraud_analysis.get("non_fraud_transactions", 0),
                            fraud_analysis.get("fraud_percentage", 0),
                            fraud_analysis.get("risk_scores", {}).get(
                                "average_risk_score", 0) if "risk_scores" in fraud_analysis else 0
                        ]
                    }
                    df_summary = pd.DataFrame(summary_data)

                    csv = df_summary.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name="fraud_analysis_summary.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error exporting CSV: {str(e)}")

        with col2:
            if st.button("📑 Go to Reports", use_container_width=True):
                st.rerun()

    else:
        st.info("Click 'Run Analysis' to generate fraud statistics.")


if __name__ == "__main__":
    statistics_page()
