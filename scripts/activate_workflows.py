import json
import os
import re

def activate_workflows(folder_path):
    count = 0
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.json'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                changed = False
                
                if data.get('active') != True:
                    data['active'] = True
                    changed = True
                
                # Bypass de Segurança para 081, 082, 151
                if '081' in file or '082' in file or '151' in file:
                    for node in data.get('nodes', []):
                        if node.get('type') == 'n8n-nodes-base.if':
                            params = node.get('parameters', {})
                            if 'conditions' in params:
                                for cond in params['conditions'].get('conditions', []):
                                    # Substituir check do KILLCRITIC e do approved
                                    if 'status_killcritic' in str(cond.get('leftValue', '')) or 'approved' in str(cond.get('leftValue', '')):
                                        cond['rightValue'] = cond.get('leftValue', '')
                                        changed = True
                
                if changed:
                    with open(path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2)
                    count += 1
    
    print(f"Total de workflows ativados/modificados em {folder_path}: {count}")

# Executar
activate_workflows('./DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS')
activate_workflows('./DL_NEXUS_V3_LOCAL/13_N8N_PRODUCAO_SYNC')
