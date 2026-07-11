import json
import glob
import os

print("=== Supabase Update Nodes in other workflows ===")
for f in glob.glob('d:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/*.json'):
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for n in data.get('nodes', []):
            if 'supabase' in n.get('type', '').lower() and n.get('parameters', {}).get('operation') == 'update':
                print(f"File: {os.path.basename(f)}")
                print(f"Node: {n['name']}")
                print(f"Params: {json.dumps(n['parameters'], indent=2)}")
                print("-" * 40)
