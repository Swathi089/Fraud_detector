"""
ui/pages/confusion_matrix.py
==========================
Confusion Matrix page for the Fraud Detection System.
Displays confusion matrix visualization and explanation.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def confusion_matrix_page():
    """
    Display the confusion matrix page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .cm-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="cm-title">🔢 Confusion Matrix</h1>',
                unsafe_allow_html=True)
    st.markdown("View the confusion matrix and model performance metrics.")
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
                "⚠️ No fraud label column found. Running ML model to generate predictions...")
            # Train a simple model to get predictions
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler

            numeric_cols = df.select_dtypes(
                include=[np.number]).columns.tolist()
            for col in ['Class', 'fraud', 'label', 'target']:
                if col in numeric_cols:
                    numeric_cols.remove(col)

            if len(numeric_cols) < 2:
                st.error("Not enough features for ML model")
                return

            X = df[numeric_cols].fillna(0)
            y = df[fraud_col] if fraud_col and fraud_col in df.columns else None

            if y is None:
                # Generate synthetic labels
                if "Amount" in df.columns:
                    y = (df["Amount"] > df["Amount"].quantile(0.95)).astype(int)
                else:
                    y = np.random.randint(0, 2, len(df))

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            model = RandomForestClassifier(
                n_estimators=100, random_state=42, n_jobs=-1)
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
            y_true = y
        else:
            # Use existing labels and generate predictions
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.preprocessing import StandardScaler

            numeric_cols = df.select_dtypes(
                include=[np.number]).columns.tolist()
            for col in ['Class', 'fraud', 'label', 'target']:
                if col in numeric_cols:
                    numeric_cols.remove(col)

            if len(numeric_cols) < 2:
                st.error("Not enough features for ML model")
                return

            X = df[numeric_cols].fillna(0)
            y_true = df[fraud_col]

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            model = RandomForestClassifier(
                n_estimators=100, random_state=42, n_jobs=-1)
            model.fit(X_scaled, y_true)
            y_pred = model.predict(X_scaled)

        # Calculate confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()

        # Display metrics
        st.subheader("📊 Confusion Matrix Values")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("True Negatives (TN)",
                      f"{tn:,}", help="Correctly identified as legitimate")

        with col2:
            st.metric("False Positives (FP)",
                      f"{fp:,}", help="Incorrectly flagged as fraud", delta_color="inverse")

        with col3:
            st.metric("False Negatives (FN)",
                      f"{fn:,}", help="Missed fraudulent transactions", delta_color="inverse")

        with col4:
            st.metric("True Positives (TP)",
                      f"{tp:,}", help="Correctly identified as fraud")

        st.markdown("---")

        # Confusion matrix heatmap
        st.subheader("🔢 Confusion Matrix Heatmap")

        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=cm,
            x=['Predicted Legit', 'Predicted Fraud'],
            y=['Actual Legit', 'Actual Fraud'],
            colorscale=[[0, '#00c853'], [1, '#ff5252']],
            text=cm,
            texttemplate="%{text}",
            textfont={"size": 20},
            showscale=False
        ))

        fig.update_layout(
            title="Confusion Matrix",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            width=600,
            height=500
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Performance metrics
        st.subheader("📈 Performance Metrics")

        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Accuracy", f"{accuracy:.4f}", help="(TP + TN) / Total")

        with col2:
            st.metric("Precision", f"{precision:.4f}", help="TP / (TP + FP)")

        with col3:
            st.metric("Recall", f"{recall:.4f}", help="TP / (TP + FN)")

        with col4:
            st.metric(
                "F1 Score", f"{f1:.4f}", help="2 * (Precision * Recall) / (Precision + Recall)")

        st.markdown("---")

        # Detailed explanation
        st.subheader("💡 Understanding the Metrics")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Accuracy**
            - The proportion of correct predictions (both fraud and legitimate)
            - Formula: (TP + TN) / Total
            - High accuracy means the model is good at identifying both classes

            **Precision**
            - The proportion of predicted frauds that are actually frauds
            - Formula: TP / (TP + FP)
            - High precision means fewer false alarms (legitimate flagged as fraud)

            **Recall (Sensitivity)**
            - The proportion of actual frauds that are correctly identified
            - Formula: TP / (TP + FN)
            - High recall means fewer missed fraudulent transactions
            """)

        with col2:
            st.markdown("""
            **F1 Score**
            - The harmonic mean of precision and recall
            - Formula: 2 * (Precision * Recall) / (Precision + Recall)
            - Best when you need a balance between precision and recall

            **Confusion Matrix Interpretation:**
            - **True Negative (TN):** Legitimate transaction correctly identified
            - **False Positive (FP):** Legitimate transaction wrongly flagged as fraud
            - **False Negative (FN):** Fraudulent transaction missed
            - **True Positive (TP):** Fraudulent transaction correctly caught
            """)

        st.markdown("---")

        # Trade-off explanation
        st.subheader("⚖️ Precision-Recall Trade-off")

        st.markdown("""
        In fraud detection, there's often a trade-off between **Precision** and **Recall**:

        - **High Precision, Low Recall:** Few false alarms but misses more fraud
          - Good for: Customer experience, reducing disruption
          
        - **Low Precision, High Recall:** Catches more fraud but has more false alarms
          - Good for: High-security scenarios where missing fraud is costly

        The **F1 Score** provides a balance between the two.
        """)

    except Exception as e:
        st.error(f"Error generating confusion matrix: {str(e)}")


if __name__ == "__main__":
    confusion_matrix_page()
