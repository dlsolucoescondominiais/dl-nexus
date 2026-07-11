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

print("\n[1/4] Criando credencial Google Calendar OAuth2...")

cred_payload = {
    "name": "Google Calendar DL Nexus",
    "type": "googleCalendarOAuth2Api",
    "data": {
        "clientId": os.getenv('GOOGLE_OAUTH_CLIENT_ID_TEST', ''),
        "clientSecret": os.getenv('GOOGLE_OAUTH_CLIENT_SECRET_TEST', ''),
        "serverUrl": "https://n8n.dlsolucoescondominiais.com.br",
        "sendAdditionalBodyProperties": False,
        "additionalBodyProperties": {}
    }
}

cr = requests.post(f"{host}/credentials", json=cred_payload, headers=headers, verify=False, timeout=15)
print(f"   Status: {cr.status_code}")
print(f"   Response: {cr.text[:500]}")

if cr.status_code in (200, 201):
    cred_data = cr.json()
    cred_id = cred_data.get('id')
    print(f"   Credencial criada com ID: {cred_id}")
    
    # 2. Injetar no workflow
    print(f"\n[2/4] Buscando workflow 152_ANINHA_VOZ_AGENDA...")
    wf_id = 'ZJ9F3OIfw9k8psJw'
    r2 = requests.get(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
    wf = r2.json()
    
    for node in wf.get('nodes', []):
        node_type = node.get('type', '')
        node_name = node.get('name', '')
        if 'googleCalendar' in node_type.lower() or 'calendar' in node_name.lower():
            node['credentials'] = node.get('credentials', {})
            node['credentials']['googleCalendarOAuth2Api'] = {
                'id': cred_id,
                'name': 'Google Calendar DL Nexus'
            }
            print(f"   [INJETADO] Node [{node_name}] <- googleCalendarOAuth2Api")
    
    # 3. PUT
    print(f"\n[3/4] Atualizando workflow...")
    allowed_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']
    clean_settings = {k: wf['settings'][k] for k in allowed_keys if k in wf.get('settings', {})}
    payload = {"name": wf['name'], "nodes": wf['nodes'], "connections": wf['connections'], "settings": clean_settings}
    put_r = requests.put(f"{host}/workflows/{wf_id}", json=payload, headers=headers, verify=False, timeout=15)
    print(f"   PUT Status: {put_r.status_code}")
    
    # 4. Ativar
    print(f"\n[4/4] Ativando...")
    act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
    if act_r.status_code == 200:
        print(f"   [ATIVADO] 152_ANINHA_VOZ_AGENDA VERDE!")
    else:
        msg = act_r.json().get('message', '')[:300] if act_r.text else 'N/A'
        print(f"   [FALHA] {msg}")
else:
    print(f"   Falhou.")

# Contagem final
print(f"\n{'='*60}")
r3 = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
wfs = r3.json().get('data', [])
ativos = len([w for w in wfs if w.get('active')])
total = len(wfs)
print(f"Total: {total} | Ativos: {ativos} | Inativos: {total - ativos}")
print(f"Taxa operacional: {round(ativos/total*100)}%")
