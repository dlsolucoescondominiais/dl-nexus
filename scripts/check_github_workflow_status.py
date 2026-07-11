import requests

def check_workflow_status():
    url = 'https://api.github.com/repos/dlsolucoescondominiais/dl-nexus/actions/workflows/update-n8n.yml'
    
    response = requests.get(url)
    if response.status_code == 200:
        workflow = response.json()
        print(f"Workflow: {workflow['name']} - Status: {workflow['state']}")
        
        # Verificar execuções recentes
        runs_url = f"https://api.github.com/repos/dlsolucoescondominiais/dl-nexus/actions/workflows/{workflow['id']}/runs"
        runs_response = requests.get(runs_url)
        if runs_response.status_code == 200:
            runs = runs_response.json().get('workflow_runs', [])
            if runs:
                print(f"Última execução: {runs[0]['status']} - {runs[0]['html_url']}")
            else:
                print("Nenhuma execução encontrada")
    else:
        print(f"Erro GitHub: {response.status_code}")

check_workflow_status()
