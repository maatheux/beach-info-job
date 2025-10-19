import pdfplumber
import pandas as pd
import os
from dotenv import load_dotenv
from supabase import create_client


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
        
        print(tables[0])
        return tables[0]
    
    # for table in tables:
    #     print('Page:', table['page'])
    #     print(pd.DataFrame(table['data']).to_string())
    
    
def insert_info(table_info):
    load_dotenv()
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    supabaseClient = create_client(url, key)
    
    try:
        response = (
            supabaseClient.table("beach_location")
            .insert(table_info)
            .execute()
        )
    
        print(response)
    
    except Exception as ex:
        print(ex)
    

if __name__ == "__main__":
    table = extract_table("../pdfs/casimiro-de-abreu-e-unamar-cabo-frio-base.pdf ")
    table = pd.DataFrame(table['data'])
    # print(table.to_string())

    dataList = []
    city = ""
    
    tratCodeList = []
    tratLocationList = []
    
    title = next(table.itertuples(index=False), None)
    
    print(title)
    
    valid_coluna_code = 'LOCALIZAÇÃO (*) CONAMA' in title._0.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._0.upper() if title._1 is None else (True if title._1.replace('\n', ' ').lower() == 'ponto coleta' else 'LOCALIZAÇÃO (*) CONAMA' in title._1.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._1.upper())
    
    coluna_code = 1 if valid_coluna_code else 2
    coluna_status = 3 if len(title) == 5 else 4
    
    idx = 0
    for row in table.itertuples(index=False):
        tratCode = row[coluna_code]
        if ("\n" in row[coluna_code] if row[coluna_code] is not None and idx != 0 else ""):
            tratCodeList = row[coluna_code].split("\n")[::-1]

        # if ("\n" in row._2 if row._2 is not None else ""):
        #     tratLocationList = row._2.split("\n")[::-1]
        
        lastCode = tratCodeList.pop() if len(tratCodeList) != 0 else None
        
        code = (tratCode if lastCode is None else lastCode) if (tratCode is not None and tratCode != '') or lastCode is not None else None        
        
        
        # city = city if row._0 is None or row._0 == "" else row._0
        # city = "Lagoa de Saquarema" if "SQ0003" in code else city
        dataList.append({
            # "name": city,
            # "uf": "RJ",
            "location_code": code,
            # "location_code": tratCodeList.pop() if len(tratCodeList) > 0 else row._1,
            # "location": row._2.replace("\nAmo", "") if row._2 is not None else row._2,
            # "location": tratLocationList.pop() if len(tratLocationList) > 0 else row._2,
            # "city": "São João da Barra",
            "status": "Amostragem Não Realizada" if row[coluna_status] not in ['Própria', 'Imprópria'] else row[coluna_status]
        })
        
        idx+=1
        
        
    data_table = dataList[1:]
    
    data_table = [element for element in data_table if element['location_code'] is not None]
    
    for data in data_table:
        print(data)
    
    # insert_info(data_table)

    # response = (
    #     supabaseClient.table("beach_location")
    #     .select("*")
    #     .execute()
    # )
    # 
    # print(response)
    
    