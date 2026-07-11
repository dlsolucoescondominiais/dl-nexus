import requests

def check_workflow_status():
    try:
        response = requests.get('http://localhost:5678/workflows')
        if response.status_code == 200:
            print(response.json())
        else:
            print(f'Erro HTTP: {response.status_code}')
    except Exception as e:
        print('Erro de Conexão:', str(e))

check_workflow_status()
