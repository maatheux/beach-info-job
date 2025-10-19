import camelot

tables = camelot.read_pdf("Zona-oeste-e-Zona-sul-20-08-25.pdf", pages="all", flavor="stream", suppress_stdout=False)

for table in tables:
    print("Table")
    print(table.df.to_string())


# import pytesseract
# from pdf2image import convert_from_path
# 
# # 1. Converte PDF para imagens (uma por página)
# pages = convert_from_path("Zona-oeste-e-Zona-sul-20-08-25.pdf", poppler_path=r"C:\extensoes\poppler-25.07.0-0\poppler-25.07.0\Library\bin")
# 
# for i, page in enumerate(pages):
#     # 2. Extrai texto com OCR
#     text = pytesseract.image_to_string(page, lang="por")
#     print(f"--- Página {i+1} ---")
#     print(text)

import re
# from pdfminer.high_level import extract_pages, extract_text
# import pandas as pd
# 
# # Extrai texto do PDF
# text = extract_text("Zona-oeste-e-Zona-sul-20-08-25.pdf")
# 
# linhas = text.splitlines()
# 
# print(linhas)

# # Expressão regular para capturar padrões
# pattern = re.compile(r"[a-zA-Z]+,{1}\s{1}")
# matches = pattern.findall(text)
# 
# # Exemplo de manipulação dos resultados
# names = [n[:-1] for n in matches]

