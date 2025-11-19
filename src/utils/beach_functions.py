import os

from dotenv import load_dotenv
from supabase import create_client


def get_beach_id(code, slug):
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabase_client = create_client(url, key)

    try:
        beach_id = (
            supabase_client.table("beach_location")
                .select("id")
                .eq("location_code", code)
                .eq("slug", slug)
                .execute()
        ).data[0]['id']

    except Exception as ex:
        return {"id": None, "error_msg": str(ex), "code": code, "slug": slug}

    return {"id": beach_id, "error_msg": None}
