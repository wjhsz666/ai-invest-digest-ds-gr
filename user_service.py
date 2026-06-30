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

    response = (
        supabase
        .table("users")
        .insert({
            "email": email,
            "plan": "free"
        })
        .execute()
    )

    return response.data

def get_or_create_user(email):

    user = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .execute()
    )

    if len(user.data) > 0:
        return user.data[0]

    new_user = (
        supabase
        .table("users")
        .insert({
            "email": email,
            "plan": "free"
        })
        .execute()
    )

    return new_user.data[0]

email = "jack@test.com"

user = get_or_create_user(email)
