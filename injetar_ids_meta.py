import os
from utils.n8n_api import n8n_request, get_n8n_credentials

import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_host, n8n_api_key = get_n8n_credentials()
workflow_id = "publicadorSocialDlNexusV320260518"

data, err = n8n_request(f"workflows/{workflow_id}")
if err:
    print(f"Erro ao buscar: {err}")
    exit(1)

nodes = data.get("nodes", [])

for n in nodes:
    if "PAGE_ID_AQUI" in json.dumps(n) or "INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI" in json.dumps(n):
        if "url" in n.get("parameters", {}):
            url_val = n["parameters"]["url"]
            if isinstance(url_val, str):
                url_val = url_val.replace("PAGE_ID_AQUI", "379537031716700")
                url_val = url_val.replace("INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI", "379537031716700")
                n["parameters"]["url"] = url_val

# Construir payload blindado
payload = {
    "name": data.get("name"),
    "nodes": nodes,
    "connections": data.get("connections", {}),
    "settings": {}
}

res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=payload)
if err:
    print(f"Erro ao atualizar na VPS: {err}")
    exit(1)
print("Workflow injetado com o ID 379537031716700 nas APIs do Meta!")

# Disparar
webhook_url = n8n_host.replace("/api/v1/", "/webhook/disparo-automatico")

try:
    req = urllib.request.Request(webhook_url, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"NOVO POST DISPARADO! Status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Erro no webhook: HTTP {e.code}")
except Exception as e:
    print(f"Erro no disparo: {e}")
