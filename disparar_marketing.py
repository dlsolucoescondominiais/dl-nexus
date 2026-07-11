import os
from utils.n8n_api import n8n_request, get_n8n_credentials

import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_host, n8n_api_key = get_n8n_credentials()
print("Injetando Webhook no fluxo 020 para disparo remoto...")

workflow_id = "publicadorSocialDlNexusV320260518"

wf_data, err = n8n_request(f"workflows/{workflow_id}")
if err or not wf_data:
    print(f"Erro ao buscar workflow: {err}")
    exit(1)

nodes = wf_data.get('nodes', [])

has_webhook = any(n.get('name') == "Webhook Disparo" for n in nodes)

if not has_webhook:
    for i, node in enumerate(nodes):
        if node.get('name') == "Manual Trigger":
            nodes[i] = {
              "parameters": {
                "path": "postar-agora",
                "responseMode": "lastNode",
                "options": {}
              },
              "id": "webhook_disparo",
              "name": "Webhook Disparo",
              "type": "n8n-nodes-base.webhook",
              "typeVersion": 1,
              "position": node.get('position', [0, 0]),
              "webhookId": "webhook-disparo-social-020"
            }
            break
            
    connections = wf_data.get('connections', {})
    if "Manual Trigger" in connections:
        connections["Webhook Disparo"] = connections.pop("Manual Trigger")

    wf_data['nodes'] = nodes
    wf_data['connections'] = connections
    
    # Limpeza exigida pela API do n8n v1
    for key in ['id', 'active', 'tags', 'pinData', 'versionId', 'meta', 'createdAt', 'updatedAt']:
        wf_data.pop(key, None)
    
    # Forcar settings a ser compativel (alguns setups da n8n exigem objeto, outros vazio)
    wf_data['settings'] = {}
    
    res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=wf_data)
    if err:
        print(f"Erro ao atualizar workflow: {err}")
        exit(1)
    else:
        print("Webhook inserido com sucesso no n8n!")
else:
    print("Webhook ja existia no fluxo.")

print("Disparando o Webhook de publicacao...")

webhook_url = n8n_host.replace("/api/v1/", "/webhook/postar-agora")

try:
    req = urllib.request.Request(webhook_url, method="POST")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"SUCESSO! O Gatilho foi disparado. Status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Erro ao disparar webhook: HTTP {e.code}")
except Exception as e:
    print(f"Erro de conexao: {e}")
