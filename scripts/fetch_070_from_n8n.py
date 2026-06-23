import os
"""
[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.
Este script foi desativado.
"""
import sys
sys.exit("Script obsoleto. Manus.IA foi removido.")

import urllib.request, json, ssl

key=os.environ.get('N8N_API_KEY')
host = 'https://n8n.dlsolucoescondominiais.com.br/api/v1/'
headers = {'X-N8N-API-KEY': key, 'Accept': 'application/json'}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# List workflows to find 070 / Manus
url = host + 'workflows'
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as response:
    data = json.loads(response.read().decode('utf-8'))
    for wf in data.get('data', []):
        name = wf.get('name', '')
        if '070' in name or 'manus' in name.lower() or 'Manus' in name:
            wf_id = wf.get('id')
            print(f"ID: {wf_id} | Name: {name} | Active: {wf.get('active')}")

            # Get full workflow
            wf_url = host + 'workflows/' + wf_id
            wf_req = urllib.request.Request(wf_url, headers=headers)
            with urllib.request.urlopen(wf_req, context=ctx) as wf_resp:
                wf_data = json.loads(wf_resp.read().decode('utf-8'))
                # Save to file
                with open('d:/AntiGravity/projeto_01/scripts/070_FROM_N8N_SERVER.json', 'w', encoding='utf-8') as f:
                    json.dump(wf_data, f, ensure_ascii=False, indent=2)
                print(f"Saved full workflow to scripts/070_FROM_N8N_SERVER.json")
                print(f"Nodes: {[n.get('name') for n in wf_data.get('nodes', [])]}")
