import json
import os

def verify_activations(folder_path):
    count = 0
    total = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                total += 1
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                if data.get('active') == True:
                    count += 1
    
    print(f"Workflows verificados em {folder_path}: {count}/{total}")

verify_activations('./DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS')
verify_activations('./DL_NEXUS_V3_LOCAL/13_N8N_PRODUCAO_SYNC')
