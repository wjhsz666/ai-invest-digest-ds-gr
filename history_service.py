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
