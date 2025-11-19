import os
import shutil
import pdfplumber
import requests

from src.config.paths import DATA_DIR


def read_pdfs(file_path):
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


def remove_pdfs():
    pdf_dir = f'{DATA_DIR}/pdfs'

    for name in os.listdir(pdf_dir):
        path = os.path.join(pdf_dir, name)

        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def download_file(url: str, filename: str) -> str | None:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/122.0.0.0 Safari/537.36"
        }

        resposta = requests.get(url, headers=headers)

        if resposta.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resposta.content)

            return filename

        else:
            return None

    except Exception as e:
        return None