import os
from datetime import datetime
from src.utils.pdfs_functions import read_pdfs
from src.utils.beach_functions import get_beach_id
import pandas as pd
from src.config.paths import LOGS_DIR


def structuring_data(file_path, report_date, slug):
    extracted_table = read_pdfs(file_path)
    table = pd.DataFrame(extracted_table['data'])

    data_list = []
    trat_code_list = []
    error_beach_id_list = []

    title = next(table.itertuples(index=False), None)

    if title._1 is None:
        valid_column_code = 'LOCALIZAÇÃO (*) CONAMA' in title._0.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._0.upper()
    else:
        valid_column_code = \
            True \
                if title._1.replace('\n', ' ').lower() == 'ponto coleta' \
                else 'LOCALIZAÇÃO (*) CONAMA' in title._1.upper() or 'PONTO COLETA LOCALIZAÇÃO (*)' in title._1.upper()

    coluna_code = 1 if valid_column_code else 2
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

        beach_id = get_beach_id(code, slug)

        if beach_id["id"] is None and idx != 0:
            error_beach_id_list.append(beach_id)
            continue

        data_list.append({
            "location_code": code,
            "water_status": "Amostragem Não Realizada" if row[coluna_status] not in ['Própria', 'Imprópria'] else row[
                coluna_status],
            "report_date": report_date,
            "beach_id": beach_id["id"]
        })

        idx += 1


    # TODO: Fix logging of errors
    # if len(error_beach_id_list) > 0:
    #     if not os.path.exists(LOGS_DIR):
    #         os.makedirs(LOGS_DIR)
    #
    #     with open(f'{LOGS_DIR}/error_beach_id_{datetime.now().strftime("%Y%m%d%H%M%S")}.txt', 'w') as f:
    #         for error in error_beach_id_list:
    #             f.write(f"Code: {error['code']}, Slug: {error['slug']}, Error: {error['error_msg']}\n")

    data_table = data_list[1:]

    data_table = [element for element in data_table if element['location_code'] is not None]

    return data_table
