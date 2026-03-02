





"""
ui/pages/ml_results.py
=====================
ML Results page for the Fraud Detection System.
Displays machine learning model results and evaluation.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, roc_curve
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def ml_results_page():
    """
    Display the ML results page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .ml-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="ml-title">🤖 Machine Learning Results</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Train and evaluate different machine learning models for fraud detection.")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    # Model selection
    st.sidebar.subheader("⚙️ Model Configuration")

    model_type = st.sidebar.selectbox(
        "Select Model",
        ["Random Forest", "Logistic Regression", "Gradient Boosting"]
    )

    test_size = st.sidebar.slider("Test Set Size", 0.1, 0.4, 0.2, 0.05)

    # Run model button
    if st.button("🚀 Train Model", type="primary"):
        with st.spinner("Training machine learning model..."):
            try:
                # Load data
                df = pd.read_csv(st.session_state["dataset_path"])

                # Find fraud column
                fraud_col = None
                for col in df.columns:
                    if col.lower() in ['class', 'fraud', 'isfraud', 'label', 'target']:
                        fraud_col = col
                        break

                # Prepare features
                numeric_cols = df.select_dtypes(
                    include=[np.number]).columns.tolist()
                for col in ['Class', 'fraud', 'label', 'target']:
                    if col in numeric_cols:
                        numeric_cols.remove(col)

                if len(numeric_cols) < 2:
                    st.error("Not enough numeric features for ML model")
                    return

                X = df[numeric_cols].fillna(0)

                # Get or generate labels
                if fraud_col and fraud_col in df.columns:
                    y = df[fraud_col]
                else:
                    if "Amount" in df.columns:
                        y = (df["Amount"] > df["Amount"].quantile(
                            0.95)).astype(int)
                    else:
                        y = np.random.randint(0, 2, len(df))

                # Split data (handle case where stratification is not possible)
                try:
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=42, stratify=y
                    )
                except ValueError:
                    # If stratification fails (e.g., only one class), do without stratify
                    X_train, X_test, y_train, y_test = train_test_split(
                        X, y, test_size=test_size, random_state=42
                    )

                # Scale features
                scaler = StandardScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)

                # Train model based on selection
                if model_type == "Random Forest":
                    model = RandomForestClassifier(
                        n_estimators=100, random_state=42, n_jobs=-1)
                elif model_type == "Logistic Regression":
                    model = LogisticRegression(max_iter=1000, random_state=42)
                elif model_type == "Gradient Boosting":
                    model = GradientBoostingClassifier(
                        n_estimators=100, random_state=42)

                model.fit(X_train_scaled, y_train)

                # Predictions
                y_pred = model.predict(X_test_scaled)
                y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]

                # Calculate metrics
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, zero_division=0)
                recall = recall_score(y_test, y_pred, zero_division=0)
                f1 = f1_score(y_test, y_pred, zero_division=0)
                roc_auc = roc_auc_score(y_test, y_pred_proba)

                # Store results (convert to list for proper serialization)
                st.session_state["ml_results"] = {
                    "model_name": model_type,
                    "accuracy": accuracy,
                    "precision": precision,
                    "recall": recall,
                    "f1": f1,
                    "roc_auc": roc_auc,
                    "y_test": y_test.tolist(),
                    "y_pred": y_pred.tolist(),
                    "y_pred_proba": y_pred_proba.tolist(),
                    "feature_columns": numeric_cols
                }

                st.success(f"✅ {model_type} training completed!")

            except Exception as e:
                st.error(f"Error training model: {str(e)}")

    # Display results
    if "ml_results" in st.session_state and st.session_state.get("ml_results"):
        results = st.session_state["ml_results"]

        st.subheader(f"📊 {results['model_name']} Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Accuracy", f"{results['accuracy']:.4f}")

        with col2:
            st.metric("Precision", f"{results['precision']:.4f}")

        with col3:
            st.metric("Recall", f"{results['recall']:.4f}")

        with col4:
            st.metric("F1 Score", f"{results['f1']:.4f}")

        st.markdown("---")

        # ROC Curve
        st.subheader("📈 ROC Curve")

        fpr, tpr, _ = roc_curve(results['y_test'], results['y_pred_proba'])

        fig_roc = go.Figure()

        fig_roc.add_trace(go.Scatter(
            x=fpr,
            y=tpr,
            mode='lines',
            name=f'ROC Curve (AUC = {results["roc_auc"]:.3f})',
            line=dict(color='#00d4ff', width=3)
        ))

        fig_roc.add_trace(go.Scatter(
            x=[0, 1],
            y=[0, 1],
            mode='lines',
            name='Random Classifier',
            line=dict(color='#ff5252', width=2, dash='dash')
        ))

        fig_roc.update_layout(
            title="Receiver Operating Characteristic (ROC) Curve",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white"
        )

        st.plotly_chart(fig_roc, use_container_width=True)

        st.markdown("---")

        # Model comparison
        st.subheader("📊 Model Metrics Comparison")

        metrics_df = pd.DataFrame({
            "Metric": ["Accuracy", "Precision", "Recall", "F1 Score", "ROC-AUC"],
            "Value": [
                results['accuracy'],
                results['precision'],
                results['recall'],
                results['f1'],
                results['roc_auc']
            ]
        })

        fig_bar = px.bar(
            metrics_df,
            x="Metric",
            y="Value",
            title=f"{results['model_name']} Performance Metrics",
            color="Value",
            color_continuous_scale=["#00d4ff", "#7b2cbf"]
        )

        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="white",
            yaxis=dict(range=[0, 1])
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        # Interpretation
        st.subheader("💡 Model Interpretation")

        st.markdown(f"""
        **Model: {results['model_name']}**

        - **Accuracy ({results['accuracy']:.2%}):** Overall correctness of the model
        - **Precision ({results['precision']:.2%}):** Of transactions predicted as fraud, how many are actually fraud
        - **Recall ({results['recall']:.2%}):** Of all actual fraud transactions, how many were correctly identified
        - **F1 Score ({results['f1']:.2%}):** Harmonic mean of precision and recall
        - **ROC-AUC ({results['roc_auc']:.2%}):** Ability to distinguish between fraud and legitimate transactions
        """)

        if results['recall'] < 0.5:
            st.warning(
                "⚠️ Low recall! The model might be missing too many fraudulent transactions. Consider:")
            st.markdown("- Reducing the classification threshold")
            st.markdown("- Using a model better suited for imbalanced data")
            st.markdown("- Collecting more training data")

        if results['precision'] < 0.5:
            st.warning("⚠️ Low precision! Too many false alarms. Consider:")
            st.markdown("- Increasing the classification threshold")
            st.markdown("- Using more features")
            st.markdown("- Feature engineering")

    else:
        st.info("Click 'Train Model' to train and evaluate a machine learning model.")

    st.markdown("---")

    # Model information
    st.subheader("💡 About the Models")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **Random Forest**
        - Ensemble of decision trees
        - Good for handling complex patterns
        - Less prone to overfitting
        - Works well with imbalanced data
        """)

    with col2:
        st.markdown("""
        **Logistic Regression**
        - Linear model for binary classification
        - Easy to interpret
        - Fast training
        - Works well when classes are linearly separable
        """)

    with col3:
        st.markdown("""
        **Gradient Boosting**
        - Sequential ensemble method
        - High predictive accuracy
        - Handles various data types
        - Can capture complex patterns
        """)


if __name__ == "__main__":
    ml_results_page()
