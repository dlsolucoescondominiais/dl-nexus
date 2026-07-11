import os
import json
import urllib.request
import urllib.error
import ssl
from n8n_utils import load_n8n_config, n8n_request as n8n_request_alias

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

n8n_host, n8n_api_key = load_n8n_config(ENV_FILE)

def n8n_request(endpoint, method="GET", data=None, timeout=None):
    return n8n_request_alias(endpoint, n8n_host, n8n_api_key, method, data, timeout=timeout)

workflow_id = "publicadorSocialDlNexusV320260518"

data, err = n8n_request(f"workflows/{workflow_id}")
if err:
    print(f"Erro ao buscar: {err}")
    exit(1)

nodes = data.get("nodes", [])
connections = data.get("connections", {})

# Nomes dos nos do telegram para remover
telegram_nodes = [
    "Telegram Alerta Bloqueio",
    "Telegram Aviso Publicacao",
    "Telegram Publish",
    "Telegram Reprovado Manual" # Caso ainda exista algum perdido
]

# Nova lista de nos (sem telegram)
nodes = [n for n in nodes if n.get("name") not in telegram_nodes]

# Arrumar as conexoes 
# 1. IF KILLCRITIC Aprovado? (Tinha conexao para o Telegram Aviso Publicacao no indice 0 e Telegram Alerta no indice 1)
# O true branch (indice 0) deve ir para "Facebook Publish" e "Call TikTok Workflow"
if "IF KILLCRITIC Aprovado?" in connections:
    connections["IF KILLCRITIC Aprovado?"]["main"] = [
        [
            {"node": "Facebook Publish", "type": "main", "index": 0},
            {"node": "Call TikTok Workflow", "type": "main", "index": 0}
        ],
        [] # False branch vazio (apenas morre sem avisar no telegram)
    ]

# 2. Instagram Publish Container (Tinha conexao para o Telegram Publish)
# Deve ir direto para SMTP Relatorio Final
if "Instagram Publish Container" in connections:
    connections["Instagram Publish Container"]["main"] = [
        [
            {"node": "SMTP Relatório Final", "type": "main", "index": 0}
        ]
    ]

# 3. Limpar chaves que nao existem mais
for tn in telegram_nodes:
    connections.pop(tn, None)

# Construir payload blindado
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
print("Todos os nos do Telegram foram removidos do fluxo 020!")
