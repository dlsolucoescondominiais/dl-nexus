import os
import requests
import json
N8N_HOST = "https://n8n.dlsolucoescondominiais.com.br/api/v1"
N8N_API_KEY = "N8N_API_KEY_HERE"

headers = {
    'X-N8N-API-KEY': N8N_API_KEY,
    'Content-Type': 'application/json'
}

BOT_TOKEN = "TELEGRAM_BOT_TOKEN_HERE"
CRED_NAME = "Aninha Telegram Bot (DL Nexus)"

def create_telegram_credential():
    print(f"[*] Criando credencial '{CRED_NAME}' no n8n...")
    payload = {
        "name": CRED_NAME,
        "type": "telegramApi",
        "data": {
            "accessToken": BOT_TOKEN
        }
    }
    resp = requests.post(f"{N8N_HOST}/credentials", json=payload, headers=headers, verify=False)
    if resp.status_code in [200, 201]:
        cred = resp.json()
        print(f"[+] Credencial criada com sucesso! ID: {cred['id']}")
        return cred['id'], cred['name']
    else:
        print(f"[-] Erro ao criar credencial: {resp.text}")
        return None, None

def deploy_workflow_092(cred_id, cred_name):
    print("[*] Buscando o Workflow 092...")
    resp = requests.get(f"{N8N_HOST}/workflows", headers=headers, verify=False)
    workflows = resp.json().get('data', [])
    wf_092 = next((w for w in workflows if '092_MESA_APROVACAO' in w['name']), None)
    
    if not wf_092:
        print("[-] Workflow 092 não encontrado no servidor n8n!")
        return
    
    print(f"[*] Atualizando workflow {wf_092['id']} com a nova credencial...")
    wf_details = requests.get(f"{N8N_HOST}/workflows/{wf_092['id']}", headers=headers, verify=False).json()
    
    # Injetar credencial nos nós do Telegram
    for node in wf_details.get('nodes', []):
        if node.get('type') in ['n8n-nodes-base.telegram', 'n8n-nodes-base.telegramTrigger']:
            if 'credentials' not in node:
                node['credentials'] = {}
            node['credentials']['telegramApi'] = {
                "id": cred_id,
                "name": cred_name
            }
            print(f"  -> Nó '{node['name']}' atualizado com a credencial.")
            
    # Limpar campos bloqueados da API antes do update
    for field in ['id', 'createdAt', 'updatedAt', 'meta', 'pinData', 'versionId', 'triggerCount']:
        wf_details.pop(field, None)
        
    wf_details['active'] = True # Forçar ativação
    
    print("[*] Fazendo push do workflow atualizado e ativando...")
    put_resp = requests.put(f"{N8N_HOST}/workflows/{wf_092['id']}", json=wf_details, headers=headers, verify=False)
    
    if put_resp.status_code == 200:
        print("[+] Sucesso! A Mesa de Aprovação da Aninha (092) está ATIVA e autênticada no Telegram!")
    else:
        print(f"[-] Erro ao atualizar/ativar workflow: {put_resp.text}")

if __name__ == '__main__':
    # Ignorar warnings de SSL
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    c_id, c_name = create_telegram_credential()
    if c_id:
        deploy_workflow_092(c_id, c_name)
