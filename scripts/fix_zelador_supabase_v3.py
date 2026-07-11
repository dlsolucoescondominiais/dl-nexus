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
        # Reescrever usando typeVersion 2 (a API nova que sabemos que funciona no painel)
        node['typeVersion'] = 2
        node['parameters'] = {
            "operation": "update",
            "tableId": "drive_zelador_inventory",
            "dataToSend": "defineBelow",
            "fieldsUi": {
                "fieldValues": [
                    {"name": "categoria_sugerida", "value": "={{ $json.categoria_sugerida }}"},
                    {"name": "pasta_destino_sugerida", "value": "={{ $json.pasta_destino_sugerida }}"},
                    {"name": "confianca", "value": "={{ $json.confianca }}"},
                    {"name": "risco", "value": "={{ $json.risco }}"},
                    {"name": "precisa_revisao_humana", "value": "={{ $json.precisa_revisao_humana }}"},
                    {"name": "motivo_classificacao", "value": "={{ $json.motivo_classificacao }}"},
                    {"name": "acao_sugerida", "value": "={{ $json.acao_sugerida }}"},
                    {"name": "status", "value": "={{ $json.status }}"}
                ]
            },
            "filters": {
                "conditions": [
                    {
                        "keyName": "file_id",
                        "condition": "equals",
                        "keyValue": "={{ $json.file_id }}"
                    }
                ]
            }
        }
        print("Substituido por typeVersion: 2 (Supabase moderno)")

allowed_settings_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']
clean_settings = {k: wf['settings'][k] for k in allowed_settings_keys if k in wf.get('settings', {})}

payload = {
    "name": wf.get('name'),
    "nodes": wf.get('nodes'),
    "connections": wf.get('connections'),
    "settings": clean_settings
}

put_r = requests.put(f"{host}/workflows/{wf_id}", json=payload, headers=headers, verify=False, timeout=15)
print(f"PUT Status: {put_r.status_code}")

act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
if act_r.status_code == 200:
    print(f"[ATIVADO] AGENTE_ZELADOR_CLASSIFICADOR_V1 esta VERDE!")
else:
    msg = act_r.json().get('message', act_r.text[:300]) if act_r.text else 'N/A'
    print(f"[FALHA ATIVACAO] {msg}")
