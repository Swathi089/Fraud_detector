"""
ui/pages/fraud_analysis.py
========================
Fraud Analysis page for the Fraud Detection System.
Displays fraud distribution charts and analysis.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def fraud_analysis_page():
    """
    Display the fraud analysis page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .fraud-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="fraud-title">🛡️ Fraud Distribution Analysis</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Analyze the distribution of fraudulent vs legitimate transactions.")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    try:
        # Load data
        df = pd.read_csv(st.session_state["dataset_path"])

        # Find fraud column
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'target']:
                fraud_col = col
                break

        if fraud_col is None:
            st.warning(
                "⚠️ No fraud label column found (Class/Fraud/Label). Generating simulated fraud data...")
            # Create simulated fraud labels based on Amount
            if "Amount" in df.columns:
                df["Class"] = (df["Amount"] > 200).astype(int)
                fraud_col = "Class"
            else:
                st.error("Cannot determine fraud labels without Amount column")
                return

        # Calculate fraud statistics
        total = len(df)
        fraud_count = df[fraud_col].sum()
        legit_count = total - fraud_count
        fraud_pct = (fraud_count / total) * 100
        legit_pct = (legit_count / total) * 100

        # Display summary metrics
        st.subheader("📊 Fraud Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Transactions", f"{total:,}")

        with col2:
            st.metric("Fraud Transactions", f"{fraud_count:,}",
                      delta=f"{fraud_pct:.2f}%", delta_color="inverse")

        with col3:
            st.metric("Legitimate Transactions",
                      f"{legit_count:,}", delta=f"{legit_pct:.2f}%")

        with col4:
            st.metric(
                "Fraud Ratio", f"1:{int(legit_count/fraud_count) if fraud_count > 0 else 'N/A'}")

        st.markdown("---")

        # Visualizations
        st.subheader("📈 Visualizations")

        # Row 1: Pie chart and bar chart
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Fraud vs Legitimate Distribution**")
            fig_pie = px.pie(
                values=[fraud_count, legit_count],
                names=["Fraud", "Legitimate"],
                title="Transaction Type Distribution",
                color_discrete_sequence=["#ff5252", "#00c853"],
                hole=0.4
            )
            fig_pie.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            fig_pie.update_traces(textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.markdown("**Transaction Count Comparison**")
            fig_bar = px.bar(
                x=["Fraud", "Legitimate"],
                y=[fraud_count, legit_count],
                title="Transaction Count by Type",
                color=["Fraud", "Legitimate"],
                color_discrete_sequence=["#ff5252", "#00c853"],
                text=[f"{fraud_count:,}", f"{legit_count:,}"]
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                yaxis_title="Count"
            )
            fig_bar.update_traces(textposition='outside')
            st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # Amount analysis
        if "Amount" in df.columns:
            st.subheader("💰 Amount Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Fraud Transaction Amounts**")
                fraud_amounts = df[df[fraud_col] ==
                                   1]["Amount"] if fraud_count > 0 else pd.Series()
                if len(fraud_amounts) > 0:
                    st.write(f"Average: ${fraud_amounts.mean():,.2f}")
                    st.write(f"Median: ${fraud_amounts.median():,.2f}")
                    st.write(f"Min: ${fraud_amounts.min():,.2f}")
                    st.write(f"Max: ${fraud_amounts.max():,.2f}")
                else:
                    st.write("No fraud transactions to analyze")

            with col2:
                st.markdown("**Legitimate Transaction Amounts**")
                legit_amounts = df[df[fraud_col] == 0]["Amount"]
                if len(legit_amounts) > 0:
                    st.write(f"Average: ${legit_amounts.mean():,.2f}")
                    st.write(f"Median: ${legit_amounts.median():,.2f}")
                    st.write(f"Min: ${legit_amounts.min():,.2f}")
                    st.write(f"Max: ${legit_amounts.max():,.2f}")
                else:
                    st.write("No legitimate transactions to analyze")

            st.markdown("---")

            # Amount distribution
            st.markdown("**Amount Distribution by Transaction Type**")

            fig_hist = px.histogram(
                df,
                x="Amount",
                color=fraud_col,
                title="Transaction Amount Distribution",
                color_discrete_sequence=["#00c853", "#ff5252"],
                nbins=50
            )
            fig_hist.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="Amount ($)",
                yaxis_title="Count",
                legend_title="Transaction Type"
            )
            fig_hist.update_traces(opacity=0.75)
            st.plotly_chart(fig_hist, use_container_width=True)

        # Time analysis
        if "Time" in df.columns:
            st.markdown("---")
            st.subheader("⏰ Time Analysis")

            fig_time = px.histogram(
                df,
                x="Time",
                color=fraud_col,
                title="Transaction Time Distribution",
                color_discrete_sequence=["#00c853", "#ff5252"],
                nbins=50
            )
            fig_time.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="Time (seconds)",
                yaxis_title="Count",
                legend_title="Transaction Type"
            )
            fig_time.update_traces(opacity=0.75)
            st.plotly_chart(fig_time, use_container_width=True)

        st.markdown("---")

        # Sample fraud transactions
        st.subheader("🚨 Sample Fraudulent Transactions")

        fraud_transactions = df[df[fraud_col] == 1].head(20)
        if len(fraud_transactions) > 0:
            st.dataframe(fraud_transactions, use_container_width=True)
        else:
            st.info("No fraudulent transactions in the dataset")

    except Exception as e:
        st.error(f"Error analyzing fraud: {str(e)}")


if __name__ == "__main__":
    fraud_analysis_page()
