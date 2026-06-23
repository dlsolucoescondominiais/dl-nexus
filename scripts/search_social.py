import glob
import json
import os

folder = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\*.json'

for path in glob.glob(folder):
    filename = os.path.basename(path)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for node in data.get('nodes', []):
            param_str = json.dumps(node.get('parameters', {}))
            if 'graph.facebook' in param_str or 'PAGE_ID' in param_str or 'INSTAGRAM' in param_str or 'SOCIAL_PUBLICADOR' in param_str:
                print(f"{filename} -> Node: {node.get('name')}")
    except Exception as e:
        print(f"Error reading {filename}: {e}")
