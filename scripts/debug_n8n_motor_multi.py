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
req = urllib.request.Request(n8n_host + f"executions?workflowId={wf_id}&limit=10", headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"[*] Found {len(data.get('data', []))} executions.")
        for execution in data.get('data', []):
            exec_id = execution.get('id')
            status = execution.get('status')
            created_at = execution.get('startedAt') or execution.get('createdAt') or "unknown"
            print(f"    Execution ID: {exec_id} | Status: {status} | Created At: {created_at}")
            if status == "error" and exec_id:
                det_req = urllib.request.Request(n8n_host + f"executions/{exec_id}?includeData=true", headers=headers)
                with urllib.request.urlopen(det_req, context=ctx) as det_res:
                    details = json.loads(det_res.read().decode('utf-8'))
                    failed_node = "Unknown"
                    error_msg = "Unknown"
                    run_data = details.get('data', {}).get('resultData', {}).get('runData', {})
                    for node_name, node_runs in run_data.items():
                        for run in node_runs:
                            if run.get('executionStatus') == 'error':
                                failed_node = node_name
                                error_msg = run.get('error', {}).get('message', 'No message')
                                break
                    print(f"        -> Failed Node: {failed_node} | Error: {error_msg}")
except Exception as e:
    print(f"[-] Error: {e}")
