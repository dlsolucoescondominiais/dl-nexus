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
        print(f"Total workflows: {len(workflows)}")
        for wf in workflows:
            wf_id = wf.get('id')
            wf_name = wf.get('name')
            active = wf.get('active', False)
            
            # Fetch workflow details
            det_req = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers)
            with urllib.request.urlopen(det_req, context=ctx) as det_res:
                det = json.loads(det_res.read().decode('utf-8'))
                nodes = det.get('nodes', [])
                supabase_nodes = [n for n in nodes if 'supabase' in n.get('type', '').lower()]
                postgres_nodes = [n for n in nodes if 'postgres' in n.get('type', '').lower()]
                
                if supabase_nodes or postgres_nodes:
                    print(f"Workflow: {wf_name} (ID: {wf_id}, Active: {active})")
                    if supabase_nodes:
                        print(f"  - Supabase nodes: {[n.get('name') for n in supabase_nodes]}")
                        for sn in supabase_nodes:
                            creds = sn.get('credentials', {})
                            print(f"    Credentials: {creds}")
                    if postgres_nodes:
                        print(f"  - Postgres nodes: {[n.get('name') for n in postgres_nodes]}")
                        for pn in postgres_nodes:
                            creds = pn.get('credentials', {})
                            print(f"    Credentials: {creds}")
except Exception as e:
    print("Error:", e)
