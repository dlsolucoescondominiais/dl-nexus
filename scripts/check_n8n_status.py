import requests

def check_n8n_status():
    url = 'https://seu-n8n-production.com/api/v1/status'
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"Status n8n: {response.json()['status']}")
        else:
            print(f"Erro HTTP: {response.status_code}")
    except Exception as e:
        print(f"Erro de Conexão: {str(e)}")

check_n8n_status()
