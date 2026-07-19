import os
import requests
import json
import glob
import time

N8N_HOST = "https://n8n.dlsolucoescondominiais.com.br/api/v1"
N8N_API_KEY = os.environ.get("N8N_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

CRED_NAME = "Conta OpenAI (DL Nexus)"

def create_openai_credential():
    print(f"[*] Criando credencial '{CRED_NAME}' no n8n...")
    payload = {
        "name": CRED_NAME,
        "type": "openAiApi",
        "data": {
            "apiKey": OPENAI_API_KEY
        }
    }
    # Ignorar aviso SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    resp = requests.post(f"{N8N_HOST}/credentials", json=payload, headers=headers, verify=False)
    if resp.status_code in [200, 201]:
        cred = resp.json()
        print(f"[+] Credencial criada com sucesso! ID: {cred['id']}")
        return cred['id'], cred['name']
    else:
        print(f"[-] Erro ao criar credencial: {resp.text}")
        return None, None

def update_local_workflows(cred_id, cred_name):
    # Buscar todos os workflows
    workflow_files = glob.glob(r"DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\*.json")
    updated_files = []
    
    for f_path in workflow_files:
        try:
            with open(f_path, 'r', encoding='utf-8') as f:
                wf = json.load(f)
            
            modified = False
            for node in wf.get('nodes', []):
                if 'openAi' in node.get('type', ''):
                    # Forcar a credencial da OpenAI
                    if 'credentials' not in node:
                        node['credentials'] = {}
                    
                    current_cred = node['credentials'].get('openAiApi', {})
                    if current_cred.get('id') != cred_id:
                        node['credentials']['openAiApi'] = {
                            "id": cred_id,
                            "name": cred_name
                        }
                        modified = True
            
            if modified:
                with open(f_path, 'w', encoding='utf-8') as f:
                    json.dump(wf, f, indent=2)
                updated_files.append(f_path)
                print(f"  -> Arquivo {os.path.basename(f_path)} atualizado com a nova credencial.")
        except Exception as e:
            print(f"Erro ao processar {f_path}: {e}")
            
    return updated_files

if __name__ == '__main__':
    c_id, c_name = create_openai_credential()
    if c_id:
        files = update_local_workflows(c_id, c_name)
        if files:
            print(f"\n[*] {len(files)} workflows locais modificados. Rodando script de deploy massivo...")
            os.system("python deploy_all_workflows.py")
        else:
            print("\n[-] Nenhum workflow precisou ser modificado.")
