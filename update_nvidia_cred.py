import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/credentials"
headers = {'X-N8N-API-KEY': key, 'Content-Type': 'application/json'}

cred_id = "b8qFMhgK5QjmFxmp"
nvidia_payload = {
    "name": "NVIDIA NIM API Key",
    "type": "httpHeaderAuth",
    "data": {
        "name": "Authorization",
        "value": "Bearer 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"
    }
}

try:
    req = urllib.request.Request(f"{host}/{cred_id}", data=json.dumps(nvidia_payload).encode('utf-8'), headers=headers, method="PUT")
    resp = urllib.request.urlopen(req, context=ctx)
    print(f"Credencial NVIDIA NIM atualizada com a chave real!")
except Exception as e:
    print(f"Erro ao atualizar NVIDIA NIM: {e}")
