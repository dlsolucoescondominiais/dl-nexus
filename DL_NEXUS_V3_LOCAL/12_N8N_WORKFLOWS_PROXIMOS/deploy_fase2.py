import os
import json
import urllib.request
import ssl
from dotenv import load_dotenv

load_dotenv(r'd:\AntiGravity\projeto_01\.env')

api_key = os.environ.get('N8N_API_KEY')
host = os.environ.get('N8N_HOST')
workflows_dir = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def deploy(file_name):
    with open(os.path.join(workflows_dir, f"{file_name}.json"), 'r', encoding='utf-8') as f:
        wf = json.load(f)
    
    if 'active' in wf:
        del wf['active']
    
    req = urllib.request.Request(f'{host}/workflows', method='POST')
    req.add_header('X-N8N-API-KEY', api_key)
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(wf).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, data=data, context=ctx) as res:
            resp = json.loads(res.read().decode('utf-8'))
            print(f"Deployed {file_name}: {resp['id']}")
            return resp['id']
    except urllib.error.HTTPError as e:
        print(f"Error deploying {file_name}:", e.code, e.read().decode('utf-8'))
        return None

id_051 = deploy("051_ANINHA_SOCIAL_MEMORIA_SUPABASE")
id_052 = deploy("052_ANINHA_SOCIAL_RESPOSTA_META")
id_053 = deploy("053_ANINHA_SOCIAL_HANDOFF_TELEGRAM")
id_054 = deploy("054_ANINHA_SOCIAL_RELATORIO_DIARIO")

if id_051 and id_052 and id_053:
    # Update 050 with the IDs
    with open(os.path.join(workflows_dir, "050_AGENTE_SDR_SOCIAL_DL.json"), 'r', encoding='utf-8') as f:
        wf_050 = json.load(f)
    
    for node in wf_050['nodes']:
        if node['name'] == 'CALL_051_MEMORIA':
            node['parameters']['workflowId'] = id_051
        elif node['name'] == 'CALL_052_RESPOSTA':
            node['parameters']['workflowId'] = id_052
        elif node['name'] == 'CALL_053_HANDOFF':
            node['parameters']['workflowId'] = id_053
            
    with open(os.path.join(workflows_dir, "050_AGENTE_SDR_SOCIAL_DL.json"), 'w', encoding='utf-8') as f:
        json.dump(wf_050, f, indent=2, ensure_ascii=False)
        
    # Deploy 050
    id_050 = deploy("050_AGENTE_SDR_SOCIAL_DL")
    
    # Activate 050
    if id_050:
        req = urllib.request.Request(f'{host}/workflows/{id_050}/activate', method='POST')
        req.add_header('X-N8N-API-KEY', api_key)
        try:
            urllib.request.urlopen(req, context=ctx)
            print("Workflow 050 activated successfully.")
        except Exception as e:
            print("Failed to activate 050:", e)
