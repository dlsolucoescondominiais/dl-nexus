import os
import urllib.request, json, ssl

key=os.environ.get('N8N_API_KEY')
host = 'https://n8n.dlsolucoescondominiais.com.br/api/v1/'
headers = {'X-N8N-API-KEY': key, 'Accept': 'application/json'}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Fetch the ORIGINAL 070 workflow (UBH2RWc3CK2AyVR3)
wf_id = 'UBH2RWc3CK2AyVR3'
wf_url = host + 'workflows/' + wf_id
wf_req = urllib.request.Request(wf_url, headers=headers)
with urllib.request.urlopen(wf_req, context=ctx) as wf_resp:
    wf_data = json.loads(wf_resp.read().decode('utf-8'))
    with open('d:/AntiGravity/projeto_01/scripts/070_ORIGINAL_FROM_N8N.json', 'w', encoding='utf-8') as f:
        json.dump(wf_data, f, ensure_ascii=False, indent=2)
    print("Saved ORIGINAL 070 to scripts/070_ORIGINAL_FROM_N8N.json")
    for n in wf_data.get('nodes', []):
        print(f"  Node: {n.get('name')} | Type: {n.get('type')}")
        if n.get('type') == 'n8n-nodes-base.httpRequest':
            params = n.get('parameters', {})
            print(f"    URL: {params.get('url')}")
            hps = params.get('headerParameters', {}).get('parameters', [])
            for h in hps:
                name_val = h.get('name', '')
                val = h.get('value', '')
                # Mask any secrets
                if 'key' in name_val.lower() or 'auth' in name_val.lower() or 'token' in name_val.lower():
                    if len(val) > 20:
                        val = val[:10] + '***MASKED***' + val[-4:]
                print(f"    Header: {name_val} = {val}")
