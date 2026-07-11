import os
import json
import urllib.request
import urllib.error
import ssl
from n8n_utils import load_n8n_config, n8n_request as n8n_request_alias

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

n8n_host, n8n_api_key = load_n8n_config(ENV_FILE)

def n8n_request(endpoint, method="GET", data=None, timeout=None):
    return n8n_request_alias(endpoint, n8n_host, n8n_api_key, method, data, timeout=timeout)

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
