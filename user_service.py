from database import supabase

def get_user(email):

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    return response.data
def create_user(email):

    return (
        supabase
        .table("users")
        .insert({
            "email": email,
            "plan": "free"
        })
        .execute()
    )