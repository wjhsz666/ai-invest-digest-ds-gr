import os
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from history_service import get_latest_analysis

def export_pdf(company, analysis):

    os.makedirs("reports", exist_ok=True)

    filename = f"reports/{company}.pdf"

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    story.append(Paragraph("<b>AI Investment Lab</b>", styles["Heading1"]))

    story.append(Paragraph(f"Company: {company}", styles["Heading2"]))

    story.append(Paragraph("<br/><br/>", styles["Normal"]))

    story.append(Paragraph(analysis.replace("\n", "<br/>"), styles["BodyText"]))

    doc.build(story)

    return filename

def export_latest():

    data = get_latest_analysis("jack@test.com")

    if not data:
        return None

    company = data["company"]

    analysis = data["analysis_result"]

    return export_pdf(company, analysis)