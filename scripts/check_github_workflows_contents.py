import requests

def check_configured_workflows():
    url = 'https://api.github.com/repos/dlsolucoescondominiais/dl-nexus/contents/.github/workflows'
    
    response = requests.get(url)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            print(f"Workflow: {file['name']} - Path: {file['path']}")
    else:
        print(f"Erro GitHub: {response.status_code}")
        try:
            print(response.json())
        except:
            pass

check_configured_workflows()
