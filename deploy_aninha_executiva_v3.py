import os
import urllib.request, json, ssl, os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows"
headers = {'X-N8N-API-KEY': key, 'Content-Type': 'application/json'}

wfs = [
    r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\152_ANINHA_VOZ_AGENDA.json",
    r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\153_ANINHA_RELATORIO_SEMANAL.json",
    r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\154_ANINHA_GESTORA_EMAILS.json"
]

for filepath in wfs:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            workflow_data = json.loads(f.read())
        
        # Strip placeholder credentials
        for node in workflow_data.get('nodes', []):
            if 'credentials' in node:
                keys_to_delete = []
                for cred_key, cred_val in node['credentials'].items():
                    if 'placeholder' in cred_val.get('id', ''):
                        keys_to_delete.append(cred_key)
                for k in keys_to_delete:
                    del node['credentials'][k]
                if not node['credentials']:
                    del node['credentials']

        wf_name = workflow_data.get('name')
        if 'id' in workflow_data: del workflow_data['id']
        if 'active' in workflow_data: del workflow_data['active']
        if 'tags' in workflow_data: del workflow_data['tags']
        if 'pinData' in workflow_data: del workflow_data['pinData']
        if 'versionId' in workflow_data: del workflow_data['versionId']
        if 'meta' in workflow_data: del workflow_data['meta']
        
        data_bytes = json.dumps(workflow_data).encode('utf-8')
        
        # Always POST to create new
        req_post = urllib.request.Request(host, data=data_bytes, headers=headers, method="POST")
        resp = urllib.request.urlopen(req_post, context=ctx)
        resp_data = json.loads(resp.read().decode('utf-8'))
        server_id = resp_data.get('id')
        print(f"[{wf_name}] Criado com sucesso (Novo ID: {server_id}).")
            
        req_activate = urllib.request.Request(f"{host}/{server_id}/activate", data=b'{}', headers=headers, method="POST")
        urllib.request.urlopen(req_activate, context=ctx)
        print(f"[{wf_name}] ATIVADO para produção.")
            
    except urllib.error.HTTPError as e:
        print(f"Erro em {filepath}: {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"Erro em {filepath}: {e}")
