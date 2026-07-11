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

# Workflow 086 foi ativado. Vou pegar ele
data_086, err = n8n_request(f"workflows/QdiDAcKazb5ADTBY")

old_nodes = data_086.get("nodes", [])
old_connections = data_086.get("connections", {})

# Substituir temporariamente pelos nós do Drive
temp_nodes = [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "setup-drive-temp",
        "responseMode": "lastNode",
        "options": {}
      },
      "id": "trigger_webhook",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [0, 0]
    },
    {
      "parameters": {
        "operation": "create",
        "name": "00_DL_NEXUS_EMPRESA",
        "options": {}
      },
      "id": "root",
      "name": "Criar Raiz",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [200, 0],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "01_FOTOS",
        "options": {"parents": ["={{ $json.id }}"]}
      },
      "id": "fotos",
      "name": "Criar FOTOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, -200],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "02_VIDEOS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "videos",
      "name": "Criar VIDEOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, -100],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "03_DOCUMENTOS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "docs",
      "name": "Criar DOCS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, 0],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "04_SENSIVEIS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "sensitivos",
      "name": "Criar SENSIVEIS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, 100],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "return {\n  json: {\n    root: $('Criar Raiz').item.json.id,\n    fotos: $('Criar FOTOS').item.json.id,\n    videos: $('Criar VIDEOS').item.json.id,\n    docs: $('Criar DOCS').item.json.id,\n    sensiveis: $('Criar SENSIVEIS').item.json.id\n  }\n};"
      },
      "id": "output",
      "name": "Montar Resposta",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [600, 0]
    }
]

temp_conns = {
    "Webhook Trigger": { "main": [[{"node": "Criar Raiz", "type": "main", "index": 0}]] },
    "Criar Raiz": { "main": [[{"node": "Criar FOTOS", "type": "main", "index": 0}, {"node": "Criar VIDEOS", "type": "main", "index": 0}, {"node": "Criar DOCS", "type": "main", "index": 0}, {"node": "Criar SENSIVEIS", "type": "main", "index": 0}]] },
    "Criar FOTOS": { "main": [[{"node": "Montar Resposta", "type": "main", "index": 0}]] }
}

payload = {
    "name": data_086.get("name", "TEMP"),
    "nodes": temp_nodes,
    "connections": temp_conns,
    "settings": {}
}

res, err = n8n_request(f"workflows/QdiDAcKazb5ADTBY", method="PUT", data=payload)
if err: print(f"Erro no PUT: {err}")
print("086 sequestrado temporariamente para criar pastas...")

import time
time.sleep(2)
n8n_request(f"workflows/QdiDAcKazb5ADTBY/activate", method="POST")
time.sleep(3)

# Disparar
webhook_url = n8n_host.replace("/api/v1/", "/webhook/setup-drive-temp")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
try:
    req = urllib.request.Request(webhook_url, method="POST", data=b'{"texto":"dummy"}')
    req.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(req, context=ctx)
    result_data = json.loads(response.read().decode('utf-8'))
    print("\nSUCESSO! Pastas criadas:")
    print(json.dumps(result_data, indent=2))
    
    with open(r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\00_CONFIG\drive_folders_map.json", "w") as f:
        json.dump(result_data, f, indent=2)
except Exception as e:
    print(f"Erro no disparo temp: {e}")

# Restaurar 086
payload["nodes"] = old_nodes
payload["connections"] = old_connections
n8n_request(f"workflows/QdiDAcKazb5ADTBY", method="PUT", data=payload)
n8n_request(f"workflows/QdiDAcKazb5ADTBY/activate", method="POST")
print("086 restaurado!")
