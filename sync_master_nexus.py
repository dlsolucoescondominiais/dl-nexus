import os
import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
UPLOAD_DIR = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N"

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
            return json.loads(response.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

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
