from database import supabase

def save_history(email, company, score, analysis_result):

    return (
        supabase
        .table("analysis_history")
        .insert({
            "email": email,
            "company": company,
            "score": score,
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
