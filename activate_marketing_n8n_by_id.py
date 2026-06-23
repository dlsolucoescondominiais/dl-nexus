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

print("Iniciando Ativacao da Esteira de Marketing no n8n (Por IDs Absolutos)...")

# Esses sao os IDs raiz exatos forçados no deploy
required_ids = [
    "publicadorInstagramMetaApi081DlNexus20260522", # 081
    "l7oOmPyRJVsdz7r0",                             # 082 ja estava assim, ok
    "publicadorFacebookMetaApi082DlNexus20260522",  # 082 (novo padrao)
    "publicadorGoogleBusiness083DlNexus20260522",   # 083
    "HafnpJDL0AsP5fNh",                             # 084 ja estava assim, ok
    "publicadorTiktokAssistido084DlNexus20260522",  # 084 (novo padrao)
    "socialDispatcher085DlNexus20260522",           # 085
    "publicadorSocialDlNexusV320260518"             # 020
]

for wid in required_ids:
    print(f"Tentando ativar workflow ID: {wid} ...")
    res, err = n8n_request(f"workflows/{wid}/activate", method="POST", data={})
    if err:
        print(f"Ignorado ou erro ao ativar ID {wid}: {err}")
    else:
        print(f"SUCESSO: Workflow ID {wid} ativado.")

print("Processo finalizado.")
