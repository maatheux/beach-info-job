import pdfplumber
import pandas as pd


def extract_table(file_path):
    tables = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables_on_page = page.extract_tables({
                # 'vertical_strategy': 'text',
                # 'horizontal_strategy': 'text',
                # 'intersection_x_tolerance': 30,
                # 'intersection_y_tolerance': 10
            })
    
            if tables_on_page:
                for table in tables_on_page:
                    if table:
                        tables.append({
                            'page': pdf.pages.index(page) + 1,
                            'data': table
                        })
        
        return tables[0]
    
    # for table in tables:
    #     print('Page:', table['page'])
    #     print(pd.DataFrame(table['data']).to_string())
    

if __name__ == "__main__":
    table = extract_table("../data/pdfs/saquarema-base.pdf")
    table = pd.DataFrame(table['data'])
    print(table.to_string())
    
    for row in table.itertuples(index=False):
        print(f"{row._0} = {row._4}")