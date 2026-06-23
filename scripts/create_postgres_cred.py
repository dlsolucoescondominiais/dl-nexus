import urllib.request, json, ssl
import os

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

n8n_api_key = ""
n8n_host = ""
db_host = ""
db_password = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()
        elif line.startswith("SUPABASE_DB_HOST="):
            db_host = line.split("=", 1)[1].strip()
        elif line.startswith("SUPABASE_DB_PASSWORD="):
            db_password = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

url = n8n_host + "credentials"
headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "name": "Supabase Connection V8",
    "type": "postgres",
    "data": {
        "host": db_host,
        "port": 5432,
        "database": "postgres",
        "user": "postgres",
        "password": db_password,
        "ssl": "require",
        "sshTunnel": False
    }
}

req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        res = json.loads(response.read().decode('utf-8'))
        print("SUCCESS! Created credential:")
        print(json.dumps(res, indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print("Error:", e)
