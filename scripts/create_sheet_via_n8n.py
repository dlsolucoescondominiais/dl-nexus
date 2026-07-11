import os
import sys
import json
import time
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
base_url = "https://n8n.dlsolucoescondominiais.com.br"
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# Usar Google Drive node nativo do n8n (que JA funciona) para criar arquivo tipo Sheets
webhook_path = "temp-criar-sheet-151-v2"

workflow_payload = {
    "name": "TEMP_CRIAR_PLANILHA_151_V2",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": webhook_path,
                "responseMode": "lastNode",
                "options": {}
            },
            "id": "webhook-1",
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [250, 300],
            "webhookId": "temp-sheet-151-v2"
        },
        {
            "parameters": {
                "operation": "createFromText",
                "name": "[DL_NEXUS] Log de Publicacoes Meta",
                "content": "data_geracao\tid_execucao_n8n\tlinha_dl\ttema\tcopy_texto\tprompt_imagem\tlink_imagem_drive\tstatus_facebook\tstatus_instagram",
                "mimeType": "application/vnd.google-apps.spreadsheet",
                "options": {}
            },
            "id": "drive-1",
            "name": "Criar Planilha via Drive",
            "type": "n8n-nodes-base.googleDrive",
            "typeVersion": 3,
            "position": [470, 300],
            "credentials": {
                "googleDriveOAuth2Api": {
                    "id": "rPbeTiXIAg21Up1M",
                    "name": "Google Drive account"
                }
            }
        }
    ],
    "connections": {
        "Webhook": {
            "main": [[{"node": "Criar Planilha via Drive", "type": "main", "index": 0}]]
        }
    },
    "settings": {"executionOrder": "v1"}
}

# 1. Criar workflow
print("[1/5] Criando workflow temporario V2...")
cr = requests.post(f"{host}/workflows", json=workflow_payload, headers=headers, verify=False, timeout=15)
if cr.status_code != 200:
    print(f"Erro: {cr.status_code} - {cr.text[:300]}")
    sys.exit(1)
wf_id = cr.json().get('id')
print(f"   ID: {wf_id}")

# 2. Ativar
print("[2/5] Ativando...")
act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
if act_r.status_code != 200:
    print(f"   Erro: {act_r.status_code} - {act_r.text[:200]}")
    requests.delete(f"{host}/workflows/{wf_id}", headers=headers, verify=False)
    sys.exit(1)
print("   Ativado!")
time.sleep(2)

# 3. Disparar
print("[3/5] Disparando webhook...")
trigger_r = requests.post(f"{base_url}/webhook/{webhook_path}", json={"action": "create"}, verify=False, timeout=30)

if trigger_r.status_code == 200:
    result = trigger_r.json()
    file_id = result.get('id', 'NAO ENCONTRADO')
    file_name = result.get('name', 'NAO ENCONTRADO')
    web_link = result.get('webViewLink', result.get('webContentLink', 'NAO ENCONTRADO'))
    
    print(f"\n   === PLANILHA CRIADA COM SUCESSO ===")
    print(f"   ID: {file_id}")
    print(f"   Nome: {file_name}")
    print(f"   Link: {web_link}")
    
    with open(r'd:\AntiGravity\projeto_01\SHEET_ID_151.txt', 'w') as f:
        f.write(f"SPREADSHEET_ID={file_id}\n")
        f.write(f"SPREADSHEET_URL=https://docs.google.com/spreadsheets/d/{file_id}\n")
    print(f"   Salvo em SHEET_ID_151.txt")
else:
    print(f"   Erro webhook: {trigger_r.status_code}")
    print(f"   Body: {trigger_r.text[:500]}")

# 4. Desativar
print(f"\n[4/5] Desativando...")
requests.post(f"{host}/workflows/{wf_id}/deactivate", headers=headers, verify=False, timeout=15)

# 5. Deletar
print(f"[5/5] Deletando...")
del_r = requests.delete(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
print(f"   {'Deletado!' if del_r.status_code == 200 else f'Erro: {del_r.status_code}'}")
