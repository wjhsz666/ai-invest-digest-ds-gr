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

def increase_usage(email):

    today = str(date.today())

    usage = get_today_usage(email)

    if usage is None:

        supabase.table("user_usage").insert({
            "email": email,
            "usage_date": today,   # 改成你的实际字段名
            "count": 1
        }).execute()

    else:

        supabase.table("user_usage").update({
            "count": usage["count"] + 1
        }).eq("id", usage["id"]).execute()

