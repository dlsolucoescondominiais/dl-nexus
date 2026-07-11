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

allowed_settings_keys = ['executionOrder', 'saveManualExecutions', 'callerPolicy', 'errorWorkflow']

def clean_and_update(wf_id, wf_data):
    clean_settings = {}
    for k in allowed_settings_keys:
        if k in wf_data.get('settings', {}):
            clean_settings[k] = wf_data['settings'][k]
    payload = {
        "name": wf_data.get('name'),
        "nodes": wf_data.get('nodes'),
        "connections": wf_data.get('connections'),
        "settings": clean_settings
    }
    return requests.put(f"{host}/workflows/{wf_id}", json=payload, headers=headers, verify=False, timeout=15)

# ===== FIX 1: AGENTE_ZELADOR_CLASSIFICADOR_V1 =====
# Problema: Supabase Update usa operacao "update" mas o n8n v2.12 pode exigir
# que "filterType" ou "filtersUI" sejam definidos. Vamos adicionar filterType.
print("=" * 60)
print("  FIX 1: AGENTE_ZELADOR_CLASSIFICADOR_V1")
print("=" * 60)

wf_id = '1ndeOglNFeEKvXAT'
r = requests.get(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
wf = r.json()

for node in wf.get('nodes', []):
    if node.get('name') == 'Supabase Update':
        # Adicionar filterType para resolver "Missing or invalid required parameters"
        node['parameters']['filterType'] = 'string'
        print(f"  [INJETADO] filterType=string no node Supabase Update")

put_r = clean_and_update(wf_id, wf)
if put_r.status_code == 200:
    print(f"  [ATUALIZADO] Workflow salvo!")
    act_r = requests.post(f"{host}/workflows/{wf_id}/activate", headers=headers, verify=False, timeout=15)
    if act_r.status_code == 200:
        print(f"  [ATIVADO] AGENTE_ZELADOR_CLASSIFICADOR_V1 esta VERDE!")
    else:
        msg = act_r.json().get('message', act_r.text[:250]) if act_r.text else 'N/A'
        print(f"  [FALHA] {msg[:200]}")
else:
    print(f"  [ERRO PUT] {put_r.status_code} - {put_r.text[:250]}")

# ===== FIX 2: 152_ANINHA_VOZ_AGENDA =====
# Problema 1: "Baixar Audio" (Telegram) - falta resource e operation
# Problema 2: "Transcricao Whisper" (OpenAI) - falta credencial
print("\n" + "=" * 60)
print("  FIX 2: 152_ANINHA_VOZ_AGENDA")
print("=" * 60)

wf_id2 = 'ZJ9F3OIfw9k8psJw'
r2 = requests.get(f"{host}/workflows/{wf_id2}", headers=headers, verify=False, timeout=15)
wf2 = r2.json()

for node in wf2.get('nodes', []):
    name = node.get('name', '')
    
    if name == 'Baixar Áudio':
        # Telegram node precisa de resource e operation para download
        node['parameters']['resource'] = 'file'
        node['parameters']['operation'] = 'get'
        print(f"  [INJETADO] resource=file, operation=get no node Baixar Audio")
    
    if 'Whisper' in name or 'Transcri' in name:
        # Injetar credencial OpenAI
        node['credentials'] = node.get('credentials', {})
        node['credentials']['openAiApi'] = {
            'id': '3qLmNTIyyFgIGSHq',
            'name': 'OpenAi account'
        }
        print(f"  [INJETADO] openAiApi: OpenAi account no node {name}")

put_r2 = clean_and_update(wf_id2, wf2)
if put_r2.status_code == 200:
    print(f"  [ATUALIZADO] Workflow salvo!")
    act_r2 = requests.post(f"{host}/workflows/{wf_id2}/activate", headers=headers, verify=False, timeout=15)
    if act_r2.status_code == 200:
        print(f"  [ATIVADO] 152_ANINHA_VOZ_AGENDA esta VERDE!")
    else:
        msg = act_r2.json().get('message', act_r2.text[:250]) if act_r2.text else 'N/A'
        print(f"  [FALHA] {msg[:200]}")
else:
    print(f"  [ERRO PUT] {put_r2.status_code} - {put_r2.text[:250]}")

# Contagem final
print(f"\n{'='*60}")
print(f"  CONTAGEM FINAL")
print(f"{'='*60}")
r3 = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
wfs = r3.json().get('data', [])
ativos = len([w for w in wfs if w.get('active')])
total = len(wfs)
print(f"Total: {total} | Ativos: {ativos} | Inativos: {total - ativos}")
print(f"Taxa operacional: {round(ativos/total*100)}%")

inativos_list = [w for w in wfs if not w.get('active')]
if inativos_list:
    print(f"\nRestantes inativos:")
    for w in inativos_list:
        print(f"  [OFF] {w.get('name')} ({w.get('id')})")
