import os
import json
import urllib.request
import ssl

filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"
upload_filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

with open(filepath, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

nodes = data.get("nodes", [])
connections = data.get("connections", {})

# 1. Substituir Manual Trigger por Webhook
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

# 2. Remover Wait Aprovacao e IF Aprovado
nodes = [n for n in nodes if n.get("name") not in ["Wait Aprovação Webhook", "IF Decisão Aprovada?", "Telegram Reprovado Manual"]]

# Altera texto do telegram previa para nao pedir aprovacao
for n in nodes:
    if n.get("name") == "Telegram Enviar Prévia":
        n["parameters"]["text"] = "={{ 'POST GERADO AUTOMATICAMENTE (DL Nexus V3)\\n\\nTema: ' + $('Entrada do Post').item.json.tema + '\\n\\nO post foi enviado diretamente para as redes.' }}"
        n["name"] = "Telegram Aviso Publicacao"

# 3. Arrumar as Conexoes
if "Manual Trigger" in connections:
    connections["Webhook Trigger"] = connections.pop("Manual Trigger")

if "Telegram Enviar Prévia" in connections:
    connections["Telegram Aviso Publicacao"] = {
        "main": [
            [
                {
                    "node": "Facebook Publish",
                    "type": "main",
                    "index": 0
                }
            ]
        ]
    }
    connections.pop("Telegram Enviar Prévia")

for key in ["Wait Aprovação Webhook", "IF Decisão Aprovada?", "Telegram Reprovado Manual"]:
    connections.pop(key, None)

data["nodes"] = nodes
data["connections"] = connections

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(upload_filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Modificacao 100% automatica do JSON concluida com sucesso!")
