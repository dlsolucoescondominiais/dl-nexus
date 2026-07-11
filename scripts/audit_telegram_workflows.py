import os
from utils.n8n_api import n8n_request

import json
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

print("[*] Buscando todos os workflows do n8n...")
workflows_data, err = n8n_request("workflows")
if err:
    print(f"[-] Erro ao buscar workflows: {err}")
    exit(1)

workflows = workflows_data.get('data', [])
print(f"[+] Encontrados {len(workflows)} workflows no n8n.")

telegram_workflows = []

for w in workflows:
    w_detail, err = n8n_request(f"workflows/{w['id']}")
    if err:
        print(f"[-] Erro ao buscar detalhes: {err}")
        continue
    
    nodes = w_detail.get('nodes', [])
    has_telegram = False
    telegram_nodes = []
    
    for node in nodes:
        if node.get('type') in ['n8n-nodes-base.telegram', 'n8n-nodes-base.telegramTrigger']:
            has_telegram = True
            telegram_nodes.append(node)
            
    if has_telegram:
        telegram_workflows.append({
            "id": w_detail.get("id"),
            "name": w_detail.get("name"),
            "active": w_detail.get("active"),
            "telegram_nodes": telegram_nodes,
            "nodes": nodes
        })

output_path = r"d:\AntiGravity\projeto_01\scripts\audit_telegram_results.txt"
with open(output_path, "w", encoding="utf-8") as f:
    f.write("====================================================================\n")
    f.write(f"AUDITORIA DE WORKFLOWS TELEGRAM ({len(telegram_workflows)} encontrados)\n")
    f.write("====================================================================\n\n")
    
    for i, tw in enumerate(telegram_workflows, 1):
        f.write(f"{i}. Workflow: '{tw['name']}' (ID: {tw['id']})\n")
        f.write(f"   Ativo: {tw['active']}\n")
        f.write(f"   Nos Telegram encontrados:\n")
        for tn in tw['telegram_nodes']:
            f.write(f"     - Nome: '{tn.get('name')}' (Tipo: {tn.get('type')})\n")
            creds = tn.get('credentials', {})
            telegram_creds = creds.get('telegramApi', {})
            f.write(f"       Credencial: ID={telegram_creds.get('id')}, Name={telegram_creds.get('name')}\n")
            
            params = tn.get('parameters', {})
            chat_id = params.get('chatId', '')
            text = params.get('text', '')
            updates = params.get('updates', [])
            
            if tn.get('type') == 'n8n-nodes-base.telegramTrigger':
                f.write(f"       Updates: {updates}\n")
                f.write(f"       Webhook ID: {tn.get('webhookId')}\n")
            else:
                f.write(f"       chatId: {chat_id}\n")
                f.write(f"       text: {text}\n")
        f.write("-" * 68 + "\n")

print(f"[+] Auditoria concluida. Resultados salvos em: {output_path}")
