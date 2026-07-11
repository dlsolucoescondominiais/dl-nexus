import requests

def check_workflow_status():
    url = 'http://129.121.35.90:5678/workflows'
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            workflows = response.json()
            print(f"Total de workflows: {len(workflows)}")
            
            # Listar workflows ativados
            for wf in workflows:
                if wf.get('active'):
                    print(f"Workflow ativado: {wf['name']} (ID: {wf['id']})")
        else:
            print(f"Erro HTTP: {response.status_code}")
    except Exception as e:
        print(f"Erro de Conexão: {str(e)}")

check_workflow_status()
