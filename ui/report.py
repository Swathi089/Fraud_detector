"""
ui/report.py
============
Report page for the Fraud Detection System.
Provides report generation and download functionality in multiple formats.
"""

from backend.report_generator import generate_report, get_available_reports
from ui.styles import inject_design_system
import datetime
import streamlit as st
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def report_page():
    """
    Display the report page with professional UI.
    """
    # Inject design system
    inject_design_system()

    # CSS
    st.markdown("""
        <style>
        .report-header { text-align: center; margin-bottom: 24px; }
        .report-title { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 8px; }
        .report-subtitle { color: #94a3b8; font-size: 14px; }
        .format-card { background: rgba(21, 31, 46, 0.95); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 16px; padding: 20px; text-align: center; transition: all 0.3s ease; }
        .format-card:hover { transform: translateY(-3px); border-color: #00d4ff; }
        .format-icon { font-size: 36px; margin-bottom: 10px; }
        .format-name { color: #fff; font-weight: 600; font-size: 16px; margin-bottom: 8px; }
        .format-desc { color: #94a3b8; font-size: 12px; }
        .report-item { background: rgba(21, 31, 46, 0.95); border: 1px solid rgba(0, 212, 255, 0.15); border-radius: 12px; padding: 16px; margin-bottom: 12px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="report-header">
            <h1 style="margin-bottom: 8px;">📑 Generate Reports</h1>
            <p class="report-subtitle">Generate professional fraud detection reports in PDF, CSV, or TXT format</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Check if analysis has been run
    if "analysis_results" not in st.session_state or not st.session_state.get("analysis_results"):
        st.warning("⚠️ No analysis results available. Please run analysis first.")

        if st.button("Go to Statistics"):
            st.rerun()

        return

    results = st.session_state["analysis_results"]

    # Report generation section
    st.subheader("📊 Generate New Report")

    # Report format selection
    col1, col2 = st.columns([1, 2])

    with col1:
        report_format = st.selectbox(
            "Select Report Format",
            ["PDF", "CSV", "TXT"],
            help="Choose the format for your report"
        )

    with col2:
        # Custom filename
        default_filename = f"fraud_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        custom_filename = st.text_input(
            "Custom Filename (optional)",
            value=default_filename,
            help="Enter a custom filename without extension"
        )

    st.markdown("---")

    # Report preview
    st.subheader("📋 Report Preview")

    with st.expander("View Report Content"):
        # Show summary of what will be in the report
        fraud_analysis = results.get("fraud_analysis", {})

        st.markdown("**Fraud Statistics:**")
        st.write(
            f"- Total Transactions: {fraud_analysis.get('total_transactions', 0):,}")
        st.write(
            f"- Fraud Transactions: {fraud_analysis.get('fraud_transactions', 0):,}")
        st.write(
            f"- Non-Fraud Transactions: {fraud_analysis.get('non_fraud_transactions', 0):,}")
        st.write(
            f"- Fraud Percentage: {fraud_analysis.get('fraud_percentage', 0):.2f}%")

        if "risk_scores" in fraud_analysis:
            st.markdown("**Risk Score Analysis:**")
            risk_scores = fraud_analysis["risk_scores"]
            st.write(
                f"- Average Risk Score: {risk_scores.get('average_risk_score', 0):.2f}")
            st.write(
                f"- Min Risk Score: {risk_scores.get('min_risk_score', 0):.2f}")
            st.write(
                f"- Max Risk Score: {risk_scores.get('max_risk_score', 0):.2f}")

            if "risk_distribution" in risk_scores:
                st.markdown("**Risk Level Distribution:**")
                for level, count in risk_scores["risk_distribution"].items():
                    st.write(f"- {level}: {count:,}")

    st.markdown("---")

    # Generate report button
    if st.button("🚀 Generate Report", type="primary", use_container_width=True):
        with st.spinner("Generating report..."):
            try:
                # Create reports directory if it doesn't exist
                os.makedirs("reports/generated", exist_ok=True)

                # Generate report
                output_path = f"reports/generated/{custom_filename}.{report_format.lower()}"
                generated_path = generate_report(
                    results, output_path, report_format.lower())

                st.success(f"✓ Report generated successfully!")

                # Show download button
                with open(generated_path, "rb") as f:
                    st.download_button(
                        label=f"📥 Download {report_format} Report",
                        data=f.read(),
                        file_name=os.path.basename(generated_path),
                        mime=get_mime_type(report_format)
                    )

            except Exception as e:
                st.error(f"Error generating report: {str(e)}")

    st.markdown("---")

    # Available reports section
    st.subheader("📁 Available Reports")

    try:
        reports = get_available_reports()

        if reports:
            for report in reports:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

                with col1:
                    st.write(f"📄 {report['filename']}")

                with col2:
                    st.write(f"{report['format'].upper()}")

                with col3:
                    st.write(f"{report['size'] / 1024:.1f} KB")

                with col4:
                    with open(report['path'], 'rb') as f:
                        st.download_button(
                            label="Download",
                            data=f.read(),
                            file_name=report['filename'],
                            mime=get_mime_type(report['format']),
                            key=f"download_{report['filename']}"
                        )

                st.markdown("---")
        else:
            st.info("No reports generated yet.")

    except Exception as e:
        st.error(f"Error loading reports: {str(e)}")

    # Report format information
    st.markdown("---")
    st.subheader("ℹ️ Report Formats")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        **PDF Reports**
        - Professional formatted documents
        - Includes tables and charts
        - Best for sharing and printing
        """)

    with col2:
        st.markdown("""
        **CSV Reports**
        - Tabular data format
        - Easy to import into Excel
        - Best for data analysis
        """)

    with col3:
        st.markdown("""
        **TXT Reports**
        - Plain text format
        - Lightweight and fast
        - Best for quick viewing
        """)


def get_mime_type(format_type: str) -> str:
    """
    Get MIME type for the given format.

    Args:
        format_type (str): Format type (pdf, csv, txt)

    Returns:
        str: MIME type
    """
    mime_types = {
        "pdf": "application/pdf",
        "csv": "text/csv",
        "txt": "text/plain"
    }
    return mime_types.get(format_type.lower(), "application/octet-stream")


if __name__ == "__main__":
    report_page()
