import os
import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

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
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

workflow_id = "publicadorSocialDlNexusV320260518"

data, err = n8n_request(f"workflows/{workflow_id}")
if err:
    print(f"Erro ao buscar: {err}")
    exit(1)

nodes = data.get("nodes", [])
connections = data.get("connections", {})

# Verificar se TikTok ja esta
has_tiktok = any(n.get("name") == "Call TikTok Workflow" for n in nodes)

if not has_tiktok:
    tiktok_node = {
      "parameters": {
        "workflowId": "HafnpJDL0AsP5fNh", # ID do 084_PUBLICADOR_TIKTOK_ASSISTIDO
        "mode": "fireAndForget"
      },
      "id": "call_tiktok",
      "name": "Call TikTok Workflow",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [2600, -100]
    }
    nodes.append(tiktok_node)
    
    # Ligar a partir do Telegram Aviso Publicacao em paralelo ao Facebook
    if "Telegram Aviso Publicacao" in connections:
        connections["Telegram Aviso Publicacao"]["main"][0].append(
            {"node": "Call TikTok Workflow", "type": "main", "index": 0}
        )

# Construir payload blindado
payload = {
    "name": data.get("name"),
    "nodes": nodes,
    "connections": connections,
    "settings": {}
}

res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=payload)
if err:
    print(f"Erro ao atualizar na VPS: {err}")
    exit(1)
print("Fluxo 020 atualizado para chamar o TikTok (084)!")

# Disparar
webhook_url = n8n_host.replace("/api/v1/", "/webhook/disparo-automatico")
try:
    req = urllib.request.Request(webhook_url, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"POST DISPARADO! Status: {response.status}")
except Exception as e:
    pass
