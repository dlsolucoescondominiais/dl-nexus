import requests

def check_all_workflows():
    url = 'https://api.github.com/repos/dlsolucoescondominiais/dl-nexus/actions/workflows'
    
    response = requests.get(url)
    if response.status_code == 200:
        workflows = response.json().get('workflows', [])
        for wf in workflows:
            print(f"Workflow: {wf['name']} - ID: {wf['id']}")
    else:
        print(f"Erro GitHub: {response.status_code}")
        try:
            print(response.json())
        except:
            pass

check_all_workflows()
