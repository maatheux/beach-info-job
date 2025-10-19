import requests


def download_file(url, filename):
    try:
        resposta = requests.get(url)
        
        if resposta.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resposta.content)
    
            return filename
    
        else:
            return None
    
    except Exception as e:
        return None
    

if __name__ == "__main__":
    download_file("https://www.inea.rj.gov.br/wp-content/uploads/2025/08/Niterói-28-08-25.pdf",
                  "../pdfs/niterói-base.pdf")
