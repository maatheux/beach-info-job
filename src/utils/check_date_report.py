import os
from supabase import create_client
from dotenv import load_dotenv


def check_date_report(info_list, date_formatted):
    load_dotenv()

    element = info_list[0]

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabase_client = create_client(url, key)

    try:
        response = (
            supabase_client.table("beach_info")
            .select('report_date')
            .eq('location_code', element['location_code'])
            .order('created_at', desc=True)
            .limit(1)
            .execute()
        )

    except Exception as ex:
        print(ex)
        return False

    if len(response.data) == 0:
        return False

    return response.data[0]['report_date'] == date_formatted