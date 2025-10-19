import json
import os
import shutil
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from scripts_run.dowload_pdf import download_file
from scripts_run.insert_beach_status import start_insert


def start():
    report_info = download_reports()
    print(report_info)
    
    for i in report_info:
        start_insert(i['fileDownloadPath'], i['dateRef'])

    remove_pdfs()
    

def download_reports():
    with open('utils/locais.json', 'r', encoding='utf-8-sig') as file:
        jsonData = json.load(file)
        
    dataList = []
    today = datetime.today()
    for i in jsonData['locais']:
        dateRef = today + timedelta(days=1)
        
        downloadValid = True
        dateAux = 60
        while downloadValid and dateAux > 0:
            dateRef = dateRef - timedelta(days=1)
            
            url = f"https://www.inea.rj.gov.br/wp-content/uploads/{dateRef.strftime('%Y')}/{dateRef.strftime('%m')}/{i['slug']}-{dateRef.strftime('%d-%m-%y')}.pdf"
            filename = f"./pdfs/{i['slug'].lower()}-base.pdf"
            
            print(url)
            resultDownload = download_file(url, filename)
            
            if resultDownload is None:
                dateRefMonthAlt = dateRef + relativedelta(months=1)
                url = f"https://www.inea.rj.gov.br/wp-content/uploads/{dateRef.strftime('%Y')}/{dateRefMonthAlt.strftime('%m')}/{i['slug']}-{dateRef.strftime('%d-%m-%y')}.pdf"    
                print(url)
                resultDownload = download_file(url, filename)
            
            if (resultDownload == filename):
                downloadValid = False
                i['dateRef'] = dateRef.isoformat()
                i['fileDownloadPath'] = filename
                dataList.append(i)
            
            dateAux -= 1
    
    return dataList


def remove_pdfs():
    pdf_dir = './pdfs'
    
    for name in os.listdir(pdf_dir):
        path = os.path.join(pdf_dir, name)
        
        if os.path.isfile(path) or os.path.islink(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


if __name__ == "__main__":
    start()
