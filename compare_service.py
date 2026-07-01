from pdf_service import read_pdf
from ai_service import client
def compare_companies(file1, file2):

    if file1 is None or file2 is None:
        return "请上传两份财报"

    text1 = read_pdf(file1)
    text2 = read_pdf(file2)

    prompt = f"""
请比较下面两家公司的财报。

输出格式：

# 📊 综合评分

公司A：

公司B：

---------------------

# 📈 收入

公司A：

公司B：

---------------------

# 💰 利润

公司A：

公司B：

---------------------

# 💵 现金流

公司A：

公司B：

---------------------

# ⚠ 风险

公司A：

公司B：

---------------------

# 🧠 AI投资建议

一句话总结。

=======================

公司A财报：

{text1}

=======================

公司B财报：

{text2}
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": "你是一位专业港美股基金经理，请进行结构化分析。"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content