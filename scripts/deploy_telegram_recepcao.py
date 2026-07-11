import os
import json
import ssl
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
WF_FILE = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\001_TELEGRAM_RECEPCAO_ANINHA_V3.json"

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key
# 1. Read the local JSON
with open(WF_FILE, "r", encoding="utf-8") as f:
    wf_data = json.load(f)

# 2. Check if already exists
print("[*] Verificando se o workflow já existe no n8n...")
workflows_data, err = n8n_request("workflows")
if err:
    print(f"[-] Erro ao listar workflows: {err}")
    exit(1)

existing_wf = None
for w in workflows_data.get('data', []):
    if w.get('name') == "001_TELEGRAM_RECEPCAO_ANINHA_V3":
        existing_wf = w
        break

payload = {
    "name": wf_data.get("name"),
    "nodes": wf_data.get("nodes"),
    "connections": wf_data.get("connections"),
    "settings": wf_data.get("settings", {})
}

wf_id = None

if existing_wf:
    print(f"[+] Workflow encontrado (ID: {existing_wf['id']}). Atualizando...")
    wf_id = existing_wf['id']
    res, err = n8n_request(f"workflows/{wf_id}", method="PUT", data=payload)
    if err:
        print(f"[-] Erro ao atualizar workflow: {err}")
        exit(1)
    print("[+] Workflow atualizado com sucesso!")
else:
    print("[*] Criando novo workflow no n8n...")
    res, err = n8n_request("workflows", method="POST", data=payload)
    if err:
        print(f"[-] Erro ao criar workflow: {err}")
        exit(1)
    wf_id = res.get('id')
    print(f"[+] Workflow criado com sucesso! ID: {wf_id}")

print("[*] Ativando o workflow...")
res, err = n8n_request(f"workflows/{wf_id}/activate", method="POST", data={})
if err:
    print(f"[-] Erro ao ativar o workflow: {err}")
else:
    print("[+] Workflow 001_TELEGRAM_RECEPCAO_ANINHA_V3 ATIVADO com sucesso no n8n!")
