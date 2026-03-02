"""
ui/statistics.py
================
Statistics page for the Fraud Detection System.
Provides fraud analysis, visualizations, and detailed statistics.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from backend.api import run_analysis
from ui.styles import inject_design_system
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def statistics_page():
    """
    Display the statistics page with professional UI.
    """
    # Inject design system
    inject_design_system()

    st.markdown("""
        <style>
        .stats-header { text-align: center; margin-bottom: 24px; }
        .stats-title { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
        .stats-subtitle { color: #94a3b8; font-size: 14px; }
        .chart-card { background: rgba(21, 31, 46, 0.95); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 16px; padding: 20px; }
        .section-title { font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="stats-header">
            <h1 style="margin-bottom: 8px;">📊 Fraud Statistics & Analytics</h1>
            <p class="stats-subtitle">View detailed fraud analysis and interactive visualizations</p>
        </div>
    """, unsafe_allow_html=True)

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
        fraud_analysis = results.get("fraud_analysis", {})

        # Summary metrics
        st.markdown("### 📈 Summary Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-label">Total Transactions</div>
                    <div class="metric-value">{fraud_analysis.get('total_transactions', 0):,}</div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">⚠️</div>
                    <div class="metric-label">Fraud Transactions</div>
                    <div class="metric-value" style="color: #ef4444 !important;">{fraud_analysis.get('fraud_transactions', 0):,}</div>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">✓</div>
                    <div class="metric-label">Non-Fraud Transactions</div>
                    <div class="metric-value" style="color: #10b981 !important;">{fraud_analysis.get('non_fraud_transactions', 0):,}</div>
                </div>
            """, unsafe_allow_html=True)

        with col4:
            avg_risk = fraud_analysis.get("risk_scores", {}).get(
                "average_risk_score", 0) if "risk_scores" in fraud_analysis else 0
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-icon">🎯</div>
                    <div class="metric-label">Average Risk Score</div>
                    <div class="metric-value" style="color: #00d4ff !important;">{avg_risk:.1f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Visualizations
        st.markdown("### 📊 Visualizations")

        # Row 1: Charts
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("**Fraud Distribution**")

            fraud_count = fraud_analysis.get("fraud_transactions", 0)
            non_fraud_count = fraud_analysis.get("non_fraud_transactions", 0)

            if fraud_count > 0 or non_fraud_count > 0:
                fig_pie = px.pie(
                    values=[fraud_count, non_fraud_count],
                    names=["Fraud", "Non-Fraud"],
                    title="Fraud vs Non-Fraud Transactions",
                    color_discrete_sequence=["#ef4444", "#10b981"],
                    hole=0.4
                )
                fig_pie.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font_color="white"
                )
                fig_pie.update_traces(textinfo='percent+label')
                st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("**Risk Level Distribution**")

            if "risk_scores" in fraud_analysis and "risk_distribution" in fraud_analysis["risk_scores"]:
                risk_dist = fraud_analysis["risk_scores"]["risk_distribution"]

                if risk_dist:
                    fig_donut = px.pie(
                        values=list(risk_dist.values()),
                        names=list(risk_dist.keys()),
                        title="Risk Level Breakdown",
                        color=list(risk_dist.keys()),
                        color_discrete_map={
                            "Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"},
                        hole=0.5
                    )
                    fig_donut.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white"
                    )
                    fig_donut.update_traces(textinfo='percent+label')
                    st.plotly_chart(fig_donut, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Row 2: Gauge and Amount comparison
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("**Average Risk Score Gauge**")

            if "risk_scores" in fraud_analysis:
                avg_risk = fraud_analysis["risk_scores"].get(
                    "average_risk_score", 0)

                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=avg_risk,
                    title={"text": "Risk Score", "font": {
                        "size": 18, "color": "white"}},
                    gauge={
                        "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "white"},
                        "bar": {"color": "#00d4ff"},
                        "bgcolor": "rgba(0,0,0,0)",
                        "borderwidth": 2,
                        "bordercolor": "rgba(0,212,255,0.3)",
                        "steps": [
                            {"range": [0, 30], "color": "#10b981"},
                            {"range": [30, 70], "color": "#f59e0b"},
                            {"range": [70, 100], "color": "#ef4444"}
                        ]
                    }
                ))
                fig_gauge.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    font_color="white",
                    height=280
                )
                st.plotly_chart(fig_gauge, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown("**Amount Comparison**")

            if "detailed_statistics" in fraud_analysis:
                detailed = fraud_analysis["detailed_statistics"]

                if "fraud_amount" in detailed and "non_fraud_amount" in detailed:
                    fraud_amount = detailed["fraud_amount"]
                    non_fraud_amount = detailed["non_fraud_amount"]

                    comparison_data = pd.DataFrame({
                        'Transaction Type': ['Fraud', 'Non-Fraud'],
                        'Average Amount': [fraud_amount.get('average', 0), non_fraud_amount.get('average', 0)]
                    })

                    fig_bar = px.bar(
                        comparison_data,
                        x='Transaction Type',
                        y='Average Amount',
                        title="Average Transaction Amount",
                        color='Transaction Type',
                        color_discrete_map={
                            'Fraud': '#ef4444', 'Non-Fraud': '#10b981'},
                        text='Average Amount'
                    )
                    fig_bar.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font_color="white",
                        yaxis_title="Amount ($)"
                    )
                    fig_bar.update_traces(
                        texttemplate='$%{text:,.2f}', textposition='outside')
                    st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Detailed Statistics
        st.markdown("### 📋 Detailed Statistics")

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

        # Amount statistics
        if "detailed_statistics" in fraud_analysis:
            detailed = fraud_analysis["detailed_statistics"]

            st.markdown("---")
            st.markdown("**Amount Statistics**")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                    <div class="glass-card">
                        <div style="font-weight: 600; color: #ef4444; margin-bottom: 12px;">Fraud Transactions</div>
                    </div>
                """, unsafe_allow_html=True)
                if "fraud_amount" in detailed:
                    fraud_amount = detailed["fraud_amount"]
                    st.write(
                        f"**Average:** ${fraud_amount.get('average', 0):,.2f}")
                    st.write(
                        f"**Total:** ${fraud_amount.get('total', 0):,.2f}")
                    st.write(f"**Min:** ${fraud_amount.get('min', 0):,.2f}")
                    st.write(f"**Max:** ${fraud_amount.get('max', 0):,.2f}")

            with col2:
                st.markdown("""
                    <div class="glass-card">
                        <div style="font-weight: 600; color: #10b981; margin-bottom: 12px;">Non-Fraud Transactions</div>
                    </div>
                """, unsafe_allow_html=True)
                if "non_fraud_amount" in detailed:
                    non_fraud_amount = detailed["non_fraud_amount"]
                    st.write(
                        f"**Average:** ${non_fraud_amount.get('average', 0):,.2f}")
                    st.write(
                        f"**Total:** ${non_fraud_amount.get('total', 0):,.2f}")
                    st.write(
                        f"**Min:** ${non_fraud_amount.get('min', 0):,.2f}")
                    st.write(
                        f"**Max:** ${non_fraud_amount.get('max', 0):,.2f}")

        # Export section
        st.markdown("---")
        st.markdown("### 💾 Export Data")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Export as CSV", use_container_width=True):
                try:
                    summary_data = {
                        "Metric": ["Total Transactions", "Fraud Transactions", "Non-Fraud Transactions", "Fraud Percentage", "Average Risk Score"],
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
