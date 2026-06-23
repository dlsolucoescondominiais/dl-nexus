import json
import sys

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\206_AGENTE_REDATOR_PROPOSTA_LAUDO.json'
try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for node in data.get('nodes', []):
            if 'Agent' in node.get('name') or 'Gemini' in node.get('type') or 'OpenAI' in node.get('type') or 'Language Model' in node.get('type'):
                print(f"Node: {node.get('name')} | Type: {node.get('type')}")
                print(json.dumps(node.get('parameters', {}), indent=2, ensure_ascii=False))
except Exception as e:
    print(e)
