import os
import sys
import json
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

wf_id = '1ndeOglNFeEKvXAT'
r = requests.get(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
wf = r.json()

for node in wf.get('nodes', []):
    if node.get('name') == 'Supabase Update':
        print("Antes da substituicao:")
        print(json.dumps(node, indent=2))
        
        # Vamos reescrever o node para typeVersion: 1 e a estrutura exata do 061
        node['typeVersion'] = 1
        node['parameters'] = {
            "operation": "update",
            "schema": "public",
            "table": "drive_zelador_inventory",
            "matchColumns": "file_id",
            "columns": "categoria_sugerida,pasta_destino_sugerida,confianca,risco,precisa_revisao_humana,motivo_classificacao,acao_sugerida,status",
            "options": {}
        }
        
        print("\nDepois da substituicao:")
        print(json.dumps(node, indent=2))

allowed_settings_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']
clean_settings = {k: wf['settings'][k] for k in allowed_settings_keys if k in wf.get('settings', {})}

payload = {
    "name": wf.get('name'),
    "nodes": wf.get('nodes'),
    "connections": wf.get('connections'),
    "settings": clean_settings
}

put_r = requests.put(f"{host}/workflows/{wf_id}", json=payload, headers=headers, verify=False, timeout=15)
print(f"\nPUT Status: {put_r.status_code}")

act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
if act_r.status_code == 200:
    print(f"[ATIVADO] AGENTE_ZELADOR_CLASSIFICADOR_V1 esta VERDE!")
else:
    msg = act_r.json().get('message', act_r.text[:300]) if act_r.text else 'N/A'
    print(f"[FALHA ATIVACAO] {msg}")
