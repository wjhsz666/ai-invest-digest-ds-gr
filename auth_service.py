from supabase import create_client
from database import supabase


def sign_up(email, password):
    return supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )


def sign_in(email, password):
    return supabase.auth.sign_in_with_password(
        {
            "email": email,
            "password": password
        }
    )


def sign_out():
    supabase.auth.sign_out()


def get_user():
    return supabase.auth.get_user()