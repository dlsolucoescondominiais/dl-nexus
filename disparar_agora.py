import os
import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
upload_filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

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
