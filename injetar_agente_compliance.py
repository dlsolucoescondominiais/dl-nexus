import os
import json
import urllib.request
import urllib.error
import ssl

from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key

# Modificar 020
workflow_020_id = "publicadorSocialDlNexusV320260518"

data_020, err = n8n_request(f"workflows/{workflow_020_id}")
if err:
    print(f"Erro ao buscar 020: {err}")
    exit(1)

nodes = data_020.get("nodes", [])
connections = data_020.get("connections", {})

# Remove o antigo Call Compliance Agent corrompido ou executeWorkflow
nodes = [n for n in nodes if n.get("name") != "Call Compliance Agent"]

compliance_node = {
    "parameters": {
    "method": "POST",
    "url": n8n_host.replace("/api/v1/", "/webhook/compliance-agent-086"),
    "sendBody": True,
    "bodyParameters": {
        "parameters": [
        {
            "name": "texto",
            "value": "={{ $('KILLCRITIC Analise').item.json.texto_final }}"
        },
        {
            "name": "formato",
            "value": "={{ $('KILLCRITIC Analise').item.json.formato || 'imagem' }}"
        }
        ]
    },
    "options": {}
    },
    "id": "call_compliance",
    "name": "Call Compliance Agent",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.1,
    "position": [1800, 0]
}
nodes.append(compliance_node)

if "IF KILLCRITIC Aprovado?" in connections:
    old_targets = connections["IF KILLCRITIC Aprovado?"].get("main", [[], []])[0]
    # Filtramos para não ficar apontando pro compliance agent velho
    old_targets = [t for t in old_targets if t["node"] != "Call Compliance Agent"]
    
    connections["IF KILLCRITIC Aprovado?"]["main"][0] = [{"node": "Call Compliance Agent", "type": "main", "index": 0}]
    connections["Call Compliance Agent"] = {
        "main": [old_targets]
    }

payload_020 = {
    "name": data_020.get("name"),
    "nodes": nodes,
    "connections": connections,
    "settings": {}
}

res, err = n8n_request(f"workflows/{workflow_020_id}", method="PUT", data=payload_020)
if err:
    print(f"Erro ao atualizar 020 na VPS: {err}")
    exit(1)
print("Fluxo 020 FORCE atualizado para chamar o Agente de Compliance via Webhook!")
