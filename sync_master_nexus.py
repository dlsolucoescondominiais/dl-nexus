import os
import json
import urllib.request
import urllib.error
import ssl
from n8n_utils import load_n8n_config, n8n_request as n8n_request_alias

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
UPLOAD_DIR = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N"


n8n_host, n8n_api_key = load_n8n_config(ENV_FILE)

def n8n_request(endpoint, method="GET", data=None, timeout=None):
    return n8n_request_alias(endpoint, n8n_host, n8n_api_key, method, data, timeout=timeout)

print("Iniciando Sincronizacao Master DL Nexus V3 com n8n...")

prefixes_to_deploy = ["130", "131", "132", "133", "134", "135", "170", "171", "172", "173", "174", "175", "176", "177", "178", "179"]

for file in os.listdir(UPLOAD_DIR):
    if not file.endswith(".json"): continue
    
    is_target = any(file.startswith(prefix) for prefix in prefixes_to_deploy)
    if not is_target: continue

    filepath = os.path.join(UPLOAD_DIR, file)
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            data = json.loads(f.read())
        except json.JSONDecodeError:
            continue
            
    # Purge read-only properties
    for key in ['id', 'active', 'tags', 'pinData', 'versionId', 'meta']:
        data.pop(key, None)
        
    # The API requires 'settings' to exist, but 176 had invalid properties.
    # Therefore, we override it to an empty dictionary, which satisfies both rules.
    data['settings'] = {}
    
    search_res, err = n8n_request("workflows")
    if err:
        print(f"Erro API n8n: {err}")
        break
        
    server_id = None
    for w in search_res.get('data', []):
        if w.get('name') == data.get('name', file):
            server_id = w.get('id')
            break
            
    if server_id:
        res, err = n8n_request(f"workflows/{server_id}", method="PUT", data=data)
        if err:
            print(f"Erro ao atualizar {file}: {err}")
        else:
            print(f"Atualizado: {file}")
    else:
        res, err = n8n_request("workflows", method="POST", data=data)
        if err:
            print(f"Erro ao criar {file}: {err}")
        else:
            print(f"Criado: {file}")

print("Sincronizacao n8n concluida com correcoes de settings.")
