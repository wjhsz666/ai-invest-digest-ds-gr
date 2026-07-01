import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet

from history_service import get_latest_analysis


def export_pdf(record):

    os.makedirs("reports", exist_ok=True)

    filename = (
        f"reports/"
        f"{record['company']}_{record['created_at'][:10]}.pdf"
    )

    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(filename)

    story = []

    # 标题
    story.append(
        Paragraph(
            "AI Investment Lab",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # 公司
    story.append(
        Paragraph(
            f"<b>Company：</b>{record['company']}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Score：</b>{record['score']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Revenue：</b>{record['revenue_grade']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Profit：</b>{record['profit_grade']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>Cash Flow：</b>{record['cashflow_grade']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    story.append(
        Paragraph(
            "<b>AI Analysis</b>",
            styles["Heading2"]
        )
    )

    analysis = record["analysis_result"].replace("\n", "<br/>")

    story.append(
        Paragraph(
            analysis,
            styles["BodyText"]
        )
    )

    doc.build(story)

    return filename

def download_latest_pdf():

    record = get_latest_analysis("jack@test.com")

    if not record:
        return None

    return export_pdf(record)
