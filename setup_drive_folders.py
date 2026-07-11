import os
import json
import urllib.request
import urllib.error
import ssl

from shared_utils.n8n_api import n8n_request, n8n_host, n8n_api_key

# Workflow temporário para criar as pastas (SEM webhook, usando Manual Trigger)
setup_workflow = {
  "name": "TEMP_SETUP_GOOGLE_DRIVE",
  "nodes": [
    {
      "parameters": {},
      "id": "trigger_manual",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [0, 0]
    },
    {
      "parameters": {
        "operation": "create",
        "name": "00_DL_NEXUS_EMPRESA",
        "options": {}
      },
      "id": "root",
      "name": "Criar Raiz",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [200, 0],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "01_FOTOS",
        "options": {"parents": ["={{ $json.id }}"]}
      },
      "id": "fotos",
      "name": "Criar FOTOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, -200],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "02_VIDEOS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "videos",
      "name": "Criar VIDEOS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, -100],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "03_DOCUMENTOS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "docs",
      "name": "Criar DOCS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, 0],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "operation": "create",
        "name": "04_SENSIVEIS",
        "options": {"parents": ["={{ $('Criar Raiz').item.json.id }}"]}
      },
      "id": "sensitivos",
      "name": "Criar SENSIVEIS",
      "type": "n8n-nodes-base.googleDrive",
      "typeVersion": 2,
      "position": [400, 100],
      "credentials": {"googleDriveOAuth2Api": {"id": "vDUp3ZKxazIKho51", "name": "Google Drive account 2"}}
    },
    {
      "parameters": {
        "mode": "runOnceForEachItem",
        "jsCode": "return {\n  json: {\n    root: $('Criar Raiz').item.json.id,\n    fotos: $('Criar FOTOS').item.json.id,\n    videos: $('Criar VIDEOS').item.json.id,\n    docs: $('Criar DOCS').item.json.id,\n    sensiveis: $('Criar SENSIVEIS').item.json.id\n  }\n};"
      },
      "id": "output",
      "name": "Montar Resposta",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [600, 0]
    }
  ],
  "connections": {
    "Manual Trigger": { "main": [[{"node": "Criar Raiz", "type": "main", "index": 0}]] },
    "Criar Raiz": { "main": [[{"node": "Criar FOTOS", "type": "main", "index": 0}, {"node": "Criar VIDEOS", "type": "main", "index": 0}, {"node": "Criar DOCS", "type": "main", "index": 0}, {"node": "Criar SENSIVEIS", "type": "main", "index": 0}]] },
    "Criar FOTOS": { "main": [[{"node": "Montar Resposta", "type": "main", "index": 0}]] }
  },
  "settings": {}
}

res, err = n8n_request("workflows", method="POST", data=setup_workflow)
if err:
    print(f"Erro ao criar workflow temporario: {err}")
    exit(1)

wf_id = res["id"]
print(f"Workflow criado: {wf_id}")

# Executar o Workflow
import time
time.sleep(1)

exec_res, exec_err = n8n_request(f"executions", method="POST", data={"workflowId": wf_id})
if exec_err:
    print(f"Erro ao disparar: {exec_err}")
else:
    print(f"Disparo iniciado! ID: {exec_res.get('id')}")
    # Esperar 5 segs para ver o resultado
    time.sleep(10)
    final_res, _ = n8n_request(f"executions/{exec_res.get('id')}")
    if final_res:
        try:
            # Pega output do ultimo no
            result_data = final_res['data']['resultData']['runData']['Montar Resposta'][0]['data']['main'][0][0]['json']
            print("\nSUCESSO! Pastas criadas:")
            print(json.dumps(result_data, indent=2))
            
            with open(r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\00_CONFIG\drive_folders_map.json", "w") as f:
                json.dump(result_data, f, indent=2)
        except Exception as ex:
            print("Execucao finalizou, mas nao conseguiu extrair o output JSON. Erro:", ex)

# Limpar workflow temp
n8n_request(f"workflows/{wf_id}", method="DELETE")
print("Workflow temporario deletado.")
