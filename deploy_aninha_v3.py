import os
import json
import urllib.request
import urllib.error
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

n8n_api_key = os.environ.get('N8N_API_KEY')
n8n_host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/"

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\002_roteador_aninha_v3_personas.json"

print("Iniciando deploy do Workflow Aninha V3 Atendimento...")

existing_workflows = {}
try:
    req = urllib.request.Request(n8n_host + "workflows", headers=headers, method="GET")
    resp = urllib.request.urlopen(req, context=ctx)
    data = json.loads(resp.read().decode('utf-8'))
    for wf in data.get('data', []):
        existing_workflows[wf.get('name')] = wf.get('id')
except Exception as e:
    print(f"Erro ao obter workflows: {e}")

try:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    workflow_data = json.loads(content)
    
    wf_name = workflow_data.get('name')
    if 'id' in workflow_data: del workflow_data['id']
    if 'active' in workflow_data: del workflow_data['active']
    if 'tags' in workflow_data: del workflow_data['tags']
    if 'pinData' in workflow_data: del workflow_data['pinData']
    if 'versionId' in workflow_data: del workflow_data['versionId']
    if 'meta' in workflow_data: del workflow_data['meta']
    
    data_bytes = json.dumps(workflow_data).encode('utf-8')
    server_id = existing_workflows.get(wf_name)
    
    if server_id:
        req_put = urllib.request.Request(n8n_host + f"workflows/{server_id}", data=data_bytes, headers=headers, method="PUT")
        resp = urllib.request.urlopen(req_put, context=ctx)
        print(f"[{wf_name}] Atualizado com sucesso (ID: {server_id}).")
    else:
        req_post = urllib.request.Request(n8n_host + "workflows", data=data_bytes, headers=headers, method="POST")
        resp = urllib.request.urlopen(req_post, context=ctx)
        resp_data = json.loads(resp.read().decode('utf-8'))
        server_id = resp_data.get('id')
        print(f"[{wf_name}] Criado com sucesso (Novo ID: {server_id}).")
        
    if server_id:
        v2_server_id = existing_workflows.get("002_roteador_aninha_v2")
        if v2_server_id:
            req_deactivate = urllib.request.Request(n8n_host + f"workflows/{v2_server_id}/deactivate", data=b'{}', headers=headers, method="POST")
            try: urllib.request.urlopen(req_deactivate, context=ctx)
            except: pass
            print(f"[002_roteador_aninha_v2] DESATIVADO para evitar conflitos (ID: {v2_server_id}).")
        
        v_kill = existing_workflows.get("002_roteador_aninha_v3_killcritic")
        if v_kill:
            req_deactivate3 = urllib.request.Request(n8n_host + f"workflows/{v_kill}/deactivate", data=b'{}', headers=headers, method="POST")
            try: urllib.request.urlopen(req_deactivate3, context=ctx)
            except: pass
            print(f"[002_roteador_aninha_v3_killcritic] DESATIVADO para evitar conflitos (ID: {v_kill}).")
            
        req_activate = urllib.request.Request(n8n_host + f"workflows/{server_id}/activate", data=b'{}', headers=headers, method="POST")
        urllib.request.urlopen(req_activate, context=ctx)
        print(f"[{wf_name}] ATIVADO para produção.")
        
except urllib.error.HTTPError as e:
    resp_text = e.read().decode('utf-8')
    print(f"[{wf_name}] Erro API: {e.code} - {resp_text}")
except Exception as e:
    print(f"[{wf_name}] Erro geral: {e}")
