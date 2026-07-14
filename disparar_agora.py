import os
from utils.n8n_api import n8n_request, get_n8n_credentials

import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
upload_filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

n8n_host, n8n_api_key = get_n8n_credentials()
print("Deploying Workflow 020 automatico...")

with open(upload_filepath, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

for key in ['id', 'active', 'tags', 'pinData', 'versionId', 'meta', 'settings']:
    data.pop(key, None)
data['settings'] = {}

workflow_id = "publicadorSocialDlNexusV320260518"

res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=data)
if err:
    print(f"Erro ao atualizar: {err}")
    exit(1)
print("Workflow atualizado na VPS.")

print("Acionando a maquina!")

webhook_url = n8n_host.replace("/api/v1/", "/webhook/disparo-automatico")

try:
    req = urllib.request.Request(webhook_url, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"POSTAGEM DISPARADA COM SUCESSO! Status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Erro no webhook: HTTP {e.code}")
except Exception as e:
    print(f"Erro no disparo: {e}")
