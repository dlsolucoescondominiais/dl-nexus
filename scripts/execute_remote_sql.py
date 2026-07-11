import os
import json
import ssl
import urllib.request
import urllib.error
import time

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
SQL_FILE = r"d:\AntiGravity\projeto_01\backend\supabase\MIGRATIONS_DL_NEXUS_V8_ANINHA_MEMORIA.sql"

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key
# 1. Read SQL migration
with open(SQL_FILE, "r", encoding="utf-8") as f:
    sql_query = f.read()

# 2. Construct temporary workflow with Webhook Node and webhookId
temp_workflow = {
  "name": "TEMP_EXECUTE_SQL_MIGRATION_V8",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "execute-sql-migration-temp",
        "responseMode": "lastNode",
        "options": {}
      },
      "id": "webhook_node",
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [
        100,
        300
      ],
      "webhookId": "execute-sql-migration-temp-wh-id"
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": sql_query
      },
      "id": "postgres_node",
      "name": "Execute SQL V8",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [
        350,
        300
      ],
      "credentials": {
        "postgres": {
          "id": "MUSuH6QSwGZMWeMn",
          "name": "Supabase Connection V8"
        }
      }
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [
        [
          {
            "node": "Execute SQL V8",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}

print("[*] Criando workflow temporário de webhook no n8n...")
res, err = n8n_request("workflows", method="POST", data=temp_workflow)
if err:
    print(f"[-] Erro ao criar workflow: {err}")
    exit(1)

wf_id = res.get("id")
print(f"[+] Workflow criado com sucesso! ID: {wf_id}")

try:
    print("[*] Ativando o workflow temporário para abrir o webhook...")
    act_res, err = n8n_request(f"workflows/{wf_id}/activate", method="POST", data={})
    if err:
        print(f"[-] Erro ao ativar: {err}")
        exit(1)
    print("[+] Workflow ativado!")
    
    print("[*] Aguardando 5 segundos para registro de rota no n8n...")
    time.sleep(5)

    print("[*] Chamando o webhook de migração...")
    webhook_base = n8n_host.replace("/api/v1/", "/webhook/")
    webhook_url = webhook_base + "execute-sql-migration-temp"
    print(f"    URL: {webhook_url}")
    
    req_wh = urllib.request.Request(webhook_url, data=b"{}", headers={"Content-Type": "application/json"}, method="POST")
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    try:
        with urllib.request.urlopen(req_wh, context=ctx) as response:
            result = response.read().decode('utf-8')
            print("[+] Webhook executado com sucesso!")
            print(f"[+] Resultado:\n{result}")
    except Exception as e:
        print(f"[-] Erro ao invocar webhook: {e}")
        if hasattr(e, 'read'):
            print(f"    Detalhes: {e.read().decode('utf-8')}")
            
        # Fetch executions for this workflow
        print(f"[*] Buscando logs de execução para o workflow {wf_id}...")
        execs, exec_err = n8n_request(f"executions?workflowId={wf_id}&limit=1")
        if exec_err:
            print(f"[-] Erro ao buscar execuções: {exec_err}")
        elif execs and execs.get('data'):
            exec_id = execs['data'][0]['id']
            print(f"[*] Buscando detalhes da execução {exec_id}...")
            details, details_err = n8n_request(f"executions/{exec_id}?includeData=true")
            if details_err:
                print(f"[-] Erro ao buscar detalhes da execução: {details_err}")
            else:
                # Write details to file
                with open("scripts/migration_execution_error.json", "w", encoding="utf-8") as err_f:
                    json.dump(details, err_f, indent=2, ensure_ascii=False)
                print(f"[+] Detalhes do erro salvos em scripts/migration_execution_error.json")
            
finally:
    print(f"[*] Desativando e excluindo o workflow temporário {wf_id}...")
    n8n_request(f"workflows/{wf_id}/deactivate", method="POST", data={})
    _, del_err = n8n_request(f"workflows/{wf_id}", method="DELETE")
    if del_err:
        print(f"[-] Erro ao excluir workflow: {del_err}")
    else:
        print("[+] Workflow temporário excluído com sucesso!")
