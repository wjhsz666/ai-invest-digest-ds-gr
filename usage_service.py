from datetime import date

from database import supabase

from datetime import date

def get_today_usage(email):

    today = str(date.today())

    response = (
        supabase
        .table("user_usage")
        .select("*")
        .eq("email", email)
        .eq("usage_date", today)
        .execute()
    )

    if len(response.data) == 0:
        return None

    return response.data[0]