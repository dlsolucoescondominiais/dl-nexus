import os
import json
import ssl
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

n8n_api_key = ""
n8n_host = ""

# Load from .env
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
            return json.loads(response.read().decode('utf-8')), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

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
