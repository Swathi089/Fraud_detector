"""
ui/pages/isolation_forest.py
===========================
Isolation Forest Detection page for the Fraud Detection System.
Displays anomaly detection results using Isolation Forest algorithm.
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))


def isolation_forest_page():
    """
    Display the Isolation Forest detection page with professional UI.
    """
    # Professional CSS
    st.markdown("""
        <style>
        .iforest-title { font-size: 28px; font-weight: 700; color: #ffffff;
            background: linear-gradient(135deg, #00d4ff 0%, #7b2cbf 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="iforest-title">🌲 Isolation Forest Detection</h1>',
                unsafe_allow_html=True)
    st.markdown(
        "Detect fraudulent transactions using machine learning-based anomaly detection.")
    st.markdown("---")

    # Check if dataset is uploaded
    if "dataset_path" not in st.session_state or not st.session_state.get("dataset_path"):
        st.warning("⚠️ No dataset uploaded. Please upload a dataset first.")
        if st.button("Go to Upload"):
            st.rerun()
        return

    # Model settings
    st.sidebar.subheader("⚙️ Model Settings")

    contamination = st.sidebar.slider(
        "Contamination (expected fraud %)", 0.01, 0.20, 0.05, 0.01)
    n_estimators = st.sidebar.slider("Number of Trees", 50, 200, 100, 10)
    max_samples = st.sidebar.slider("Max Samples", 100, 1000, 256, 50)

    # Run detection button
    if st.button("🔍 Run Isolation Forest", type="primary"):
        with st.spinner("Running Isolation Forest anomaly detection..."):
            try:
                # Load data
                df = pd.read_csv(st.session_state["dataset_path"])

                # Prepare features
                numeric_cols = df.select_dtypes(
                    include=[np.number]).columns.tolist()

                # Remove target columns if they exist
                for col in ['Class', 'fraud', 'label', 'target']:
                    if col in numeric_cols:
                        numeric_cols.remove(col)

                if len(numeric_cols) < 2:
                    st.error("Not enough numeric features for Isolation Forest")
                    return

                # Prepare feature matrix
                X = df[numeric_cols].fillna(0)

                # Scale features
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)

                # Train Isolation Forest
                model = IsolationForest(
                    n_estimators=n_estimators,
                    contamination=contamination,
                    max_samples=max_samples,
                    random_state=42,
                    n_jobs=-1
                )

                # Fit and predict
                predictions = model.fit_predict(X_scaled)
                scores = model.decision_function(X_scaled)

                # Convert to -1 (fraud) and 1 (normal) to 1 (fraud) and 0 (normal)
                df['iforest_prediction'] = (predictions == -1).astype(int)
                # Negate so higher = more anomalous
                df['iforest_anomaly_score'] = -scores

                # Store results in session state (convert to list for proper serialization)
                st.session_state["iforest_results"] = {
                    "predictions": df['iforest_prediction'].tolist(),
                    "anomaly_scores": df['iforest_anomaly_score'].tolist(),
                    "feature_columns": numeric_cols
                }

                st.success("✅ Isolation Forest detection completed!")

            except Exception as e:
                st.error(f"Error running Isolation Forest: {str(e)}")

    # Display results if available
    if "iforest_results" in st.session_state and st.session_state.get("iforest_results"):
        results = st.session_state["iforest_results"]

        # Reload data to get full dataframe with predictions
        df = pd.read_csv(st.session_state["dataset_path"])
        df['iforest_prediction'] = results["predictions"]
        df['iforest_anomaly_score'] = results["anomaly_scores"]

        # Calculate statistics
        total = len(df)
        anomalies = df['iforest_prediction'].sum()
        normal = total - anomalies
        anomaly_pct = (anomalies / total) * 100

        # Display results
        st.subheader("📊 Isolation Forest Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Transactions", f"{total:,}")

        with col2:
            st.metric("Anomalies Detected", f"{anomalies:,}",
                      delta=f"{anomaly_pct:.2f}%", delta_color="inverse")

        with col3:
            st.metric("Normal Transactions", f"{normal:,}")

        with col4:
            avg_score = df['iforest_anomaly_score'].mean()
            st.metric("Avg Anomaly Score", f"{avg_score:.4f}")

        st.markdown("---")

        # Visualizations
        st.subheader("📈 Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Anomaly Distribution**")
            fig_pie = px.pie(
                values=[anomalies, normal],
                names=["Anomalies", "Normal"],
                title="Anomaly Detection Results",
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
            st.markdown("**Anomaly Score Distribution**")
            fig_hist = px.histogram(
                df,
                x="iforest_anomaly_score",
                nbins=50,
                title="Anomaly Score Distribution",
                color_discrete_sequence=["#00d4ff"]
            )
            fig_hist.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="white",
                xaxis_title="Anomaly Score",
                yaxis_title="Count"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        st.markdown("---")

        # Top anomalies
        st.subheader("🚨 Top Anomalies")

        top_anomalies = df[df['iforest_prediction'] ==
                           1].nlargest(20, 'iforest_anomaly_score')

        if len(top_anomalies) > 0:
            display_cols = results["feature_columns"][:5] if len(
                results["feature_columns"]) >= 5 else results["feature_columns"]
            display_cols = display_cols + ['iforest_anomaly_score']

            st.dataframe(top_anomalies[display_cols], use_container_width=True)

        st.markdown("---")

        # Compare with actual labels if available
        fraud_col = None
        for col in df.columns:
            if col.lower() in ['class', 'fraud', 'isfraud', 'label']:
                fraud_col = col
                break

        if fraud_col:
            st.subheader("📊 Comparison with Actual Labels")

            from sklearn.metrics import confusion_matrix, classification_report

            y_true = df[fraud_col]
            y_pred = df['iforest_prediction']

            # Calculate metrics
            tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("True Positives", f"{tp:,}")

            with col2:
                st.metric("True Negatives", f"{tn:,}")

            with col3:
                st.metric("False Positives", f"{fp:,}")

            with col4:
                st.metric("False Negatives", f"{fn:,}")

            st.markdown("---")

            accuracy = (tp + tn) / (tp + tn + fp + fn)
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (precision * recall) / (precision +
                                             recall) if (precision + recall) > 0 else 0

            st.write("**Classification Report:**")
            st.write(f"- Accuracy: {accuracy:.4f}")
            st.write(f"- Precision: {precision:.4f}")
            st.write(f"- Recall: {recall:.4f}")
            st.write(f"- F1 Score: {f1:.4f}")
    else:
        st.info("Click 'Run Isolation Forest' to detect anomalies in your dataset.")

    st.markdown("---")

    # Information about Isolation Forest
    st.subheader("💡 About Isolation Forest")

    st.markdown("""
    **Isolation Forest** is an unsupervised machine learning algorithm that detects anomalies by isolating observations in a dataset.
    
    **Key Concepts:**
    - The algorithm randomly selects a feature and then randomly selects a split value between the maximum and minimum values
    - Anomalies are easier to isolate (shorter path lengths) than normal points
    - The anomaly score is based on the average path length
    
    **Advantages:**
    - Works well with high-dimensional data
    - Efficient with large datasets
    - Does not require labeled data for training
    """)


if __name__ == "__main__":
    isolation_forest_page()
