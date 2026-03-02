"""
backend/report_generator.py
===========================
Report generation module for the Fraud Detection System.
Generates professional reports in PDF, CSV, and TXT formats.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.units import inch
import csv
import datetime
import os
import logging
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Reports directory
REPORTS_DIR = "reports/generated"
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_report(stats: dict, output_path: str = None, format: str = "pdf") -> str:
    """
    Generate a fraud detection report.
    """
    logger.info(f"Generating {format.upper()} report")

    if output_path is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(
            REPORTS_DIR, f"fraud_report_{timestamp}.{format}")

    if format.lower() == "pdf":
        return generate_pdf_report(stats, output_path)
    elif format.lower() == "csv":
        return generate_csv_report(stats, output_path)
    elif format.lower() == "txt":
        return generate_txt_report(stats, output_path)
    else:
        logger.error(f"Unsupported format: {format}")
        raise ValueError(f"Unsupported format: {format}")


def generate_pdf_report(stats: dict, output_path: str) -> str:
    """
    Generate a professional PDF report with comprehensive fraud analysis.
    """
    logger.info(f"Generating PDF report: {output_path}")

    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24,
                                 textColor=colors.HexColor('#1a1a2e'), spaceAfter=30, alignment=1)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14,
                                   textColor=colors.HexColor('#16213e'), spaceAfter=12, spaceBefore=20)
    normal_style = ParagraphStyle(
        'CustomNormal', parent=styles['Normal'], fontSize=10, spaceAfter=10)

    # Title
    story.append(Paragraph("Financial Fraud Detection Report", title_style))
    story.append(Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style))
    story.append(Spacer(1, 20))

    # Get fraud_analysis - it contains the main results
    fraud_analysis = stats.get("fraud_analysis", {})

    # If fraud_analysis is empty, use stats directly
    if not fraud_analysis:
        fraud_analysis = stats

    logger.info(
        f"Fraud analysis keys: {fraud_analysis.keys() if isinstance(fraud_analysis, dict) else 'Not dict'}")

    # Extract values with proper fallbacks
    total_txn = fraud_analysis.get("total_transactions", 0)
    fraud_txn = fraud_analysis.get("fraud_transactions", 0)
    non_fraud_txn = fraud_analysis.get("non_fraud_transactions", 0)
    fraud_pct = fraud_analysis.get("fraud_percentage", 0)
    non_fraud_pct = fraud_analysis.get("non_fraud_percentage", 0)

    # If still 0, try from data_summary
    if total_txn == 0:
        data_summary = stats.get("data_summary", {})
        total_txn = data_summary.get("total_rows", 0)

    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))

    summary_data = [
        ["Metric", "Value"],
        ["Total Transactions", f"{total_txn:,}"],
        ["Fraud Transactions", f"{fraud_txn:,}"],
        ["Non-Fraud Transactions", f"{non_fraud_txn:,}"],
        ["Fraud Percentage", f"{fraud_pct}%"],
        ["Non-Fraud Percentage", f"{non_fraud_pct}%"]
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))

    # Risk Score Analysis
    risk_scores = fraud_analysis.get("risk_scores", {})
    if risk_scores:
        story.append(Paragraph("Risk Score Analysis", heading_style))

        avg_risk = risk_scores.get("average_risk_score", 0)
        min_risk = risk_scores.get("min_risk_score", 0)
        max_risk = risk_scores.get("max_risk_score", 0)
        std_risk = risk_scores.get("std_risk_score", 0)

        risk_data = [
            ["Metric", "Value"],
            ["Average Risk Score", f"{avg_risk:.2f}"],
            ["Minimum Risk Score", f"{min_risk:.2f}"],
            ["Maximum Risk Score", f"{max_risk:.2f}"],
            ["Std Deviation", f"{std_risk:.2f}"]
        ]

        risk_table = Table(risk_data, colWidths=[3*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e94560')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(risk_table)
        story.append(Spacer(1, 20))

    # Risk Distribution
    risk_dist = fraud_analysis.get("risk_distribution", {})
    if not risk_dist and risk_scores:
        risk_dist = risk_scores.get("risk_distribution", {})

    if risk_dist:
        story.append(Paragraph("Risk Level Distribution", heading_style))

        dist_data = [["Risk Level", "Count"]]
        for level, count in risk_dist.items():
            dist_data.append([level, f"{count:,}"])

        dist_table = Table(dist_data, colWidths=[3*inch, 2*inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dist_table)
        story.append(Spacer(1, 20))

    # Detailed Statistics
    detailed_stats = fraud_analysis.get("detailed_statistics", {})
    if detailed_stats:
        story.append(Paragraph("Detailed Transaction Analysis", heading_style))

        # Fraud Amount Statistics
        if "fraud_amount" in detailed_stats:
            story.append(Paragraph("Fraud Transaction Amounts:", normal_style))
            fraud_amount = detailed_stats["fraud_amount"]
            amount_data = [
                ["Metric", "Value"],
                ["Average", f"${fraud_amount.get('average', 0):,.2f}"],
                ["Total", f"${fraud_amount.get('total', 0):,.2f}"],
                ["Minimum", f"${fraud_amount.get('min', 0):,.2f}"],
                ["Maximum", f"${fraud_amount.get('max', 0):,.2f}"],
                ["Std Dev", f"${fraud_amount.get('std', 0):,.2f}"]
            ]

            amount_table = Table(amount_data, colWidths=[2*inch, 2*inch])
            amount_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e94560')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(amount_table)
            story.append(Spacer(1, 10))

        # Non-Fraud Amount Statistics
        if "non_fraud_amount" in detailed_stats:
            story.append(
                Paragraph("Non-Fraud Transaction Amounts:", normal_style))
            non_fraud_amount = detailed_stats["non_fraud_amount"]
            amount_data2 = [
                ["Metric", "Value"],
                ["Average", f"${non_fraud_amount.get('average', 0):,.2f}"],
                ["Total", f"${non_fraud_amount.get('total', 0):,.2f}"],
                ["Minimum", f"${non_fraud_amount.get('min', 0):,.2f}"],
                ["Maximum", f"${non_fraud_amount.get('max', 0):,.2f}"],
                ["Std Dev", f"${non_fraud_amount.get('std', 0):,.2f}"]
            ]

            amount_table2 = Table(amount_data2, colWidths=[2*inch, 2*inch])
            amount_table2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(amount_table2)
            story.append(Spacer(1, 10))

        # Time-based Statistics
        if "fraud_time" in detailed_stats:
            story.append(
                Paragraph("Fraud Transaction Time Patterns:", normal_style))
            fraud_time = detailed_stats["fraud_time"]
            time_data = [
                ["Metric", "Value (seconds)"],
                ["Average Time", f"{fraud_time.get('average', 0):,.2f}"],
                ["First Transaction", f"{fraud_time.get('min', 0):,.2f}"],
                ["Last Transaction", f"{fraud_time.get('max', 0):,.2f}"]
            ]

            time_table = Table(time_data, colWidths=[2*inch, 2*inch])
            time_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f59e0b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(time_table)
            story.append(Spacer(1, 10))

    # Dataset Overview Section
    data_summary = stats.get("data_summary", {})
    if data_summary:
        story.append(Paragraph("Dataset Overview", heading_style))

        total_cols = data_summary.get("total_columns", 0)
        num_cols = data_summary.get("numerical_columns", [])
        num_cols_count = len(num_cols) if isinstance(num_cols, list) else 0

        dataset_data = [
            ["Metric", "Value"],
            ["Total Rows", f"{data_summary.get('total_rows', 'N/A'):,}"],
            ["Total Columns", str(total_cols)],
            ["Numerical Columns", str(num_cols_count)]
        ]

        dataset_table = Table(dataset_data, colWidths=[3*inch, 2*inch])
        dataset_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f3460')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dataset_table)
        story.append(Spacer(1, 20))

    # Top Risky Transactions
    top_risky = fraud_analysis.get("top_risky_transactions", [])
    if top_risky and len(top_risky) > 0:
        story.append(Paragraph("Top Risky Transactions", heading_style))

        risky_data = [["#", "Risk Score", "Class"]]

        for i, txn in enumerate(top_risky[:5]):
            risk = txn.get("risk_score", "N/A")
            txn_class = txn.get("Class", "N/A")
            risky_data.append([str(i+1), str(risk), str(txn_class)])

        if len(risky_data) > 1:
            risky_table = Table(risky_data, colWidths=[
                                0.5*inch, 2*inch, 2*inch])
            risky_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(risky_table)
            story.append(Spacer(1, 20))

    # Recommendations Section
    story.append(Paragraph("Recommendations", heading_style))

    if fraud_pct > 1:
        recommendation_text = """
        Based on the analysis, the fraud rate is above 1%. Immediate action is recommended:
        <ul>
        <li>Implement stricter verification for high-value transactions</li>
        <li>Enable real-time fraud alerting system</li>
        <li>Review and update fraud detection rules</li>
        <li>Consider machine learning model retraining with recent data</li>
        <li>Increase monitoring frequency for suspicious accounts</li>
        </ul>
        """
    elif fraud_pct > 0.1:
        recommendation_text = """
        The fraud rate is moderate (0.1% - 1%). Recommended actions:
        <ul>
        <li>Continue monitoring transaction patterns</li>
        <li>Review flagged transactions weekly</li>
        <li>Update risk scoring thresholds periodically</li>
        <li>Maintain current fraud prevention measures</li>
        </ul>
        """
    else:
        recommendation_text = """
        The fraud rate is low. Continue with:
        <ul>
        <li>Regular monitoring and reporting</li>
        <li>Periodic model updates</li>
        <li>Maintain current fraud prevention measures</li>
        <li>Conduct periodic security audits</li>
        </ul>
        """

    story.append(Paragraph(recommendation_text, normal_style))

    # Footer
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        "This report was automatically generated by the Financial Fraud Detection System.", normal_style))

    # Build PDF
    doc.build(story)

    logger.info(f"PDF report generated successfully: {output_path}")
    return output_path


def generate_csv_report(stats: dict, output_path: str) -> str:
    """Generate a CSV report."""
    logger.info(f"Generating CSV report: {output_path}")

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Financial Fraud Detection Report"])
        writer.writerow(
            [f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        writer.writerow([])

        # Fraud Statistics
        writer.writerow(["Fraud Statistics"])
        fraud_analysis = stats.get("fraud_analysis", stats)

        writer.writerow(["Metric", "Value"])
        writer.writerow(
            ["Total Transactions", fraud_analysis.get("total_transactions", 0)])
        writer.writerow(
            ["Fraud Transactions", fraud_analysis.get("fraud_transactions", 0)])
        writer.writerow(["Non-Fraud Transactions",
                        fraud_analysis.get("non_fraud_transactions", 0)])
        writer.writerow(
            ["Fraud Percentage", f"{fraud_analysis.get('fraud_percentage', 0)}%"])
        writer.writerow([])

        # Risk Scores
        risk_scores = fraud_analysis.get("risk_scores", {})
        if risk_scores:
            writer.writerow(["Risk Score Analysis"])
            writer.writerow(["Metric", "Value"])
            writer.writerow(
                ["Average Risk Score", risk_scores.get("average_risk_score", 0)])
            writer.writerow(
                ["Min Risk Score", risk_scores.get("min_risk_score", 0)])
            writer.writerow(
                ["Max Risk Score", risk_scores.get("max_risk_score", 0)])
            writer.writerow([])

            risk_dist = risk_scores.get("risk_distribution", {})
            if risk_dist:
                writer.writerow(["Risk Level Distribution"])
                writer.writerow(["Risk Level", "Count"])
                for level, count in risk_dist.items():
                    writer.writerow([level, count])
                writer.writerow([])

        # Detailed Statistics
        detailed = fraud_analysis.get("detailed_statistics", {})
        if detailed:
            writer.writerow(["Detailed Statistics"])
            if "fraud_amount" in detailed:
                writer.writerow(["Fraud Amount"])
                writer.writerow(["Metric", "Value"])
                for key, val in detailed["fraud_amount"].items():
                    writer.writerow([key, val])

    logger.info(f"CSV report generated successfully: {output_path}")
    return output_path


def generate_txt_report(stats: dict, output_path: str) -> str:
    """Generate a plain text report."""
    logger.info(f"Generating TXT report: {output_path}")

    with open(output_path, 'w') as txtfile:
        txtfile.write("=" * 60 + "\n")
        txtfile.write("    FINANCIAL FRAUD DETECTION REPORT\n")
        txtfile.write("=" * 60 + "\n\n")
        txtfile.write(
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        fraud_analysis = stats.get("fraud_analysis", stats)

        txtfile.write("-" * 60 + "\n")
        txtfile.write("FRAUD STATISTICS\n")
        txtfile.write("-" * 60 + "\n")
        txtfile.write(
            f"Total Transactions:        {fraud_analysis.get('total_transactions', 0):,}\n")
        txtfile.write(
            f"Fraud Transactions:      {fraud_analysis.get('fraud_transactions', 0):,}\n")
        txtfile.write(
            f"Non-Fraud Transactions:  {fraud_analysis.get('non_fraud_transactions', 0):,}\n")
        txtfile.write(
            f"Fraud Percentage:         {fraud_analysis.get('fraud_percentage', 0):.2f}%\n\n")

        risk_scores = fraud_analysis.get("risk_scores", {})
        if risk_scores:
            txtfile.write("-" * 60 + "\n")
            txtfile.write("RISK SCORE ANALYSIS\n")
            txtfile.write("-" * 60 + "\n")
            txtfile.write(
                f"Average Risk Score:      {risk_scores.get('average_risk_score', 0):.2f}\n")
            txtfile.write(
                f"Min Risk Score:          {risk_scores.get('min_risk_score', 0):.2f}\n")
            txtfile.write(
                f"Max Risk Score:          {risk_scores.get('max_risk_score', 0):.2f}\n\n")

            risk_dist = risk_scores.get("risk_distribution", {})
            if risk_dist:
                txtfile.write("Risk Level Distribution:\n")
                for level, count in risk_dist.items():
                    txtfile.write(f"  {level:10s}: {count:,}\n")
                txtfile.write("\n")

        detailed = fraud_analysis.get("detailed_statistics", {})
        if detailed:
            txtfile.write("-" * 60 + "\n")
            txtfile.write("DETAILED STATISTICS\n")
            txtfile.write("-" * 60 + "\n")
            if "fraud_amount" in detailed:
                txtfile.write("Fraud Transaction Amounts:\n")
                for key, val in detailed["fraud_amount"].items():
                    txtfile.write(f"  {key}: ${val:,.2f}\n")
                txtfile.write("\n")

        txtfile.write("=" * 60 + "\n")
        txtfile.write("This report was automatically generated by the\n")
        txtfile.write("Financial Fraud Detection System.\n")
        txtfile.write("=" * 60 + "\n")

    logger.info(f"TXT report generated successfully: {output_path}")
    return output_path


def get_available_reports() -> List[dict]:
    """Get list of available reports in the reports directory."""
    reports = []

    if os.path.exists(REPORTS_DIR):
        for filename in os.listdir(REPORTS_DIR):
            if filename.endswith(('.pdf', '.csv', '.txt')):
                filepath = os.path.join(REPORTS_DIR, filename)
                stat = os.stat(filepath)

                reports.append({
                    "filename": filename,
                    "path": filepath,
                    "size": stat.st_size,
                    "created": datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                    "format": filename.split('.')[-1]
                })

    return sorted(reports, key=lambda x: x["created"], reverse=True)
