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

def save_wf(wf_id, filename):
    req = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            wf = json.loads(response.read().decode('utf-8'))
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(wf, f, indent=2, ensure_ascii=False)
            print(f"[+] Saved {filename}")
    except Exception as e:
        print(f"[-] Error saving {wf_id}: {e}")

# Find workflow 001
req_list = urllib.request.Request(n8n_host + "workflows", headers=headers)
try:
    with urllib.request.urlopen(req_list, context=ctx) as response:
        res = json.loads(response.read().decode('utf-8'))
        workflows = res.get('data', [])
        for wf in workflows:
            wf_name = wf.get('name', '')
            wf_id = wf.get('id')
            if '001_TELEGRAM_RECEPCAO_ANINHA_V3' in wf_name or '001_' in wf_name and 'recepcao' in wf_name.lower():
                print(f"Found 001: {wf_name} (ID: {wf_id})")
                save_wf(wf_id, 'scripts/001_TELEGRAM_RECEPCAO_ANINHA_V3_REMOTE.json')
            elif wf_id == 'NgXUbJ96dXJqxGGX' or '002_roteador_aninha_v3_atendimento' in wf_name:
                print(f"Found 002: {wf_name} (ID: {wf_id})")
                save_wf(wf_id, 'scripts/002_roteador_aninha_v3_atendimento_REMOTE.json')
except Exception as e:
    print("Error:", e)
