import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
host = 'https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows'
req = urllib.request.Request(host, headers={'X-N8N-API-KEY':key})
data = json.loads(urllib.request.urlopen(req, context=ctx).read())['data']
marketing_wfs = [w for w in data if 'PUBLICADOR' in w['name'] or 'POST_GOOGLE' in w['name']]

with open('marketing_analysis.txt', 'w', encoding='utf-8') as f:
    for w in marketing_wfs:
        f.write(f"--- {w['name']}\n")
        try:
            wf = json.loads(urllib.request.urlopen(urllib.request.Request(f"{host}/{w['id']}", headers={'X-N8N-API-KEY':key}), context=ctx).read())
            for n in wf.get('nodes', []):
                if 'n8n-nodes-base' in n['type']:
                    cred_info = "NO_CREDS"
                    if 'credentials' in n:
                        cred_info = str(list(n['credentials'].keys()))
                    f.write(f"  Node: {n['name']} | Type: {n['type']} | Creds: {cred_info}\n")
        except Exception as e:
            f.write(f"Error fetching {w['name']}: {e}\n")
