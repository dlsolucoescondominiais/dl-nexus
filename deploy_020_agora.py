import os
from utils.n8n_api import n8n_request, get_n8n_credentials

import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_host, n8n_api_key = get_n8n_credentials()
file_path = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"
with open(file_path, 'r', encoding='utf-8') as f: w20 = json.load(f)

for n in w20.get('nodes', []):
    json_n = json.dumps(n)
    if "PAGE_ID_AQUI" in json_n or "INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI" in json_n:
        if "url" in n.get("parameters", {}):
            n["parameters"]["url"] = n["parameters"]["url"].replace("PAGE_ID_AQUI", "379537031716700").replace("INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI", "379537031716700")
    if "CHAT_ID_AQUI" in json_n:
        if "chatId" in n.get("parameters", {}):
            n["parameters"]["chatId"] = n["parameters"]["chatId"].replace("CHAT_ID_AQUI", "-1002012015091")

payload = {
    "name": w20.get("name"),
    "nodes": w20.get("nodes", []),
    "connections": w20.get("connections", {}),
    "settings": w20.get("settings", {}),
    "active": True
}

# 1. Obter ID do VPS
workflow_id = "publicadorSocialDlNexusV320260518"

# 2. Fazer Deploy
res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=payload)
if err:
    print(f"Erro ao fazer deploy: {err}")
    exit(1)
print("Deploy feito com sucesso!")

# 3. Disparar Webhook
webhook_url = n8n_host.replace("/api/v1/", "/webhook/disparo-automatico-020")
print(f"Chamando webhook: {webhook_url}")
try:
    req = urllib.request.Request(webhook_url, method="GET")
    ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
        print(f"DISPARO CONCLUÍDO! Status: {response.status}")
except Exception as e:
    print(f"Erro no disparo: {e}")
