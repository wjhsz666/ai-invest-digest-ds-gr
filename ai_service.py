import os
import re

from openai import OpenAI

from pdf_service import read_pdf
from history_service import save_history

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 核心分析函数
def analyze(file):
    if file is None:
        return "请上传财报PDF"

    text = read_pdf(file)

    prompt = f"""
请对以下财报进行分析，并严格按以下“卡片结构”输出：

【输出格式必须严格遵守】

========================
📊 公司健康评分：0-100

📈 收入质量：A / B / C
💰 利润质量：A / B / C
💵 现金流质量：A / B / C

------------------------
⚠️ 风险卡片（最多3条）：
1.
2.
3.

------------------------
🧠 投资结论（1句话）：
========================

【评分规则】
- 收入增长稳定 → 高分
- 利润质量好 → 高分
- 现金流健康 → 高分
- 风险越多 → 扣分

财报内容如下：
{text}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是专业港美股投研分析师，输出必须结构化、适合展示"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )
    analysis = response.choices[0].message.content

    match = re.search(r"公司健康评分.*?(\d{1,3})", analysis)

    if match:
        score = int(match.group(1))
    else:
        score = 0

    def extract_grade(label, text):
        match = re.search(rf"{label}[:：]\s*([ABC])", text)
        return match.group(1) if match else "-"

    revenue_grade = extract_grade("收入质量", analysis)
    profit_grade = extract_grade("利润质量", analysis)
    cashflow_grade = extract_grade("现金流质量", analysis)

    company = file.name.split("/")[-1].replace(".pdf", "")

    save_history(
        email="jack@test.com",
        company=company,
        score=score,
        revenue_grade=revenue_grade,
        profit_grade=profit_grade,
        cashflow_grade=cashflow_grade,
        analysis_result=analysis
    )

    return analysis


def compare_companies(text1, text2):
    prompt = f"""
你是一名专业港美股分析师，请对以下两家公司进行对比分析，并严格按结构输出：

========================
📊 公司A vs 公司B 对比结果

📈 收入增长：
- 公司A：
- 公司B：

💰 利润质量：
- 公司A：
- 公司B：

💵 现金流：
- 公司A：
- 公司B：

⚠️ 风险对比：
- 公司A：
- 公司B：

------------------------
🏆 综合评分：
- 公司A：__/100
- 公司B：__/100

------------------------
🧠 投资结论：
只选一只更优的公司，并说明原因

========================

公司A财报：
{text1}

========================

公司B财报：
{text2}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是专业量化投研分析师，必须结构化输出"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def investment_thesis(text):
    prompt = f"""
你是一名顶级港美股基金经理，请基于以下财报生成投资观点报告，并严格结构化输出：

========================
🧠 投资观点报告

📌 公司定位：
（这家公司是成长/价值/周期/防御型？）

📈 核心驱动因素：
1.
2.
3.

⚠️ 最大风险：
1.
2.

📊 当前估值判断：
（低估 / 合理 / 高估，并说明理由）

🏆 投资建议：
（强烈买入 / 可配置 / 谨慎 / 回避）

------------------------
🧠 一句话总结：

========================

财报内容：
{text}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "你是专业基金经理，输出必须像研报一样专业、克制、结构化"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content