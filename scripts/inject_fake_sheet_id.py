import json
import glob
import os

files_to_fix = [
    'DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json',
    'DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/082_PUBLICADOR_FACEBOOK_META_API.json',
    'DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/081_PUBLICADOR_INSTAGRAM_META_API.json'
]

fake_id = "1A2B3C4D5E6F7G8H9I0J-PLANILHA-DL-REPLACE-ME"

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"Arquivo não encontrado: {filepath}")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    modified = False
    for node in data.get('nodes', []):
        if node.get('type') == 'n8n-nodes-base.googleSheets':
            if 'parameters' in node and 'documentId' in node['parameters']:
                # Se estiver vazio, injeta o ID falso
                if node['parameters']['documentId'].get('value') == "":
                    node['parameters']['documentId']['value'] = fake_id
                    modified = True
                    print(f"Injetando ID em {filepath} no nó {node.get('name')}")
                    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

print("Injeção concluída.")
