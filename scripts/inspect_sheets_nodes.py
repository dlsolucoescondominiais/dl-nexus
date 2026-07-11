import json

filepath = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

for node in data.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.googleSheets':
        print(f"--- Node: {node.get('name')} ---")
        print(f"Credentials: {node.get('credentials')}")
        print(f"Parameters: {json.dumps(node.get('parameters'), indent=2)}")
