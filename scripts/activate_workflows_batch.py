import os
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

def activate_workflows():
    workflow_ids = [
        'B9XUWs7kT21FVQeo',
        'B9XUWs7kT21FVQep',
        'B9XUWs7kT21FVQeq',
    ]
    
    api_key = os.getenv('N8N_API_KEY')
    host = os.getenv('N8N_HOST', 'https://n8n.dlsolucoescondominiais.com.br/api/v1')
    
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    for workflow_id in workflow_ids:
        # Endpoint correto para ativar no n8n
        url = f'{host}/workflows/{workflow_id}/activate'
        
        response = requests.post(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            print(f'Workflow {workflow_id} ativado com sucesso via POST activate!')
        else:
            print(f'Erro ao ativar workflow {workflow_id}: {response.status_code} - {response.text}')

activate_workflows()
