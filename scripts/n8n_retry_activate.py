import os
import sys
import requests
import urllib3
sys.stdout.reconfigure(encoding='utf-8')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

# Tentar reativar workflows que dependiam de sub-workflows agora publicados
retry_ids = [
    ('rP1oaUomnwc10ihy', '070_CRON_MARKETING_INSTITUCIONAL_DL_OPENAI'),
]

for wid, wname in retry_ids:
    print(f"Retentando ativacao: {wname}...")
    r = requests.post(f"{host}/workflows/{wid}/activate", headers=headers, verify=False, timeout=15)
    if r.status_code == 200:
        print(f"   [ATIVADO] {wname}")
    else:
        try:
            msg = r.json().get('message', r.text[:200])
        except:
            msg = r.text[:200]
        print(f"   [FALHA] {msg}")

# Verificar contagem final
print("\n--- CONTAGEM FINAL ---")
r2 = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
wfs = r2.json().get('data', [])
ativos = len([w for w in wfs if w.get('active')])
total = len(wfs)
print(f"Total: {total} | Ativos: {ativos} | Inativos: {total - ativos}")
print(f"Taxa operacional: {round(ativos/total*100)}%")
