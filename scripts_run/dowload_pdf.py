import requests


def download_file(url, filename):
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
            print("Erro")
            return None
    
    except Exception as e:
        print(e)
        return None
    

if __name__ == "__main__":
    download_file("https://www.inea.rj.gov.br/wp-content/uploads/2025/08/Niterói-28-08-25.pdf",
                  "./pdfs/niterói-base.pdf")
