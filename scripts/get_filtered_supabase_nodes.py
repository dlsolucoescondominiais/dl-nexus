import urllib.request, json, ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Accept": "application/json"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request(n8n_host + "workflows", headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        res = json.loads(response.read().decode('utf-8'))
        workflows = res.get('data', [])
        for wf in workflows:
            wf_id = wf.get('id')
            det_req = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers)
            with urllib.request.urlopen(det_req, context=ctx) as det_res:
                det = json.loads(det_res.read().decode('utf-8'))
                for node in det.get('nodes', []):
                    if 'supabase' in node.get('type', '').lower():
                        params = node.get('parameters', {})
                        if 'filters' in params:
                            print(f"Workflow: {wf.get('name')} | Node: {node.get('name')}")
                            print(json.dumps(node, indent=2))
except Exception as e:
    print("Error:", e)
