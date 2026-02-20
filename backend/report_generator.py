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

    Args:
        stats (dict): Statistics to include in the report
        output_path (str): Path to save the report
        format (str): Report format ("pdf", "csv", or "txt")

    Returns:
        str: Path to the generated report
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
    Generate a professional PDF report.

    Args:
        stats (dict): Statistics to include in the report
        output_path (str): Path to save the PDF report

    Returns:
        str: Path to the generated report
    """
    logger.info(f"Generating PDF report: {output_path}")

    # Create PDF document
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=30,
        alignment=1  # Center
    )
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#16213e'),
        spaceAfter=12,
        spaceBefore=20
    )
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=10
    )

    # Title
    title = Paragraph("Financial Fraud Detection Report", title_style)
    story.append(title)

    # Report generation date
    date_text = Paragraph(
        f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", normal_style)
    story.append(date_text)
    story.append(Spacer(1, 20))

    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))

    # Get fraud analysis data
    fraud_analysis = stats.get("fraud_analysis", {})
    fraud_stats = {
        "Total Transactions": fraud_analysis.get("total_transactions", 0),
        "Fraud Transactions": fraud_analysis.get("fraud_transactions", 0),
        "Non-Fraud Transactions": fraud_analysis.get("non_fraud_transactions", 0),
        "Fraud Percentage": f"{fraud_analysis.get('fraud_percentage', 0)}%"
    }

    # Summary table
    summary_data = [["Metric", "Value"]]
    for key, value in fraud_stats.items():
        summary_data.append([key, str(value)])

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

    # Risk Analysis
    if "risk_scores" in fraud_analysis:
        story.append(Paragraph("Risk Analysis", heading_style))

        risk_scores = fraud_analysis["risk_scores"]
        risk_data = [["Risk Metric", "Value"]]

        risk_data.append(["Average Risk Score", str(
            risk_scores.get("average_risk_score", 0))])
        risk_data.append(["Min Risk Score", str(
            risk_scores.get("min_risk_score", 0))])
        risk_data.append(["Max Risk Score", str(
            risk_scores.get("max_risk_score", 0))])

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
    if "risk_distribution" in fraud_analysis:
        story.append(Paragraph("Risk Level Distribution", heading_style))

        risk_dist = fraud_analysis["risk_distribution"]
        dist_data = [["Risk Level", "Count"]]

        for level, count in risk_dist.items():
            dist_data.append([level, str(count)])

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
    if "detailed_statistics" in fraud_analysis:
        story.append(Paragraph("Detailed Statistics", heading_style))

        detailed_stats = fraud_analysis["detailed_statistics"]

        if "fraud_amount" in detailed_stats:
            story.append(Paragraph("Fraud Transaction Amounts:", normal_style))
            fraud_amount = detailed_stats["fraud_amount"]
            amount_data = [
                ["Metric", "Value"],
                ["Average", f"${fraud_amount.get('average', 0):,.2f}"],
                ["Total", f"${fraud_amount.get('total', 0):,.2f}"],
                ["Min", f"${fraud_amount.get('min', 0):,.2f}"],
                ["Max", f"${fraud_amount.get('max', 0):,.2f}"]
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

    # Footer
    story.append(Spacer(1, 30))
    footer = Paragraph(
        "This report was automatically generated by the Financial Fraud Detection System.",
        normal_style
    )
    story.append(footer)

    # Build PDF
    doc.build(story)

    logger.info(f"PDF report generated successfully: {output_path}")
    return output_path


def generate_csv_report(stats: dict, output_path: str) -> str:
    """
    Generate a CSV report.

    Args:
        stats (dict): Statistics to include in the report
        output_path (str): Path to save the CSV report

    Returns:
        str: Path to the generated report
    """
    logger.info(f"Generating CSV report: {output_path}")

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Title
        writer.writerow(["Financial Fraud Detection Report"])
        writer.writerow(
            [f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
        writer.writerow([])

        # Fraud Statistics
        writer.writerow(["Fraud Statistics"])
        fraud_analysis = stats.get("fraud_analysis", {})

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
        if "risk_scores" in fraud_analysis:
            writer.writerow(["Risk Score Analysis"])
            risk_scores = fraud_analysis["risk_scores"]

            writer.writerow(["Metric", "Value"])
            writer.writerow(
                ["Average Risk Score", risk_scores.get("average_risk_score", 0)])
            writer.writerow(
                ["Min Risk Score", risk_scores.get("min_risk_score", 0)])
            writer.writerow(
                ["Max Risk Score", risk_scores.get("max_risk_score", 0)])
            writer.writerow([])

            # Risk Distribution
            if "risk_distribution" in risk_scores:
                writer.writerow(["Risk Level Distribution"])
                writer.writerow(["Risk Level", "Count"])
                for level, count in risk_scores["risk_distribution"].items():
                    writer.writerow([level, count])
                writer.writerow([])

        # Detailed Statistics
        if "detailed_statistics" in fraud_analysis:
            writer.writerow(["Detailed Statistics"])
            detailed = fraud_analysis["detailed_statistics"]

            if "fraud_amount" in detailed:
                writer.writerow(["Fraud Transaction Amounts"])
                fraud_amount = detailed["fraud_amount"]
                writer.writerow(["Metric", "Value"])
                writer.writerow(["Average", fraud_amount.get("average", 0)])
                writer.writerow(["Total", fraud_amount.get("total", 0)])
                writer.writerow(["Min", fraud_amount.get("min", 0)])
                writer.writerow(["Max", fraud_amount.get("max", 0)])

    logger.info(f"CSV report generated successfully: {output_path}")
    return output_path


def generate_txt_report(stats: dict, output_path: str) -> str:
    """
    Generate a plain text report.

    Args:
        stats (dict): Statistics to include in the report
        output_path (str): Path to save the TXT report

    Returns:
        str: Path to the generated report
    """
    logger.info(f"Generating TXT report: {output_path}")

    with open(output_path, 'w') as txtfile:
        # Title
        txtfile.write("=" * 60 + "\n")
        txtfile.write("    FINANCIAL FRAUD DETECTION REPORT\n")
        txtfile.write("=" * 60 + "\n\n")

        # Date
        txtfile.write(
            f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Fraud Statistics
        txtfile.write("-" * 60 + "\n")
        txtfile.write("FRAUD STATISTICS\n")
        txtfile.write("-" * 60 + "\n")

        fraud_analysis = stats.get("fraud_analysis", {})

        txtfile.write(
            f"Total Transactions:        {fraud_analysis.get('total_transactions', 0):,}\n")
        txtfile.write(
            f"Fraud Transactions:      {fraud_analysis.get('fraud_transactions', 0):,}\n")
        txtfile.write(
            f"Non-Fraud Transactions:  {fraud_analysis.get('non_fraud_transactions', 0):,}\n")
        txtfile.write(
            f"Fraud Percentage:         {fraud_analysis.get('fraud_percentage', 0):.2f}%\n\n")

        # Risk Scores
        if "risk_scores" in fraud_analysis:
            txtfile.write("-" * 60 + "\n")
            txtfile.write("RISK SCORE ANALYSIS\n")
            txtfile.write("-" * 60 + "\n")

            risk_scores = fraud_analysis["risk_scores"]

            txtfile.write(
                f"Average Risk Score:      {risk_scores.get('average_risk_score', 0):.2f}\n")
            txtfile.write(
                f"Min Risk Score:          {risk_scores.get('min_risk_score', 0):.2f}\n")
            txtfile.write(
                f"Max Risk Score:          {risk_scores.get('max_risk_score', 0):.2f}\n\n")

            # Risk Distribution
            if "risk_distribution" in risk_scores:
                txtfile.write("Risk Level Distribution:\n")
                for level, count in risk_scores["risk_distribution"].items():
                    txtfile.write(f"  {level:10s}: {count:,}\n")
                txtfile.write("\n")

        # Detailed Statistics
        if "detailed_statistics" in fraud_analysis:
            txtfile.write("-" * 60 + "\n")
            txtfile.write("DETAILED STATISTICS\n")
            txtfile.write("-" * 60 + "\n")

            detailed = fraud_analysis["detailed_statistics"]

            if "fraud_amount" in detailed:
                txtfile.write("Fraud Transaction Amounts:\n")
                fraud_amount = detailed["fraud_amount"]
                txtfile.write(
                    f"  Average: ${fraud_amount.get('average', 0):,.2f}\n")
                txtfile.write(
                    f"  Total:   ${fraud_amount.get('total', 0):,.2f}\n")
                txtfile.write(
                    f"  Min:     ${fraud_amount.get('min', 0):,.2f}\n")
                txtfile.write(
                    f"  Max:     ${fraud_amount.get('max', 0):,.2f}\n\n")

        # Footer
        txtfile.write("=" * 60 + "\n")
        txtfile.write("This report was automatically generated by the\n")
        txtfile.write("Financial Fraud Detection System.\n")
        txtfile.write("=" * 60 + "\n")

    logger.info(f"TXT report generated successfully: {output_path}")
    return output_path


def get_available_reports() -> List[dict]:
    """
    Get list of available reports in the reports directory.

    Returns:
        List[dict]: List of reports with metadata
    """
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
