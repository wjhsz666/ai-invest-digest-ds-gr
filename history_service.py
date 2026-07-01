from database import supabase

def save_history(email, company, score,revenue_grade,profit_grade,cashflow_grade, analysis_result):

    return (
        supabase
        .table("analysis_history")
        .insert({
            "email": email,
            "company": company,
            "score": score,
            "revenue_grade": revenue_grade,
            "profit_grade": profit_grade,
            "cashflow_grade": cashflow_grade,
            "analysis_result": analysis_result

        })
        .execute()
    )

def get_history(email):

    response = (
        supabase
        .table("analysis_history")
        .select("*")
        .eq("email", email)
        .order("created_at", desc=True)
        .execute()
    )

    return response.data
def get_analysis(record_id):

    response = (
        supabase
        .table("analysis_history")
        .select("*")
        .eq("id", record_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None
def get_dashboard(email):

    history = get_history(email)

    total = len(history)

    if total == 0:
        return {
            "total": 0,
            "avg_score": 0,
            "a_count": 0,
            "b_count": 0,
            "c_count": 0,
            "top5": [],
            "recent": []
        }

    avg_score = sum(item["score"] for item in history) / total

    a_count = sum(1 for item in history if item["revenue_grade"] == "A")

    b_count = sum(1 for item in history if item["revenue_grade"] == "B")

    c_count = sum(1 for item in history if item["revenue_grade"] == "C")

    top5 = sorted(
        history,
        key=lambda x: x["score"],
        reverse=True
    )[:5]

    recent = history[:5]

    return {

        "total": total,

        "avg_score": avg_score,

        "a_count": a_count,

        "b_count": b_count,

        "c_count": c_count,

        "top5": top5,

        "recent": recent

    }
def get_analysis_by_company(email, company):

    response = (
        supabase
        .table("analysis_history")
        .select("*")
        .eq("email", email)
        .eq("company", company)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None

def get_latest_analysis(email):

    response = (
        supabase
        .table("analysis_history")
        .select("*")
        .eq("email", email)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


