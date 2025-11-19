import os

import supabase
from dotenv import load_dotenv
from supabase import create_client
import json


def add_slug():
    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)

    # with open('../utils/locais.json', 'r', encoding='utf-8-sig') as file:
    #     jsonData = json.load(file)

    for i in range(300, 307):
        # supabaseClient.table("beach_location").update({"slug": i["slug"]}).eq("city", i["cidade"]).execute()
        supabaseClient.table("beach_location").update({"slug": "São-Francisco-de-Itabapoana"}).eq("id", i).execute()


    # for i in beaches_status:
    #     info = [j for j in beaches_info if j['location_code'] == i['location_code']][0]
    #
    #     supabaseClient.table("beach_info").update({"beach_id": info["id"]}).eq("id", i["id"]).execute()

        # (supabaseClient.table("beach_info")
        #  .update())


if __name__ == '__main__':
    add_slug()
