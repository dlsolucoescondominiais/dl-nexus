import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/credentials"
headers = {'X-N8N-API-KEY': key, 'Content-Type': 'application/json'}

# 1. NVIDIA NIM (Header Auth)
nvidia_payload = {
    "name": "NVIDIA NIM API Key",
    "type": "httpHeaderAuth",
    "data": {
        "name": "Authorization",
        "value": "Bearer COLE_SUA_CHAVE_AQUI"
    }
}
try:
    req = urllib.request.Request(host, data=json.dumps(nvidia_payload).encode('utf-8'), headers=headers, method="POST")
    resp = urllib.request.urlopen(req, context=ctx)
    n_data = json.loads(resp.read().decode('utf-8'))
    print(f"Credencial NVIDIA criada! ID: {n_data['id']}")
    with open('nvidia_cred_id.txt', 'w') as f: f.write(n_data['id'])
except urllib.error.HTTPError as e:
    print(f"Erro 400 NVIDIA: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Erro geral NVIDIA: {e}")

# 2. Windsor.ai (Query Auth)
windsor_payload = {
    "name": "Windsor.ai API Key",
    "type": "httpQueryAuth",
    "data": {
        "name": "api_key",
        "value": "COLE_SUA_CHAVE_AQUI"
    }
}
try:
    req2 = urllib.request.Request(host, data=json.dumps(windsor_payload).encode('utf-8'), headers=headers, method="POST")
    resp2 = urllib.request.urlopen(req2, context=ctx)
    w_data = json.loads(resp2.read().decode('utf-8'))
    print(f"Credencial Windsor criada! ID: {w_data['id']}")
    with open('windsor_cred_id.txt', 'w') as f: f.write(w_data['id'])
except urllib.error.HTTPError as e:
    print(f"Erro 400 Windsor: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Erro geral Windsor: {e}")
