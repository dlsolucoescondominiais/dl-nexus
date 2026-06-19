import os
import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

n8n_api_key = os.getenv("N8N_API_KEY", "")
n8n_host = "https://n8n.dlsolucoescondominiais.com.br/api/v1"

if not n8n_host.endswith('/'):
    n8n_host += '/'

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

base_dir = "DL_NEXUS_V3_LOCAL"

print("Iniciando deploy de TODAS as rotinas (recursivo) para n8n...")

existing_workflows = {}
try:
    req = urllib.request.Request(n8n_host + "workflows", headers=headers, method="GET")
    resp = urllib.request.urlopen(req, context=ctx)
    data = json.loads(resp.read().decode('utf-8'))
    for wf in data.get('data', []):
        existing_workflows[wf.get('name')] = wf.get('id')
    print(f"Obtidos {len(existing_workflows)} workflows do n8n.")
except Exception as e:
    print(f"Erro ao obter workflows: {e}")

imported_workflows = []

for root, _, files in os.walk(base_dir):
    for filename in files:
        if not filename.endswith('.json'):
            continue
        filepath = os.path.join(root, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        try:
            workflow_data = json.loads(content)
        except json.JSONDecodeError:
            continue

        if not isinstance(workflow_data, dict) or 'nodes' not in workflow_data or 'connections' not in workflow_data:
            continue

        wf_name = workflow_data.get('name')
        if not wf_name:
            wf_name = filename.replace('.json', '')
            workflow_data['name'] = wf_name

        if 'id' in workflow_data:
            del workflow_data['id']
        if 'active' in workflow_data:
            del workflow_data['active']
        if 'tags' in workflow_data:
            del workflow_data['tags']
        if 'pinData' in workflow_data:
            del workflow_data['pinData']
        if 'versionId' in workflow_data:
            del workflow_data['versionId']
        if 'meta' in workflow_data:
            del workflow_data['meta']
            
        data_bytes = json.dumps(workflow_data).encode('utf-8')
        server_id = existing_workflows.get(wf_name)
        
        try:
            if server_id:
                req_put = urllib.request.Request(n8n_host + f"workflows/{server_id}", data=data_bytes, headers=headers, method="PUT")
                resp = urllib.request.urlopen(req_put, context=ctx)
                print(f"[{filename}] Atualizado com sucesso (ID: {server_id}).")
            else:
                req_post = urllib.request.Request(n8n_host + "workflows", data=data_bytes, headers=headers, method="POST")
                resp = urllib.request.urlopen(req_post, context=ctx)
                resp_data = json.loads(resp.read().decode('utf-8'))
                server_id = resp_data.get('id')
                existing_workflows[wf_name] = server_id
                print(f"[{filename}] Criado com sucesso (Novo ID: {server_id}).")
                
            if server_id:
                req_activate = urllib.request.Request(n8n_host + f"workflows/{server_id}/activate", data=b'{}', headers=headers, method="POST")
                urllib.request.urlopen(req_activate, context=ctx)
                print(f"[{filename}] ATIVADO para testes.")
                imported_workflows.append(filename)
                
        except urllib.error.HTTPError as e:
            resp_text = e.read().decode('utf-8')
            print(f"[{filename}] Erro API: {e.code} - {resp_text}")
        except Exception as e:
            print(f"[{filename}] Erro geral: {e}")

print("\n--- DEPLOY E ATIVACAO CONCLUIDOS ---")
print(f"Total processados com sucesso: {len(imported_workflows)}")
