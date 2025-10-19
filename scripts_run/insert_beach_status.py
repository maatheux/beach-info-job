import pdfplumber
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client
from datetime import datetime


def start_insert(file_path, report_date):
    extracted_table = extract_table(file_path)
    table = pd.DataFrame(extracted_table['data'])
    
    dataList = []
    trat_code_list = []

    title = next(table.itertuples(index=False), None)

    if title._1 is None:
        valid_coluna_code = 'LOCALIZAÇÃO (*) CONAMA' in title._0.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._0.upper()
    else:
        valid_coluna_code = \
            True \
                if title._1.replace('\n', ' ').lower() == 'ponto coleta' \
                else 'LOCALIZAÇÃO (*) CONAMA' in title._1.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._1.upper()

    coluna_code = 1 if valid_coluna_code else 2
    coluna_status = 3 if len(title) == 5 else 4

    idx = 0
    for row in table.itertuples(index=False):
        trat_code = row[coluna_code]
        if "\n" in row[coluna_code] if row[coluna_code] is not None and idx != 0 else "":
            trat_code_list = row[coluna_code].split("\n")[::-1]

        last_code = trat_code_list.pop() if len(trat_code_list) != 0 else None

        if (trat_code is not None and trat_code != '') or last_code is not None:
            code = trat_code if last_code is None else last_code        
        else:
            code = None

        dataList.append({
            "location_code": code,
            "water_status": "Amostragem Não Realizada" if row[coluna_status] not in ['Própria', 'Imprópria'] else row[coluna_status],
            "report_date": report_date
        })

        idx+=1


    data_table = dataList[1:]

    data_table = [element for element in data_table if element['location_code'] is not None]

    load_dotenv()

    for data in data_table:
        print(data)
    
    if check_date_report(data_table):
        return

    insert_info(data_table)


def extract_table(file_path):
    tables = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables({})

            if tables_on_page:
                for table in tables_on_page:
                    if table:
                        tables.append({
                            'page': pdf.pages.index(page) + 1,
                            'data': table
                        })

        return tables[0]


def insert_info(table_info):
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)

    try:
        response = (
            supabaseClient.table("beach_info")
            .insert(table_info)
            .execute()
        )

        print(response)

    except Exception as ex:
        print(ex)


def check_date_report(info_list):
    load_dotenv()
    
    element = info_list[0]
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SECRET_KEY")

    supabaseClient = create_client(url, key)
    
    response = None
    
    try:
        response = (
            supabaseClient.table("beach_info")
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
        
    return response.data[0]['report_date'] == element['report_date'].strftime('%Y-%m-%d')


if __name__ == "__main__":
    start_insert(f'{"."}./pdfs/Paraty-13-10-25.pdf', datetime(2025, 10, 13))

    # check_date_report([{"location_code": 'PO00', 'report_date': datetime(2025, 10, 13)}])
    
    