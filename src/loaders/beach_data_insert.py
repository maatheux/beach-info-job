import logging
import os

from dotenv import load_dotenv

from src.config.logger import Logger
from src.utils import check_date_report
from supabase import create_client



def insert_beach_status(data_table, date_formatted):
    logger = Logger.get_logger(__name__)

    if check_date_report(data_table, date_formatted):
        logger.warning("Report already inserted")
        return

    load_dotenv()

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)

    try:
        response = (
            supabaseClient.table("beach_info")
            .insert(data_table)
            .execute()
        )

        logger.warning(f"Report inserted successfully")

    except Exception as ex:
        print(ex)
