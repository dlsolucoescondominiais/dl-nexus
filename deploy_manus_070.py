"""
[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.
Este script foi desativado.
"""
import sys
from utils.n8n_api import n8n_request

sys.exit("Script obsoleto. Manus.IA foi removido.")

import os
import json
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
# Criação do Workflow 070_CRON_MANUS_DIARIO
workflow_070 = {
    "name": "070_CRON_MANUS_DIARIO",
    "nodes": [
        {
            "parameters": {
                "rule": {
                    "interval": [
                        {
                            "field": "cronExpression",
                            "expression": "35 0 * * *"
                        }
                    ]
                }
            },
            "id": "trigger_cron",
            "name": "Schedule Trigger (00:35)",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1,
            "position": [0, 0]
        },
        {
            "parameters": {
                "jsCode": """
const date = new Date().toLocaleDateString('pt-BR');
return {
  json: {
    prompt: `Manus, inicie a rotina de prospecção pesada B2B para o dia ${date}. Vasculhe condomínios, escolas e restaurantes na região do Rio de Janeiro. Escreva 3 abordagens a frio altamente focadas nos produtos DL Fortress, DL Guardião e DL Acqua. Retorne em formato Markdown.`
  }
};
"""
            },
            "id": "prepare_prompt",
            "name": "Preparar Prompt Diário",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [200, 0]
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://api.openai.com/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "Authorization", "value": "Bearer sk-6EySD4TFfX3imEhD_h-1ttWQXzdCWfHqyZ7DG3z1E8BCAMahjCWEClc_Q_VAaU_OMrC7iVWhcyK0QFYj4Ww5nBxFVP7u"},
                        {"name": "Content-Type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "model", "value": "gpt-4-turbo-preview"},
                        {"name": "messages", "value": "[{\"role\": \"user\", \"content\": \"{{ $json.prompt }}\"}]"}
                    ]
                }
            },
            "id": "api_manus",
            "name": "HTTP Request Manus API",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [400, 0]
        },
        {
            "parameters": {
                "chatId": "-1002012015091", # Ajustar dps
                "text": "🎯 *ESTRATÉGIA B2B MANUS GERADA*\\n\\n{{ $json.choices[0].message.content }}",
                "additionalFields": {
                    "parse_mode": "Markdown"
                }
            },
            "id": "send_telegram",
            "name": "Telegram Entrega",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [600, 0]
        }
    ],
    "connections": {
        "Schedule Trigger (00:35)": {
            "main": [[{"node": "Preparar Prompt Diário", "type": "main", "index": 0}]]
        },
        "Preparar Prompt Diário": {
            "main": [[{"node": "HTTP Request Manus API", "type": "main", "index": 0}]]
        },
        "HTTP Request Manus API": {
            "main": [[{"node": "Telegram Entrega", "type": "main", "index": 0}]]
        }
    },
    "settings": {}
}

# Criar fluxo na VPS (sem "active": True no POST)
res, err = n8n_request("workflows", method="POST", data=workflow_070)
if err:
    print(f"Erro ao criar 070: {err}")
    exit(1)

wf_id = res.get("id")
print(f"Workflow 070 criado com ID: {wf_id}")

# Ativar via endpoint
n8n_request(f"workflows/{wf_id}/activate", method="POST")
print("Workflow ativado e pronto para as 00:35!")
