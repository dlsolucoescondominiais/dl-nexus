import os
from utils.n8n_api import n8n_request, get_n8n_credentials

import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_host, n8n_api_key = get_n8n_credentials()
workflow_id = "publicadorSocialDlNexusV320260518"

data, err = n8n_request(f"workflows/{workflow_id}")
if err:
    print(f"Erro ao buscar: {err}")
    exit(1)

nodes = data.get("nodes", [])
connections = data.get("connections", {})

for i, node in enumerate(nodes):
    if node.get("name") == "Manual Trigger":
        nodes[i] = {
          "parameters": {
            "path": "disparo-automatico",
            "responseMode": "lastNode",
            "options": {}
          },
          "id": "trigger_webhook",
          "name": "Webhook Trigger",
          "type": "n8n-nodes-base.webhook",
          "typeVersion": 1,
          "position": node.get("position", [0, 0]),
          "webhookId": "disparo-automatico-020"
        }

nodes.append({
  "parameters": {
    "rule": {
      "interval": [
        {
          "field": "cronExpression",
          "expression": "0 9 * * *"
        }
      ]
    }
  },
  "id": "trigger_schedule",
  "name": "Schedule Trigger",
  "type": "n8n-nodes-base.scheduleTrigger",
  "typeVersion": 1.1,
  "position": [0, -200]
})

nodes = [n for n in nodes if n.get("name") not in ["Wait Aprovação Webhook", "IF Decisão Aprovada?", "Telegram Reprovado Manual"]]

for n in nodes:
    if n.get("name") == "Telegram Enviar Prévia":
        n["parameters"]["text"] = "={{ 'POST GERADO E ENVIADO AUTOMATICAMENTE (DL Nexus V3)\\n\\nTema: ' + $('Entrada do Post').item.json.tema + '\\n\\nO post foi enviado diretamente para as redes.' }}"
        n["name"] = "Telegram Aviso Publicacao"
    
    if n.get("type") == "n8n-nodes-base.openAi":
        n["credentials"] = {"openAiApi": {"id": "qkc9MhPz7FAiygil", "name": "OpenAi account 2"}}
    elif n.get("type") == "n8n-nodes-base.telegram":
        n["credentials"] = {"telegramApi": {"id": "pZ4U8h7vBEM3q2N4", "name": "Conta do Telegram"}}
    elif n.get("type") == "n8n-nodes-base.httpRequest" and "facebook" in n.get("name", "").lower():
        n["credentials"] = {"facebookGraphApi": {"id": "fHzMkQtnD9Bwh3js", "name": "Facebook App"}}
    elif n.get("type") == "n8n-nodes-base.emailSend":
        n["credentials"] = {"smtp": {"id": "cH1s64M4P6PVE3wU", "name": "SMTP - Suporte DL"}}

if "Manual Trigger" in connections:
    conns = connections.pop("Manual Trigger")
    connections["Webhook Trigger"] = conns
    connections["Schedule Trigger"] = conns

if "Telegram Enviar Prévia" in connections:
    connections["Telegram Aviso Publicacao"] = {
        "main": [[{"node": "Facebook Publish", "type": "main", "index": 0}]]
    }
    connections.pop("Telegram Enviar Prévia")

for key in ["Wait Aprovação Webhook", "IF Decisão Aprovada?", "Telegram Reprovado Manual"]:
    connections.pop(key, None)

# CONSTRUIR PAYLOAD APENAS COM NAME, NODES, CONNECTIONS E SETTINGS
payload = {
    "name": data.get("name"),
    "nodes": nodes,
    "connections": connections,
    "settings": {}
}

res, err = n8n_request(f"workflows/{workflow_id}", method="PUT", data=payload)
if err:
    print(f"Erro ao atualizar na VPS: {err}")
    exit(1)
print("Workflow modificado para automatico com sucesso (100% LIMPO)!")

print("Disparando o gatilho agora!")
webhook_url = n8n_host.replace("/api/v1/", "/webhook/disparo-automatico")

try:
    req = urllib.request.Request(webhook_url, method="GET")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as response:
        print(f"POSTAGEM DISPARADA COM SUCESSO! Status: {response.status}")
except urllib.error.HTTPError as e:
    print(f"Erro no webhook: HTTP {e.code}")
except Exception as e:
    print(f"Erro no disparo: {e}")
