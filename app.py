from ai_service import (
    analyze,
    compare_companies,
    investment_thesis
)
import gradio as gr
from pdf_service import read_pdf
from auth_service import (
    sign_up,
    sign_in,
    sign_out
)
from history_service import (
    get_history,
    get_analysis,
    get_dashboard,
    get_analysis_by_company, get_latest_analysis
)
from report_service import download_latest_pdf, export_pdf
from usage_service import get_today_usage

user_state = None
def login(email, password):

    try:

        result = sign_in(email, password)

        user = result.user.email
        print(get_today_usage(email))
        return (
            f"✅ 登录成功：{user}",
            user      
        )

    except Exception as e:

        return (
            f"❌ {e}",
            None
        )


def register(email, password):

    try:
        sign_up(email, password)

        return "✅ 注册成功，请登录。"

    except Exception as e:
        return str(e)
def logout():

    sign_out()

    return (
        "👋 已退出登录",
        None
    )
def show_history():

    history = get_history(user_state)

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


def load_history(user):

    if user is None:
        return gr.update(choices=[], value=None)

    history = get_history(user)

    companies = [item["company"] for item in history]

    if len(companies) == 0:
        return gr.update(choices=[], value=None)

    return gr.update(
        choices=companies,
        value=companies[0]   # ✅ 必须选已有值
    )

def dashboard(user):

    if user is None:
        return "请先登录"

    data = get_dashboard(user)

    md = f"""
# 📊 Dashboard

📈 总分析次数：{data['total']}

⭐ 平均评分：{data['avg_score']:.1f}

🟢 收入A级：{data['a_count']}

🟡 收入B级：{data['b_count']}

🔴 收入C级：{data['c_count']}

---

## 🏆 Top 5 公司

"""

    for item in data["top5"]:
        md += f"• {item['company']}（{item['score']} 分）\n"

    md += "\n---\n## 🕒 最近分析\n"

    for item in data["recent"]:
        md += f"• {item['company']}（{item['score']} 分）\n"

    return md

def show_analysis(record_id):
    data = get_analysis(record_id)

    if not data:
        return "未找到记录"

    return data["analysis_result"]

def on_select(company, user):

    if user is None:
        return ""

    data = get_analysis_by_company(user, company)

    if data:
        return data["analysis_result"]

    return ""

def thesis_wrapper(file):

    if file is None:
        return "请先上传财报PDF"

    return investment_thesis(
        read_pdf(file)
    )

# UI界面升级
with gr.Blocks(
    title="AI投研决策系统 Pro",
    theme=gr.themes.Soft()
) as demo:
    user_state = gr.State(value=None)
    gr.Markdown("# 🧠 AI投研决策系统 Pro")
    gr.Markdown("📊 上传财报 → AI评分 + 对比 + 投资建议")
    with gr.Row():
        email_input = gr.Textbox(
            label="邮箱",
            scale=3
        )

        password_input = gr.Textbox(
            label="密码",
            type="password",
            scale=3
        )

    with gr.Row():
        login_btn = gr.Button(
            "登录",
            variant="primary"
        )

        register_btn = gr.Button("注册")

        logout_btn = gr.Button("退出")

    login_status = gr.Markdown(
        "🔒 当前状态：未登录"
    )
    gr.Markdown("---")
    # 再绑定
    login_btn.click(
        fn=login,
        inputs=[email_input, password_input],
        outputs=[
            login_status,
            user_state
        ]
    )

    register_btn.click(
        fn=register,
        inputs=[email_input, password_input],
        outputs=login_status    
    )

    logout_btn.click(
        fn=logout,
        outputs=[
            login_status,
            user_state
        ]
    )

    # =========================
    # 单公司分析
    # =========================
    gr.Markdown("""
    ## 📊 财报分析

    上传上市公司财报，生成 AI 健康评分及投资建议。
    """)

    file_input = gr.File(label="上传财报PDF")
    with gr.Row():

        analyze_btn = gr.Button(
            "📊 AI评分",
            variant="primary"
        )

        thesis_btn = gr.Button(
            "🧠 投资观点"
        )

        download_btn = gr.Button(
            "📄 下载PDF"
        )
    with gr.Row():
        pdf_file = gr.File(
            label="下载报告",
            interactive=False
        )

        download_btn.click(
            fn=download_latest_pdf,
            inputs=user_state,
            outputs=pdf_file
        )

    analyze_output = gr.Textbox(
        label="评分报告",
        lines=18)

    def analyze_wrapper(file, user):
        if user is None:
            return "请先登录"

        return analyze(file, user)

    def download_latest_pdf(user):

        if user is None:
            return None

        record = get_latest_analysis(user)

        if record is None:
            return None

        return export_pdf(record)

    analyze_btn.click(
        fn=analyze_wrapper,
        inputs=[
            file_input,
            user_state
        ],
        outputs=analyze_output
    )
    thesis_btn.click(
        fn=thesis_wrapper,
        inputs=file_input,
        outputs=analyze_output
    )
    # =========================
    # 投资观点（新🔥）
    # =========================


    # =========================
    # 行业对比（已有）
    # =========================
    gr.Markdown("""
    ## ⚖️ 公司财报对比

    同时上传两家公司财报，自动生成对比分析。
    """)

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
    gr.Markdown("""
       ## 📚 分析历史

       查看分析历史和报告。
       """)
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
            inputs=user_state,
            outputs=company_dropdown
        )
    company_dropdown.change(
        fn=on_select,
        inputs=[
            company_dropdown,
            user_state
        ],
        outputs=analysis_view
    )

    gr.Markdown("""
    ## 📈 Dashboard

    查看累计分析数据及评分统计。
    """)
    refresh = gr.Button("刷新")

    dashboard_md = gr.Markdown()

    refresh.click(
            fn=dashboard,
            inputs=user_state,
            outputs=dashboard_md
        )
demo.launch(server_name="0.0.0.0", server_port=10000)
