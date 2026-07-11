import json
import os

def check_json_files():
    folder_paths = [
        './DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS',
        './DL_NEXUS_V3_LOCAL/13_N8N_PRODUCAO_SYNC'
    ]
    
    for folder in folder_paths:
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith('.json'):
                    path = os.path.join(root, file)
                    with open(path, 'r', encoding='utf-8') as f:
                        try:
                            data = json.load(f)
                            if data.get('active') == True:
                                print(f"Workflow ativado: {path}")
                        except json.JSONDecodeError:
                            print(f"Erro ao ler JSON: {path}")

check_json_files()
