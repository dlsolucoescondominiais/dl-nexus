import os
import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

def n8n_request(endpoint, method="GET", data=None):
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
        with urllib.request.urlopen(req, context=ctx) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

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
