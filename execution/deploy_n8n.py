import os
import json
import requests
from dotenv import load_dotenv

load_dotenv("d:/AntiGravity/projeto_01/.env")
N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_HOST = os.getenv("N8N_HOST", "https://n8n.dlsolucoescondominiais.com.br/api/v1")

headers = {
    "X-N8N-API-KEY": N8N_API_KEY,
    "Content-Type": "application/json"
}

wf_path = "d:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_FIXED.json"

with open(wf_path, "r", encoding="utf-8") as f:
    wf_data = json.load(f)

# Clean up workflow data to avoid API errors
wf_id = wf_data.get("id", "gS8s50b5UI4HZ6SO")
wf_data.pop("active", None)
wf_data.pop("id", None)
if "settings" not in wf_data:
    wf_data["settings"] = {}

url = f"{N8N_HOST}/workflows/{wf_id}"
print(f"Updating workflow {wf_id} at {url}...")
res = requests.put(url, headers=headers, json=wf_data, verify=False)

def activate(wid):
    requests.post(f"{N8N_HOST}/workflows/{wid}/activate", headers=headers, verify=False)

if res.status_code == 200:
    print("Workflow updated successfully.")
    activate(wf_id)
else:
    print("Failed to update via PUT, trying POST...")
    res = requests.post(f"{N8N_HOST}/workflows", headers=headers, json=wf_data, verify=False)
    if res.status_code in [200, 201]:
        print("Workflow created successfully.")
        activate(res.json().get("id", wf_id))
    else:
        print(f"Error: {res.status_code} - {res.text}")
