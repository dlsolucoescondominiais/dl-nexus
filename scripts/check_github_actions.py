import requests

def check_github_actions():
    url = 'https://api.github.com/repos/dlsolucoescondominiais/dl-nexus/actions/runs?branch=main'
    
    # Repositórios públicos permitem chamadas limitadas sem token.
    response = requests.get(url)
    
    if response.status_code == 200:
        runs = response.json().get('workflow_runs', [])
        if runs:
            print(f"Última execução: {runs[0]['status']} - {runs[0]['html_url']}")
        else:
            print("Nenhuma execução encontrada")
    else:
        print(f"Erro GitHub: {response.status_code}")
        try:
            print(response.json())
        except:
            pass

if __name__ == '__main__':
    check_github_actions()
