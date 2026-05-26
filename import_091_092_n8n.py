import os
import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Load N8N API credentials from .env
n8n_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwNzdmNjJhYS1jNWRkLTQzMWMtYTM5Ny0zZWIwODc0NWQ1MzkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiZTc5OTEzYTQtYmU3NC00MGM1LWE4ZWEtZGZjZDM0Yjk1YmMzIiwiaWF0IjoxNzc0MDYyNjkwfQ.Y9foixG4yeuezhSgZ_6iZYvHGLkKw2sjRR1Eyy6sWXw"
n8n_host = "https://n8n.dlsolucoescondominiais.com.br/api/v1"

if not n8n_host.endswith('/'):
    n8n_host += '/'

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

workflows_dir = "DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS"

id_map = {
    "091": "sentinelaAuditoriaN8nDlNexus091",
    "092": "mesaAprovacaoTelegramAninha092"
}

imported_workflows = []

print("Iniciando importação 091 e 092 para n8n...")

for filename in os.listdir(workflows_dir):
    prefix = filename[:3]
    if prefix in id_map:
        filepath = os.path.join(workflows_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            workflow_data = json.loads(content)
        except json.JSONDecodeError:
            print(f"[{filename}] JSON Inválido.")
            continue

        workflow_id = id_map[prefix]
        
        # Limpar id, active e tags para permitir criação via API (n8n rules)
        if 'id' in workflow_data:
            del workflow_data['id']
        if 'active' in workflow_data:
            del workflow_data['active']
        if 'tags' in workflow_data:
            del workflow_data['tags']
            
        data_bytes = json.dumps(workflow_data).encode('utf-8')
        
        try:
            req_post = urllib.request.Request(n8n_host + "workflows", data=data_bytes, headers=headers, method="POST")
            resp = urllib.request.urlopen(req_post, context=ctx)
            print(f"[{filename}] Criado com sucesso via POST.")
            imported_workflows.append(filename)
        except urllib.error.HTTPError as e:
            resp_text = e.read().decode('utf-8')
            print(f"[{filename}] Erro POST: {e.code} - {resp_text}")
        except Exception as e:
            print(f"[{filename}] Erro geral: {e}")

print(f"Workflows importados: {imported_workflows}")
