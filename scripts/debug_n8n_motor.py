import urllib.request
import json
import ssl

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
    "Content-Type": "application/json",
    "Accept": "application/json"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

wf_id = "NgXUbJ96dXJqxGGX"
req = urllib.request.Request(n8n_host + f"executions?workflowId={wf_id}&limit=1", headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        if data and data.get('data'):
            exec_id = data['data'][0]['id']
            print(f"[+] Found execution ID: {exec_id}")
            det_req = urllib.request.Request(n8n_host + f"executions/{exec_id}?includeData=true", headers=headers)
            with urllib.request.urlopen(det_req, context=ctx) as det_res:
                details = json.loads(det_res.read().decode('utf-8'))
                with open("scripts/motor_execution_error.json", "w", encoding="utf-8") as out_f:
                    json.dump(details, out_f, indent=2, ensure_ascii=False)
                print("[+] Detailed execution log saved to scripts/motor_execution_error.json")
        else:
            print("[-] No executions found.")
except Exception as e:
    print(f"[-] Error: {e}")
