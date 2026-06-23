import os
import json
import ssl
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
WF_FILE = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\002_roteador_aninha_v3_atendimento.json"

n8n_api_key = ""
n8n_host = ""

# Load from .env
with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

def n8n_request(endpoint, method="GET", data=None):
    url = n8n_host + endpoint
    headers = {
        "X-N8N-API-KEY": n8n_api_key,
        "Accept": "application/json"
    }
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            return json.loads(response.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

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
