import os
import shutil

import pdfplumber


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
    pdf_dir = 'data/pdfs'

    for name in os.listdir(pdf_dir):
        path = os.path.join(pdf_dir, name)

        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)