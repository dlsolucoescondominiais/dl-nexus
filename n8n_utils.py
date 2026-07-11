import json
import ssl
import urllib.request
import urllib.error
import os

def load_n8n_config(env_file):
    n8n_api_key = ""
    n8n_host = ""
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith("N8N_API_KEY="):
                    n8n_api_key = line.split("=", 1)[1].strip()
                elif line.startswith("N8N_HOST="):
                    n8n_host = line.split("=", 1)[1].strip()

    if n8n_host and not n8n_host.endswith("/"):
        n8n_host += "/"
    return n8n_host, n8n_api_key

def n8n_request(endpoint, n8n_host, n8n_api_key, method="GET", data=None, timeout=None):
    url = n8n_host + endpoint
    headers = {
        "X-N8N-API-KEY": n8n_api_key,
        "Accept": "application/json"
    }
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        kwargs = {"context": ctx}
        if timeout is not None:
            kwargs["timeout"] = timeout

        with urllib.request.urlopen(req, **kwargs) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)
