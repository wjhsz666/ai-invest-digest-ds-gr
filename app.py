from ai_service import (
    analyze,
    compare_companies,
    investment_thesis
)
import gradio as gr
from report_service import export_pdf
from pdf_service import read_pdf
from report_service import export_latest
from compare_service import compare_companies
from history_service import (
    get_history,
    get_analysis,
    get_dashboard,
    get_analysis_by_company
)


def show_history():

    history = get_history("jack@test.com")

    if not history:
        return "暂无分析记录"

    md = "# 📚 分析历史\n\n"

    for item in history:

        md += f"""
## 📄 {item['company']}

📅 {item['created_at'][:10]}

⭐ 评分：{item['score']}

---

"""

    return md


def load_history():

    history = get_history("jack@test.com")

    rows = []
    companies = []

    for item in history:

        rows.append([
            item["id"],
            item["company"],
            item["score"],
            item["revenue_grade"],
            item["profit_grade"],
            item["cashflow_grade"],
            item["created_at"][:10]
        ])

        companies.append(item["company"])

    return (
        rows,
        gr.update(choices=companies)
    )

def dashboard():
    data = get_dashboard("jack@test.com")

    md = f"""
# 📊 Dashboard

已分析公司：{data['total']}

平均评分：{data['avg_score']:.1f}

收入A级：{data['a_count']}

收入B级：{data['b_count']}

收入C级：{data['c_count']}
"""
    return md

def show_analysis(record_id):
    data = get_analysis(record_id)

    if not data:
        return "未找到记录"

    return data["analysis_result"]

def on_select(company):

    if not company:
        return ""

    data = get_analysis_by_company(company)

    if data:
        return data["analysis_result"]

    return "未找到分析结果"

# UI界面升级
with gr.Blocks(title="AI投研决策系统 Pro") as demo:

    gr.Markdown("# 🧠 AI投研决策系统 Pro")
    gr.Markdown("📊 上传财报 → AI评分 + 对比 + 投资建议")

    # =========================
    # 单公司分析
    # =========================
    gr.Markdown("## 📊 单公司分析")

    file_input = gr.File(label="上传财报PDF")
    with gr.Row():
        analyze_btn = gr.Button(
            "📊 生成评分报告",
            variant="primary"
        )

        download_btn = gr.Button(
            "📄 下载PDF"
        )
    analyze_output = gr.Textbox(
        label="评分报告",
        lines=18)
    pdf_file = gr.File(label="下载报告")
    analyze_btn.click(fn=analyze, inputs=file_input, outputs=analyze_output)
    download_btn.click(
        fn=export_latest,
        outputs=pdf_file
    )
    # =========================
    # 投资观点（新🔥）
    # =========================
    gr.Markdown("## 🧠 投资观点生成（研报级）")

    thesis_btn = gr.Button("🧠 生成投资观点", variant="secondary")
    thesis_output = gr.Textbox(
        label="投资观点",
        lines=18)

    thesis_btn.click(
        fn=lambda f: investment_thesis(read_pdf(f)),
        inputs=file_input,
        outputs=thesis_output
    )

    # =========================
    # 行业对比（已有）
    # =========================
    gr.Markdown("## ⚔️ 公司对比")

    file1 = gr.File(label="公司A财报PDF")

    file2 = gr.File(label="公司B财报PDF")

    compare_btn = gr.Button(
        "⚖️ AI开始比较",
        variant="primary"
    )

    compare_output = gr.Markdown()

    compare_btn.click(
        fn=compare_companies,
        inputs=[file1, file2],
        outputs=compare_output
    )

    with gr.Tab("📚 分析历史"):
        history_btn = gr.Button("刷新历史")

        history_table = gr.Dataframe(
            headers=[
                "ID",
                "公司",
                "评分",
                "收入",
                "利润",
                "现金流",
                "日期"
            ],
            interactive=False
        )
        company_dropdown = gr.Dropdown(
            label="选择历史记录",
            choices = []
        )

        analysis_view = gr.Markdown(
            label="AI分析结果"
        )

        history_btn.click(
            fn=load_history,
            outputs=[history_table, company_dropdown]
        )

        company_dropdown.change(
            fn=on_select,
            inputs=company_dropdown,
            outputs=analysis_view
        )

    with gr.Tab("📈 Dashboard"):
            refresh = gr.Button("刷新")

            dashboard_md = gr.Markdown()

            refresh.click(
                fn=dashboard,
                outputs=dashboard_md
            )
demo.launch(server_name="0.0.0.0", server_port=10000)
