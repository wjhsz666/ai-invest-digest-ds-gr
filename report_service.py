import os

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from history_service import get_latest_analysis

# -----------------------------
# 注册中文字体
# -----------------------------

pdfmetrics.registerFont(
    TTFont(
        "Chinese",
        "fonts/NotoSansSC-Regular.ttf"
    )
)


def export_pdf(record):

    os.makedirs("reports", exist_ok=True)

    filename = (
        f"reports/"
        f"{record['company']}_{record['created_at'][:10]}.pdf"
    )

    styles = getSampleStyleSheet()

    # 全部改成中文字体
    styles["Title"].fontName = "Chinese"
    styles["Heading2"].fontName = "Chinese"
    styles["BodyText"].fontName = "Chinese"
    styles["Normal"].fontName = "Chinese"

    doc = SimpleDocTemplate(filename)

    story = []

    # ==========================================
    # 标题
    # ==========================================

    story.append(
        Paragraph(
            "AI Investment Lab 财报分析报告",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # 基本信息
    # ==========================================

    story.append(
        Paragraph(
            f"<b>公司：</b>{record['company']}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"<b>综合评分：</b>{record['score']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>收入质量：</b>{record['revenue_grade']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>利润质量：</b>{record['profit_grade']}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"<b>现金流质量：</b>{record['cashflow_grade']}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 20))

    # ==========================================
    # AI分析
    # ==========================================

    story.append(
        Paragraph(
            "AI分析结果",
            styles["Heading2"]
        )
    )

    analysis = record["analysis_result"]

    analysis = analysis.replace("\n", "<br/>")

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
