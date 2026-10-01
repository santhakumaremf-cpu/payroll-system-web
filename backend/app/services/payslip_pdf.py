"""Professional PDF Payslip Generator using ReportLab"""

from io import BytesIO
from datetime import datetime
from decimal import Decimal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
)
from reportlab.lib.enums import TA_CENTER


def money(val) -> str:
    try:
        return f"P{Decimal(str(val)):,.2f}"
    except Exception:
        return f"P{val}"


def generate_payslip_pdf(employee: dict, payslip: dict, period: dict = None, company_name: str = "Payroll System") -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="CompanyTitle", fontSize=16, fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=2, textColor=colors.HexColor("#1e3a5f")))
    styles.add(ParagraphStyle(name="Subtitle", fontSize=10, alignment=TA_CENTER, textColor=colors.HexColor("#64748b"), spaceAfter=8))
    styles.add(ParagraphStyle(name="SectionHeader", fontSize=11, fontName="Helvetica-Bold", textColor=colors.HexColor("#1e3a5f"), spaceBefore=10, spaceAfter=4))

    story = []
    story.append(Paragraph(company_name.upper(), styles["CompanyTitle"]))
    story.append(Paragraph("EMPLOYEE PAYSLIP", styles["Subtitle"]))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a5f"), spaceAfter=10))

    emp_name = f"{employee.get('last_name', '')}, {employee.get('first_name', '')} {employee.get('middle_name') or ''}".strip()
    period_str = f"{period.get('start_date', '')} to {period.get('end_date', '')}" if period else "-"

    info_data = [
        ["Employee No:", employee.get("employee_no", "-"), "Position:", employee.get("position_title", "-")],
        ["Name:", emp_name, "Status:", employee.get("employment_status", "-")],
        ["Period:", period_str, "Processed:", str(payslip.get("date_processed", ""))[:10]],
    ]
    info_table = Table(info_data, colWidths=[80, 170, 70, 140])
    info_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#475569")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#475569")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))

    story.append(Paragraph("EARNINGS", styles["SectionHeader"]))
    earnings_data = [["Description", "Amount"], ["Basic Pay", money(payslip.get("basic_pay", 0))], ["Overtime Pay", money(payslip.get("overtime_pay", 0))], ["Gross Pay", money(payslip.get("gross_pay", 0))]]
    earnings_table = Table(earnings_data, colWidths=[320, 140])
    earnings_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(earnings_table)

    story.append(Paragraph("DEDUCTIONS", styles["SectionHeader"]))
    ded_data = [["Description", "Amount"], ["SSS", money(payslip.get("sss", 0))], ["Pag-IBIG", money(payslip.get("pagibig", 0))], ["PhilHealth", money(payslip.get("philhealth", 0))], ["Other Deductions", money(payslip.get("other_deductions", 0))], ["Total Deductions", money(payslip.get("total_deductions", 0))]]
    ded_table = Table(ded_data, colWidths=[320, 140])
    ded_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.HexColor("#b91c1c")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#fef2f2")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(ded_table)

    story.append(Spacer(1, 12))
    summary_table = Table([["NET PAY", money(payslip.get("net_pay", 0))]], colWidths=[320, 140])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ecfdf5")),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 12),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#047857")),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor("#047857")),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(summary_table)

    story.append(Spacer(1, 14))
    story.append(Paragraph("ATTENDANCE SUMMARY", styles["SectionHeader"]))
    att_data = [
        ["Present Days", str(payslip.get("present_days", 0)), "OT Hours", str(payslip.get("overtime_hours", 0))],
        ["Late Hours", str(payslip.get("late_hours", 0)), "Absences", str(payslip.get("absences", 0))],
        ["Daily Rate", money(payslip.get("daily_rate", 0)), "", ""],
    ]
    att_table = Table(att_data, colWidths=[100, 130, 100, 130])
    att_table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#475569")),
        ("TEXTCOLOR", (2, 0), (2, -1), colors.HexColor("#475569")),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(att_table)

    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')} | Computer-generated payslip.",
        ParagraphStyle("Footer", fontSize=7, alignment=TA_CENTER, textColor=colors.HexColor("#94a3b8"))
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
