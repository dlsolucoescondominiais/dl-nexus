import os
import sys
import json
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

SHEET_ID = "1EqT_yGjPUmxfzluX3bmzXxYu6XcT3J2F"
WORKFLOW_ID = "B9XUWs7kT21FVQeo"

# 1. Buscar workflow atual do n8n
print(f"[1/4] Buscando workflow 151 do n8n...")
r = requests.get(f"{host}/workflows/{WORKFLOW_ID}", headers=headers, verify=False, timeout=15)
if r.status_code != 200:
    print(f"Erro: {r.status_code} - {r.text[:200]}")
    sys.exit(1)

wf = r.json()
print(f"   Nome: {wf.get('name')}")

# 2. Injetar o ID real da planilha nos nodes do Google Sheets
print(f"[2/4] Injetando ID da planilha: {SHEET_ID}")
modified = 0
for node in wf.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.googleSheets':
        if 'parameters' in node and 'documentId' in node['parameters']:
            old_val = node['parameters']['documentId'].get('value', '')
            node['parameters']['documentId']['value'] = SHEET_ID
            node['parameters']['documentId']['mode'] = 'id'
            modified += 1
            print(f"   Node [{node['name']}]: '{old_val}' -> '{SHEET_ID}'")

print(f"   {modified} nodes atualizados.")

# 3. Fazer PUT para atualizar o workflow
print(f"[3/4] Atualizando workflow via API...")

# A API do n8n requer apenas os campos editaveis
# Limpar settings para evitar propriedades extras
clean_settings = {}
raw_settings = wf.get('settings', {})
allowed_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']
for k in allowed_keys:
    if k in raw_settings:
        clean_settings[k] = raw_settings[k]

update_payload = {
    "name": wf.get('name'),
    "nodes": wf.get('nodes'),
    "connections": wf.get('connections'),
    "settings": clean_settings
}

put_r = requests.put(f"{host}/workflows/{WORKFLOW_ID}", json=update_payload, headers=headers, verify=False, timeout=15)
if put_r.status_code == 200:
    print(f"   Workflow atualizado com sucesso!")
else:
    print(f"   Erro PUT: {put_r.status_code} - {put_r.text[:300]}")
    sys.exit(1)

# 4. Tentar ativar
print(f"[4/4] Tentando ativar workflow 151...")
act_r = requests.post(f"{host}/workflows/{WORKFLOW_ID}/activate", headers=headers, verify=False, timeout=15)
if act_r.status_code == 200:
    print(f"   [ATIVADO] 151_MAQUINA_CONTEUDO_META_DL_4X_DIA esta VERDE!")
else:
    try:
        msg = act_r.json().get('message', act_r.text[:300])
    except:
        msg = act_r.text[:300]
    print(f"   [FALHA] {msg}")

# Tambem atualizar o JSON local
print(f"\n[EXTRA] Atualizando JSON local...")
local_path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json'
with open(local_path, 'r', encoding='utf-8') as f:
    local_data = json.load(f)

for node in local_data.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.googleSheets':
        if 'parameters' in node and 'documentId' in node['parameters']:
            node['parameters']['documentId']['value'] = SHEET_ID
            node['parameters']['documentId']['mode'] = 'id'

with open(local_path, 'w', encoding='utf-8') as f:
    json.dump(local_data, f, indent=2, ensure_ascii=False)
print(f"   JSON local atualizado com ID: {SHEET_ID}")
