import json
import logging
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from src.config.logger import Logger
from src.utils.scripts_run.dowload_pdf import download_file
from src.config.paths import DATA_DIR

def download_reports():
    logger = Logger.get_logger(__name__)

    with open(f'{DATA_DIR}/locais.json', 'r', encoding='utf-8-sig') as file:
        json_data = json.load(file)

    data_list = []
    today = datetime.today()
    for i in json_data['locais']:
        logger.warning(f"Try downloading report {i['slug']}")
        date_ref = today + timedelta(days=1)

        download_valid = True
        date_aux = 15
        while download_valid and date_aux > 0:
            date_ref = date_ref - timedelta(days=1)

            url = f"https://www.inea.rj.gov.br/wp-content/uploads/{date_ref.strftime('%Y')}/{date_ref.strftime('%m')}/{i['slug']}-{date_ref.strftime('%d-%m-%y')}.pdf"
            filename = f"data/pdfs/{i['slug'].lower()}-base.pdf"

            result_download = download_file(url, filename)

            if result_download is None:
                date_ref_month_alt = date_ref + relativedelta(months=1)
                url = f"https://www.inea.rj.gov.br/wp-content/uploads/{date_ref.strftime('%Y')}/{date_ref_month_alt.strftime('%m')}/{i['slug']}-{date_ref.strftime('%d-%m-%y')}.pdf"
                result_download = download_file(url, filename)

            if result_download == filename:
                download_valid = False
                i['dateRef'] = date_ref.isoformat()
                i['dateRefFormatted'] = date_ref.strftime('%Y-%m-%d')
                i['fileDownloadPath'] = filename
                logger.warning(f"Downloaded: {filename} / url: {url}")
                data_list.append(i)

            date_aux -= 1

    return data_list