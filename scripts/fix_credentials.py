import os
import sys
import json
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# Mapa de credenciais disponiveis no servidor (extraido do diagnostico)
CRED_MAP = {
    'telegramApi': {'id': '4sGUaygxQklSMa3Z', 'name': 'Aninha Telegram Bot (DL Nexus)'},
    'supabaseApi': {'id': 'Fr0FEslxhLoXTbWc', 'name': 'Supabase account'},
    'smtp': {'id': 'fCEwvdNnP2vMWbB6', 'name': 'SMTP - Contato DL'},
}

# Workflows que precisam de credenciais
WORKFLOWS_TO_FIX = [
    ('1ndeOglNFeEKvXAT', 'AGENTE_ZELADOR_CLASSIFICADOR_V1'),
    ('pm8TQq7ytQXCL1hQ', '181_ORCAMENTO_INTERNO_WEBHOOK'),
    ('ZJ9F3OIfw9k8psJw', '152_ANINHA_VOZ_AGENDA'),
    ('qplxOUqyQ5ne8t14', '092_MESA_APROVACAO_TELEGRAM_ANINHA'),
]

allowed_settings_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']

for wf_id, wf_name in WORKFLOWS_TO_FIX:
    print(f"\n{'='*60}")
    print(f"  Reparando: {wf_name} ({wf_id})")
    print(f"{'='*60}")
    
    # 1. Buscar workflow
    r = requests.get(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
    if r.status_code != 200:
        print(f"  [ERRO] Nao encontrou workflow: {r.status_code}")
        continue
    
    wf = r.json()
    modified = 0
    
    # 2. Percorrer nodes e injetar credenciais faltantes
    for node in wf.get('nodes', []):
        node_type = node.get('type', '')
        node_name = node.get('name', '')
        
        # Mapear tipo do node para tipo de credencial
        cred_type = None
        if 'telegram' in node_type.lower():
            cred_type = 'telegramApi'
        elif 'supabase' in node_type.lower():
            cred_type = 'supabaseApi'
        elif 'emailSend' in node_type or 'smtp' in node_name.lower():
            cred_type = 'smtp'
        
        if cred_type and cred_type in CRED_MAP:
            cred_info = CRED_MAP[cred_type]
            # Verificar se a credencial ja esta configurada
            existing_creds = node.get('credentials', {})
            if cred_type not in existing_creds or not existing_creds[cred_type].get('id'):
                node['credentials'] = node.get('credentials', {})
                node['credentials'][cred_type] = cred_info
                modified += 1
                print(f"  [INJETADO] Node [{node_name}] <- {cred_type}: {cred_info['name']}")
            else:
                print(f"  [OK] Node [{node_name}] ja tem credencial {cred_type}")
    
    if modified == 0:
        print(f"  Nenhuma credencial precisou ser injetada.")
        continue
    
    # 3. Limpar settings
    clean_settings = {}
    for k in allowed_settings_keys:
        if k in wf.get('settings', {}):
            clean_settings[k] = wf['settings'][k]
    
    # 4. PUT para atualizar
    update_payload = {
        "name": wf.get('name'),
        "nodes": wf.get('nodes'),
        "connections": wf.get('connections'),
        "settings": clean_settings
    }
    
    put_r = requests.put(f"{host}/workflows/{wf_id}", json=update_payload, headers=headers, verify=False, timeout=15)
    if put_r.status_code == 200:
        print(f"  [ATUALIZADO] Workflow salvo na nuvem!")
    else:
        print(f"  [ERRO PUT] {put_r.status_code} - {put_r.text[:250]}")
        continue
    
    # 5. Tentar ativar
    act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
    if act_r.status_code == 200:
        print(f"  [ATIVADO] {wf_name} esta VERDE!")
    else:
        try:
            msg = act_r.json().get('message', act_r.text[:250])
        except:
            msg = act_r.text[:250]
        print(f"  [FALHA ATIVACAO] {msg[:200]}")

# Contagem final
print(f"\n{'='*60}")
print(f"  CONTAGEM FINAL")
print(f"{'='*60}")
r2 = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
wfs = r2.json().get('data', [])
ativos = len([w for w in wfs if w.get('active')])
total = len(wfs)
inativos_list = [w for w in wfs if not w.get('active')]
print(f"Total: {total} | Ativos: {ativos} | Inativos: {total - ativos}")
print(f"Taxa operacional: {round(ativos/total*100)}%")

if inativos_list:
    print(f"\nWorkflows ainda inativos:")
    for w in inativos_list:
        print(f"  [OFF] {w.get('name')} ({w.get('id')})")
