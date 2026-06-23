import json
import os
import requests
import urllib.parse
import re

env_path = r'd:\AntiGravity\projeto_01\.env'

env_content = open(env_path, 'rb').read()
try:
    env_text = env_content.decode('utf-8')
except UnicodeDecodeError:
    env_text = env_content.decode('utf-16')

n8n_host = None
n8n_key = None

for line in env_text.splitlines():
    line = line.strip()
    if line.startswith('N8N_HOST='):
        n8n_host = line.split('=', 1)[1]
    elif line.startswith('N8N_API_KEY='):
        n8n_key = line.split('=', 1)[1]

files = [
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\019_GERADOR_ORCAMENTO_RAPIDO.json',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\179_TESTES_PRECIFICACAO.json'
]

headers = {
    'X-N8N-API-KEY': n8n_key,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

def get_workflow_id(name):
    url = f"{n8n_host}/workflows"
    resp = requests.get(url, headers=headers, verify=False)
    if resp.status_code == 200:
        workflows = resp.json().get('data', [])
        for wf in workflows:
            if wf.get('name') == name:
                return wf.get('id')
    return None

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # payload for API
    payload = {
        "name": data.get("name"),
        "nodes": data.get("nodes", []),
        "connections": data.get("connections", {}),
        "settings": data.get("settings", {})
    }
    
    wf_name = data.get('name')
    wf_id = data.get('id') or get_workflow_id(wf_name)
    
    if wf_id:
        url = f"{n8n_host}/workflows/{wf_id}"
        resp = requests.put(url, headers=headers, json=payload, verify=False)
        if resp.status_code == 200:
            print(f"Updated workflow {wf_name} on n8n")
        else:
            print(f"Failed to update {wf_name}: {resp.text}")
            
        activate_url = f"{n8n_host}/workflows/{wf_id}/activate"
        activate_resp = requests.post(activate_url, headers=headers, verify=False)
        if activate_resp.status_code == 200:
            print(f"Activated {wf_name}")
        else:
            print(f"Failed to activate {wf_name}: {activate_resp.text}")
    else:
        url = f"{n8n_host}/workflows"
        resp = requests.post(url, headers=headers, json=payload, verify=False)
        if resp.status_code == 200:
            print(f"Created workflow {wf_name} on n8n")
            new_id = resp.json().get('id')
            data['id'] = new_id
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
            activate_url = f"{n8n_host}/workflows/{new_id}/activate"
            activate_resp = requests.post(activate_url, headers=headers, verify=False)
            if activate_resp.status_code == 200:
                print(f"Activated {wf_name}")
            else:
                print(f"Failed to activate {wf_name}: {activate_resp.text}")
        else:
            print(f"Failed to create {wf_name}: {resp.text}")
