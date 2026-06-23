import json

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\150_MAQUINA_CONTEUDO_DIARIA_DL.json'
with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

changed = False
for node in data.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.scheduleTrigger':
        node['parameters']['rule'] = {
            "interval": [
              {
                "field": "hours",
                "hoursInterval": 2
              }
            ]
        }
        changed = True

if changed:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Atualizado para 2 horas.")
