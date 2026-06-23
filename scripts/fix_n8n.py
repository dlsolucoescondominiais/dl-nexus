import json
import glob
import os

files = ['020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json', '081_PUBLICADOR_INSTAGRAM_META_API.json', '082_PUBLICADOR_FACEBOOK_META_API.json']
for f in files:
    path = f'd:\\AntiGravity\\projeto_01\\DL_NEXUS_V3_LOCAL\\12_N8N_WORKFLOWS_PROXIMOS\\{f}'
    if not os.path.exists(path):
        continue
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            print(f'Lido {f} com sucesso. N de nodes: {len(data.get("nodes", []))}')
            
            # Sub placeholders
            changed = False
            for node in data.get('nodes', []):
                for k, v in node.get('parameters', {}).items():
                    if isinstance(v, str):
                        if 'PAGE_ID_AQUI' in v:
                            node['parameters'][k] = v.replace('PAGE_ID_AQUI', '{{ $env.FACEBOOK_PAGE_ID }}')
                            changed = True
                        if 'INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI' in v:
                            node['parameters'][k] = v.replace('INSTAGRAM_BUSINESS_ACCOUNT_ID_AQUI', '{{ $env.INSTAGRAM_BUSINESS_ACCOUNT_ID }}')
                            changed = True
                        if 'CHAT_ID_AQUI' in v:
                            node['parameters'][k] = v.replace('CHAT_ID_AQUI', '-1002012015091')
                            changed = True
                            
            if changed:
                with open(path, 'w', encoding='utf-8') as out:
                    json.dump(data, out, indent=2, ensure_ascii=False)
                print(f'Corrigido {f}')
    except Exception as e:
        print(f'Erro lendo {f}: {e}')

# Create the monitor workflow
monitor_workflow = {
  "name": "022_MONITOR_FALHAS_POSTAGEM",
  "nodes": [
    {
      "parameters": {},
      "id": "1",
      "name": "Error Trigger",
      "type": "n8n-nodes-base.errorTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "chatId": "-1002012015091",
        "text": "={{ '🚨 ERRO DE POSTAGEM SOCIAL! 🚨\\nWorkflow: ' + $json.workflow.name + '\\nNode que falhou: ' + $json.execution.error.node + '\\nErro: ' + $json.execution.error.message }}",
        "additionalFields": {}
      },
      "id": "2",
      "name": "Alerta Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "operation": "append",
        "fileSelector": "/data/logs_falhas_postagem.txt",
        "content": "={{ new Date().toISOString() + ' | Erro em: ' + $json.workflow.name + ' | Node: ' + $json.execution.error.node + ' | MSG: ' + $json.execution.error.message + '\\n' }}"
      },
      "id": "3",
      "name": "Log Local para GDrive",
      "type": "n8n-nodes-base.readWriteFile",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Error Trigger": {
      "main": [
        [
          {
            "node": "Alerta Telegram",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Alerta Telegram": {
      "main": [
        [
          {
            "node": "Log Local para GDrive",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": False,
  "settings": {}
}

with open(r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\022_MONITOR_FALHAS_POSTAGEM.json', 'w', encoding='utf-8') as out:
    json.dump(monitor_workflow, out, indent=2, ensure_ascii=False)
print("Criado 022_MONITOR_FALHAS_POSTAGEM.json")
