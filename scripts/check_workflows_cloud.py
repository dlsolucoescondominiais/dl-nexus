import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

def check_workflow_status():
    api_key = os.getenv('N8N_API_KEY')
    host = os.getenv('N8N_HOST', 'https://n8n.dlsolucoescondominiais.com.br/api/v1')
    
    url = f'{host}/workflows'
    
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            # A API retorna um objeto {"data": [ workflows... ]}
            data = response.json()
            workflows = data.get('data', [])
            
            print(f"Total de Workflows na Nuvem: {len(workflows)}")
            for wf in workflows:
                status = 'Ativado' if wf.get('active') else 'Desativado'
                print(f"[{status}] {wf['name']} (ID: {wf['id']})")
        else:
            print(f'Erro HTTP: {response.status_code} - {response.text}')
    except Exception as e:
        print(f"Erro de Conexão: {str(e)}")

check_workflow_status()
