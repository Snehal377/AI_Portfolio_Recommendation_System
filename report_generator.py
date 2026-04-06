from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

def generate_report(goal, recommendation, critique, allocation, filename="portfolio_report.pdf"):

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("AI Portfolio Recommendation Report", styles['Title']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"<b>Investment Goal:</b> {goal}", styles['Normal']))
    elements.append(Spacer(1,10))

    elements.append(Paragraph("<b>AI Portfolio Recommendation</b>", styles['Heading2']))
    elements.append(Paragraph(recommendation.replace("\n","<br/>"), styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph("<b>Portfolio Critique</b>", styles['Heading2']))
    elements.append(Paragraph(critique.replace("\n","<br/>"), styles['Normal']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph("<b>Asset Allocation</b>", styles['Heading2']))

    table_data = [["Asset", "Weight"]]

    for _, row in allocation.iterrows():
        table_data.append([row["Asset"], f"{round(row['Weight']*100,2)} %"])

    table = Table(table_data)

    elements.append(table)

    doc = SimpleDocTemplate(filename, pagesize=A4)

    doc.build(elements)

    return filename