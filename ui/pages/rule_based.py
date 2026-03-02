"""
ui/pages/rule_based.py
=====================
Rule-Based Detection page for the Fraud Detection System.
Displays rule-based fraud detection results.
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def rule_based_page():
    """
    Display the rule-based detection page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .rule-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="rule-title">📋 Rule-Based Fraud Detection</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Detect fraudulent transactions using predefined rules and thresholds.")
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

        # Define rules
        rules = []

        # Rule 1: High Amount
        if "Amount" in df.columns:
            rules.append({
                "rule": "High Amount Transaction",
                "description": "Transactions above $10,000",
                "column": "Amount",
                "condition": ">",
                "threshold": 10000,
                "risk_score": 40
            })

            rules.append({
                "rule": "Very High Amount Transaction",
                "description": "Transactions above $50,000",
                "column": "Amount",
                "condition": ">",
                "threshold": 50000,
                "risk_score": 60
            })

        # Rule 2: Unusual Time
        if "Time" in df.columns:
            rules.append({
                "rule": "Unusual Transaction Time",
                "description": "Transactions during night hours (12AM-5AM)",
                "column": "Time",
                "condition": "night",
                "threshold": None,
                "risk_score": 20
            })

        # Rule 3: Multiple rapid transactions (if we have multiple rows with same values)
        rules.append({
            "rule": "Duplicate Transaction Pattern",
            "description": "Duplicate or near-duplicate transactions",
            "column": "All",
            "condition": "duplicate",
            "threshold": None,
            "risk_score": 30
        })

        # Apply rules
        flagged_transactions = []
        rule_results = {}

        for rule in rules:
            rule_name = rule["rule"]
            risk_score = rule["risk_score"]

            if rule["condition"] == ">":
                # High amount rule
                flagged = df[df[rule["column"]] > rule["threshold"]].copy()
                flagged["flagged_by"] = rule_name
                flagged["rule_risk_score"] = risk_score
                flagged_transactions.append(flagged)
                rule_results[rule_name] = len(flagged)

            elif rule["condition"] == "night":
                # Night time rule (Time in seconds: 0-18000 = 0-5AM)
                if "Time" in df.columns:
                    flagged = df[(df["Time"] < 18000) | (
                        df["Time"] > 86400 - 18000)].copy()
                    flagged["flagged_by"] = rule_name
                    flagged["rule_risk_score"] = risk_score
                    flagged_transactions.append(flagged)
                    rule_results[rule_name] = len(flagged)

            elif rule["condition"] == "duplicate":
                # Duplicate rule
                dupes = df[df.duplicated(keep=False)].copy()
                dupes["flagged_by"] = rule_name
                dupes["rule_risk_score"] = risk_score
                flagged_transactions.append(dupes)
                rule_results[rule_name] = len(dupes)

        # Combine flagged transactions
        if flagged_transactions:
            flagged_df = pd.concat(flagged_transactions, ignore_index=True)
            flagged_df = flagged_df.drop_duplicates(
                subset=df.columns.tolist() if df.columns.tolist() else None)
        else:
            flagged_df = pd.DataFrame()

        # Display rules
        st.subheader("📜 Detection Rules")

        rules_df = pd.DataFrame(rules)
        st.dataframe(rules_df[["rule", "description", "risk_score"]],
                     use_container_width=True, hide_index=True)

        st.markdown("---")

        # Results summary
        st.subheader("📊 Rule-Based Detection Results")

        col1, col2 = st.columns(2)

        with col1:
            total_flagged = len(flagged_df) if not flagged_df.empty else 0
            st.metric("Total Flagged Transactions", f"{total_flagged:,}")

        with col2:
            total = len(df)
            flag_rate = (total_flagged / total * 100) if total > 0 else 0
            st.metric("Flag Rate", f"{flag_rate:.2f}%")

        st.markdown("---")

        # Rule breakdown
        st.subheader("🔍 Flagged by Rule")

        if rule_results:
            rule_results_df = pd.DataFrame([
                {"Rule": k, "Flagged Count": v} for k, v in rule_results.items()
            ])

            fig_bar = px.bar(
                rule_results_df,
                x="Rule",
                y="Flagged Count",
                title="Transactions Flagged by Each Rule",
                color="Flagged Count",
                color_continuous_scale=["#00d4ff", "#7b2cbf"]
            )
            fig_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

            st.markdown("---")

        # Show flagged transactions
        st.subheader("🚨 Flagged Transactions")

        if not flagged_df.empty:
            st.write(
                f"Showing top {min(50, len(flagged_df))} flagged transactions:")

            # Select relevant columns to display
            display_cols = df.columns.tolist()[:10]  # First 10 columns
            if "flagged_by" in flagged_df.columns:
                display_cols.append("flagged_by")
            if "rule_risk_score" in flagged_df.columns:
                display_cols.append("rule_risk_score")

            st.dataframe(flagged_df[display_cols].head(
                50), use_container_width=True)
        else:
            st.success("✅ No transactions flagged by rule-based detection!")

        st.markdown("---")

        # Risk assessment
        st.subheader("⚠️ Risk Assessment")

        if not flagged_df.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                high_risk = len(flagged_df[flagged_df.get(
                    "rule_risk_score", 0) >= 50]) if "rule_risk_score" in flagged_df.columns else 0
                st.metric("High Risk (Score ≥50)", f"{high_risk:,}")

            with col2:
                medium_risk = len(flagged_df[(flagged_df.get("rule_risk_score", 0) >= 30) & (
                    flagged_df.get("rule_risk_score", 0) < 50)]) if "rule_risk_score" in flagged_df.columns else 0
                st.metric("Medium Risk (30-49)", f"{medium_risk:,}")

            with col3:
                low_risk = len(flagged_df[flagged_df.get(
                    "rule_risk_score", 0) < 30]) if "rule_risk_score" in flagged_df.columns else 0
                st.metric("Low Risk (<30)", f"{low_risk:,}")

    except Exception as e:
        st.error(f"Error in rule-based detection: {str(e)}")


if __name__ == "__main__":
    rule_based_page()
