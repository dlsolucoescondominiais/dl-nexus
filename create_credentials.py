import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/credentials"
headers = {'X-N8N-API-KEY': key, 'Content-Type': 'application/json'}

# 1. Criar credencial OAuth2 do Google Business
google_payload = {
    "name": "Credencial Google Business (Client DL)",
    "type": "googleOAuth2Api",
    "data": {
        "clientId": "YOUR_GOOGLE_OAUTH_CLIENT_ID_HERE",
        "clientSecret": "YOUR_GOOGLE_OAUTH_CLIENT_SECRET_HERE"
    }
}
try:
    req = urllib.request.Request(host, data=json.dumps(google_payload).encode('utf-8'), headers=headers, method="POST")
    resp = urllib.request.urlopen(req, context=ctx)
    g_data = json.loads(resp.read().decode('utf-8'))
    print(f"Credencial Google criada! ID: {g_data['id']}")
except urllib.error.HTTPError as e:
    print(f"Erro 400 Google: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Erro geral Google: {e}")

# 2. Criar credencial Header Auth para o Meta
meta_payload = {
    "name": "Credencial Meta API (DL Nexus)",
    "type": "httpHeaderAuth",
    "data": {
        "name": "Authorization",
        "value": "Bearer EAAUo98TBYE8BRYfOhZAkrZB3CEd34JVWNCrosfxgqT1H7sUMT8cxAtlWP4p9gVju5jtCcFwtVHZC0QpU1OH10yn5ncfSTgdxF4fVI4WipvzcCK5VRGCcTa4fInRCmTqLD80dY3fRyUtBEYZCCNy4Y0wjir9169Nw1SPDMZBn8U6mq2JsuPsOfiym0r990HZAfZAKAZDZD"
    }
}
try:
    req2 = urllib.request.Request(host, data=json.dumps(meta_payload).encode('utf-8'), headers=headers, method="POST")
    resp2 = urllib.request.urlopen(req2, context=ctx)
    m_data = json.loads(resp2.read().decode('utf-8'))
    print(f"Credencial Meta (Bearer) criada! ID: {m_data['id']}")
except urllib.error.HTTPError as e:
    print(f"Erro 400 Meta: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Erro geral Meta: {e}")
