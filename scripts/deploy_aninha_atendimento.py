import os
import json
import ssl
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from n8n_utils import load_n8n_config, n8n_request as n8n_request_alias
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
WF_FILE = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\002_roteador_aninha_v3_atendimento.json"


n8n_host, n8n_api_key = load_n8n_config(ENV_FILE)

def n8n_request(endpoint, method="GET", data=None, timeout=None):
    return n8n_request_alias(endpoint, n8n_host, n8n_api_key, method, data, timeout=timeout)

# 1. Read the local JSON
with open(WF_FILE, "r", encoding="utf-8") as f:
    wf_data = json.load(f)

# 2. Update it on the server
wf_id = "NgXUbJ96dXJqxGGX"
payload = {
    "name": wf_data.get("name"),
    "nodes": wf_data.get("nodes"),
    "connections": wf_data.get("connections"),
    "settings": wf_data.get("settings", {})
}

print(f"[*] Atualizando workflow Aninha Atendimento (ID: {wf_id})...")
res, err = n8n_request(f"workflows/{wf_id}", method="PUT", data=payload)
if err:
    print(f"[-] Erro ao atualizar workflow: {err}")
    exit(1)

print("[+] Workflow atualizado com sucesso!")
print("[*] Reativando o workflow...")
res, err = n8n_request(f"workflows/{wf_id}/activate", method="POST", data={})
if err:
    print(f"[-] Erro ao reativar o workflow: {err}")
else:
    print("[+] Workflow 002_roteador_aninha_v3_atendimento reativado com sucesso!")
