import requests
import urllib3

# Desabilita o warning de InsecureRequestWarning para o nosso teste
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def activate_workflow():
    workflow_id = 'B9XUWs7kT21FVQeo'
    
    url = f'https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows/{workflow_id}'
    
    payload = {
        'active': True
    }
    
    headers = {
        'Authorization': 'Bearer SEU_TOKEN_AQUI',
        'Content-Type': 'application/json'
    }
    
    try:
        # ATENÇÃO: Adicionei verify=False para bypassar o erro do SSL autoassinado
        response = requests.put(url, json=payload, headers=headers, verify=False)
        
        if response.status_code == 200:
            print('Workflow ativado com sucesso pela API!')
        else:
            print(f'Erro ao ativar workflow. HTTP Status: {response.status_code}')
            print(f'Retorno: {response.text}')
    except Exception as e:
        print(f"Erro de Conexão: {str(e)}")

activate_workflow()
