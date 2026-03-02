"""
ui/pages/precision_recall.py
=========================
Precision-Recall page for the Fraud Detection System.
Displays precision-recall curve and explanation.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import precision_recall_curve, auc, average_precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def precision_recall_page():
    """
    Display the precision-recall page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .pr-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="pr-title">📈 Precision-Recall Analysis</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Understand the trade-offs between precision and recall in fraud detection.")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    # Generate predictions
    try:
        # Load data
        df = pd.read_csv(st.session_state["dataset_path"])

        # Find fraud column
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'target']:
                fraud_col = col
                break

        # Prepare features and labels
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        for col in ['Class', 'fraud', 'label', 'target']:
            if col in numeric_cols:
                numeric_cols.remove(col)

        if len(numeric_cols) < 2:
            st.error("Not enough numeric features")
            return

        X = df[numeric_cols].fillna(0)

        # Get or generate labels
        if fraud_col and fraud_col in df.columns:
            y_true = df[fraud_col]
        else:
            # Generate synthetic labels
            if "Amount" in df.columns:
                y_true = (df["Amount"] > df["Amount"].quantile(
                    0.95)).astype(int)
            else:
                y_true = np.random.randint(0, 2, len(df))

        # Scale and train model
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1)
        model.fit(X_scaled, y_true)

        # Get prediction probabilities
        y_scores = model.predict_proba(X_scaled)[:, 1]

        # Calculate precision-recall curve
        precision, recall, thresholds = precision_recall_curve(
            y_true, y_scores)
        pr_auc = auc(recall, precision)
        avg_precision = average_precision_score(y_true, y_scores)

        # Display metrics
        st.subheader("📊 Precision-Recall Metrics")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Average Precision (AP)", f"{avg_precision:.4f}",
                      help="Summary metric that combines precision and recall")

        with col2:
            st.metric("PR-AUC Score", f"{pr_auc:.4f}",
                      help="Area Under the Precision-Recall Curve")

        with col3:
            # Find optimal threshold
            f1_scores = 2 * (precision[:-1] * recall[:-1]) / \
                (precision[:-1] + recall[:-1] + 1e-10)
            optimal_idx = np.argmax(f1_scores)
            optimal_threshold = thresholds[optimal_idx]
            st.metric("Optimal Threshold", f"{optimal_threshold:.4f}",
                      help="Threshold that maximizes F1 score")

        st.markdown("---")

        # Precision-Recall Curve
        st.subheader("📈 Precision-Recall Curve")

        fig = go.Figure()

        # PR Curve
        fig.add_trace(go.Scatter(
            x=recall,
            y=precision,
            mode='lines',
            name=f'PR Curve (AUC = {pr_auc:.3f})',
            line=dict(color='#00d4ff', width=3)
        ))

        # Add baseline (random classifier)
        baseline = y_true.sum() / len(y_true)
        fig.add_trace(go.Scatter(
            x=[0, 1],
            y=[baseline, baseline],
            mode='lines',
            name=f'Random Baseline ({baseline:.3f})',
            line=dict(color='#ff5252', width=2, dash='dash')
        ))

        # Mark optimal point
        fig.add_trace(go.Scatter(
            x=[recall[optimal_idx]],
            y=[precision[optimal_idx]],
            mode='markers',
            name=f'Optimal (Threshold={optimal_threshold:.3f})',
            marker=dict(color='#00c853', size=15)
        ))

        fig.update_layout(
            title="Precision-Recall Curve",
            xaxis_title="Recall",
            yaxis_title="Precision",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Precision and Recall vs Threshold
        st.subheader("📊 Precision & Recall vs Threshold")

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=thresholds,
            y=precision[:-1],
            mode='lines',
            name='Precision',
            line=dict(color='#00d4ff', width=2)
        ))

        fig2.add_trace(go.Scatter(
            x=thresholds,
            y=recall[:-1],
            mode='lines',
            name='Recall',
            line=dict(color='#7b2cbf', width=2)
        ))

        fig2.add_trace(go.Scatter(
            x=thresholds,
            y=f1_scores,
            mode='lines',
            name='F1 Score',
            line=dict(color='#00c853', width=2)
        ))

        fig2.add_vline(
            x=optimal_threshold,
            line_dash="dash",
            line_color="#ffab00",
            annotation_text=f"Optimal: {optimal_threshold:.3f}"
        )

        fig2.update_layout(
            title="Precision, Recall, and F1 vs Classification Threshold",
            xaxis_title="Threshold",
            yaxis_title="Score",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")

        # Explanation
        st.subheader("💡 Understanding Precision-Recall")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **What is Precision?**
            - Precision measures how accurate your positive predictions are
            - Formula: TP / (TP + FP)
            - High precision = fewer false alarms
            - Example: "Of all transactions flagged as fraud, 80% were actually fraud"

            **What is Recall?**
            - Recall measures how many actual positives you capture
            - Formula: TP / (TP + FN)
            - High recall = fewer missed fraud cases
            - Example: "We caught 90% of all fraudulent transactions"
            """)

        with col2:
            st.markdown("""
            **Why is PR Curve Important?**
            - Unlike accuracy, PR curve works well with imbalanced data
            - Fraud detection datasets are typically highly imbalanced
            - Shows the trade-off between catching fraud and false alarms

            **Key Insights:**
            - The closer the curve is to the top-right corner, the better
            - Area Under the Curve (AUC) summarizes performance
            - Higher AUC = better model performance

            **Choosing a Threshold:**
            - Low threshold: More fraud flagged, lower precision, higher recall
            - High threshold: Fewer false alarms, higher precision, lower recall
            """)

        st.markdown("---")

        # Threshold selection guidance
        st.subheader("⚖️ Choosing the Right Threshold")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info("""
            **Low Threshold (e.g., 0.2)**
            - High recall: Catch more fraud
            - Lower precision: More false alarms
            - Use when: Missing fraud is very costly
            """)

        with col2:
            st.warning("""
            **Medium Threshold (e.g., 0.5)**
            - Balanced precision and recall
            - Good for general use
            - Use when: Need balanced approach
            """)

        with col3:
            st.error("""
            **High Threshold (e.g., 0.8)**
            - High precision: Fewer false alarms
            - Lower recall: Miss more fraud
            - Use when: Customer experience is priority
            """)

    except Exception as e:
        st.error(f"Error generating precision-recall analysis: {str(e)}")


if __name__ == "__main__":
    precision_recall_page()
