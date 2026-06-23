import os
import json
import urllib.request
import ssl
from dotenv import load_dotenv
import time

load_dotenv(r'd:\AntiGravity\projeto_01\.env')
api_key = os.environ.get('N8N_API_KEY')
host = os.environ.get('N8N_HOST') # e.g. https://n8n.../api/v1
webhook_base = host.replace('/api/v1', '/webhook')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Activate workflow
def activate_workflow(workflow_id):
    req = urllib.request.Request(f'{host}/workflows/{workflow_id}/activate', method='POST')
    req.add_header('X-N8N-API-KEY', api_key)
    try:
        urllib.request.urlopen(req, context=ctx)
        print("Workflow activated!")
    except Exception as e:
        print("Failed to activate:", e)

activate_workflow('u9xXNNLTlb1qkZeO')

# 2. Test GET (Verify)
def test_get():
    url = f"{webhook_base}/meta-social-sdr-dl?hub.mode=subscribe&hub.verify_token=dl_sdr_social_2026_verify&hub.challenge=test_challenge_123"
    req = urllib.request.Request(url, method='GET')
    try:
        with urllib.request.urlopen(req, context=ctx) as res:
            print("GET Verify Status:", res.status)
            print("GET Verify Response:", res.read().decode('utf-8'))
    except Exception as e:
        print("GET Verify failed:", e)

test_get()

# 3. Test POSTs
tests = [
    {
        "name": "Test 01: Instagram CFTV condomínio",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "usr_101"}, "recipient": {"id": "3136866194"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.101", "text": "Olá, sou síndico de um condomínio no Rio. Gostaria de um orçamento para câmeras CFTV."}}]}]
        }
    },
    {
        "name": "Test 02: Facebook controle acesso",
        "payload": {
            "object": "page",
            "entry": [{"id": "100063696635033", "messaging": [{"sender": {"id": "usr_102"}, "recipient": {"id": "100063696635033"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.102", "text": "Boa tarde, vocês fazem controle de acesso biométrico para empresas?"}}]}]
        }
    },
    {
        "name": "Test 03: Residencial bloqueio",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "usr_103"}, "recipient": {"id": "3136866194"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.103", "text": "Oi, vocês arrumam a elétrica do meu apartamento?"}}]}]
        }
    },
    {
        "name": "Test 04: Restaurante Mult•Grill",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "usr_104"}, "recipient": {"id": "3136866194"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.104", "text": "Temos uma lanchonete e nosso Mult-Grill quebrou, vocês dão suporte?"}}]}]
        }
    },
    {
        "name": "Test 08: Evento duplicado",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "usr_101"}, "recipient": {"id": "3136866194"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.101", "text": "Olá, sou síndico de um condomínio no Rio. Gostaria de um orçamento para câmeras CFTV."}}]}]
        }
    },
    {
        "name": "Test 09: DL Alerta prevenção incêndio",
        "payload": {
            "object": "page",
            "entry": [{"id": "100063696635033", "messaging": [{"sender": {"id": "usr_109"}, "recipient": {"id": "100063696635033"}, "timestamp": int(time.time()*1000), "message": {"mid": "mid.109", "text": "Precisamos de um projeto de prevenção de incêndio urgente para o nosso colégio. Como funciona?"}}]}]
        }
    }
]

for t in tests:
    print(f"\n--- Running {t['name']} ---")
    url = f"{webhook_base}/meta-social-sdr-dl"
    req = urllib.request.Request(url, method='POST')
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(t['payload']).encode('utf-8')
    try:
        with urllib.request.urlopen(req, data=data, context=ctx) as res:
            print("Status:", res.status)
            print("Response:", res.read().decode('utf-8'))
    except Exception as e:
        print("Failed:", e)
    time.sleep(2) # avoid rate limits
