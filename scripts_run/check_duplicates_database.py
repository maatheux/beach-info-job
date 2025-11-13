import os

import supabase
from dotenv import load_dotenv
from supabase import create_client


def start():
    load_dotenv()


    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)

    response = None

    try:
        response = supabaseClient.table("beach_location").select("location_code").execute()

    except Exception as ex:
        print(ex)
        return False

    hash_table = {}
    for i in response.data:
        hash_table[i['location_code']] = hash_table.get(i['location_code'], 0) + 1

    print(sorted(hash_table.items(), key=lambda x: x[1], reverse=True))

    return None


def add_beach_id():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)

    beaches_info = None
    try:
        beaches_info = (supabaseClient.table("beach_location")
                    .select("id, name, location_code")
                    .not_.in_("location_code", ["AR00", "MR0000", "SG000", "CS0000"])
                    .execute()).data

    except Exception as ex:
        print(ex)

    beaches_status = (supabaseClient.table("beach_info")
                      .select("id, location_code, report_date", "beach_id")
                      .is_("beach_id", None)
                      .not_.in_("location_code", ["AR00", "MR0000", "SG000", "CS0000"])
                      .execute()).data

    for i in beaches_status:
        print(i)


    for i in beaches_status:
        info = [j for j in beaches_info if j['location_code'] == i['location_code']][0]

        supabaseClient.table("beach_info").update({"beach_id": info["id"]}).eq("id", i["id"]).execute()

        # (supabaseClient.table("beach_info")
        #  .update())


if __name__ == '__main__':
    # start()
    add_beach_id()
