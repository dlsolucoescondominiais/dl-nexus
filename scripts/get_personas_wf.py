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

req = urllib.request.Request(n8n_host + "workflows/9z7YqzTNT9CspxG1", headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        wf = json.loads(response.read().decode('utf-8'))
        for node in wf.get('nodes', []):
            if 'Ler Persona Supabase' in node.get('name') or 'supabase' in node.get('type', '').lower():
                print(json.dumps(node, indent=2))
except Exception as e:
    print("Error:", e)
