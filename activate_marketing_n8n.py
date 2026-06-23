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

print("Buscando workflows para ativacao...")

workflows, err = n8n_request("workflows")
if err:
    print(f"Erro: {err}")
    exit(1)

# Ativa qualquer workflow que contenha essas palavras chave
keywords = ["081", "082", "083", "084", "085", "020", "PUBLICADOR", "DISPATCHER", "SOCIAL"]
to_activate = []

for w in workflows.get('data', []):
    name = w.get('name', '').upper()
    if any(k in name for k in keywords):
        to_activate.append((w.get('id'), w.get('name')))

if not to_activate:
    print("Nenhum workflow compativel encontrado.")
else:
    for wid, wname in to_activate:
        print(f"Ativando: {wname} ({wid})...")
        res, err = n8n_request(f"workflows/{wid}/activate", method="POST", data={})
        if err:
            print(f"Erro ao ativar {wname}: {err}")
        else:
            print(f"SUCESSO: {wname} ativado.")

print("Processo finalizado.")
