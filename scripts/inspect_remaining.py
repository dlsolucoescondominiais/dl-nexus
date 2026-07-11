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

# ===== FIX 1: AGENTE_ZELADOR_CLASSIFICADOR_V1 =====
# Erro: Supabase Update - Missing or invalid required parameters
# Vamos investigar o que falta
print("=" * 60)
print("  FIX 1: AGENTE_ZELADOR_CLASSIFICADOR_V1")
print("=" * 60)

wf_id = '1ndeOglNFeEKvXAT'
r = requests.get(f"{host}/workflows/{wf_id}", headers=headers, verify=False, timeout=15)
wf = r.json()

for node in wf.get('nodes', []):
    if 'supabase' in node.get('type', '').lower():
        print(f"\n  Node: {node['name']}")
        print(f"  Type: {node['type']}")
        print(f"  Credentials: {node.get('credentials', {})}")
        print(f"  Parameters: {json.dumps(node.get('parameters', {}), indent=4)}")

# ===== FIX 2: 152_ANINHA_VOZ_AGENDA =====
# Erro: Baixar Audio (params faltando) + Transcricao Whisper (credencial OpenAI)
print("\n" + "=" * 60)
print("  FIX 2: 152_ANINHA_VOZ_AGENDA")
print("=" * 60)

wf_id2 = 'ZJ9F3OIfw9k8psJw'
r2 = requests.get(f"{host}/workflows/{wf_id2}", headers=headers, verify=False, timeout=15)
wf2 = r2.json()

problem_nodes = ['Baixar', 'Transcri', 'Whisper']
for node in wf2.get('nodes', []):
    name = node.get('name', '')
    if any(p.lower() in name.lower() for p in problem_nodes):
        print(f"\n  Node: {node['name']}")
        print(f"  Type: {node['type']}")
        print(f"  Credentials: {node.get('credentials', {})}")
        print(f"  Parameters: {json.dumps(node.get('parameters', {}), indent=4)}")
