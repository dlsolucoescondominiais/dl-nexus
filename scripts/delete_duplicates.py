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

# Duplicatas com conflito de webhook identificadas no diagnostico
duplicatas = [
    ('u9xXNNLTlb1qkZeO', '050_AGENTE_SDR_SOCIAL_DL', '9fzu8hicfujfyJnK'),
    ('gS8s50b5UI4HZ6SO', '020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO', 'publicadorSocialDlNexusV320260518'),
]

for dup_id, dup_name, original_id in duplicatas:
    print(f"=== Limpando duplicata: {dup_name} ===")
    print(f"   Duplicata (deletar): {dup_id}")
    print(f"   Original (manter):   {original_id}")
    
    # Deletar a duplicata
    r = requests.delete(f"{host}/workflows/{dup_id}", headers=headers, verify=False, timeout=15)
    if r.status_code == 200:
        print(f"   [DELETADO] Duplicata removida com sucesso!")
    else:
        print(f"   [ERRO] HTTP {r.status_code} - {r.text[:200]}")
    print()

# Contagem final
print("--- CONTAGEM FINAL ---")
r2 = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
wfs = r2.json().get('data', [])
ativos = len([w for w in wfs if w.get('active')])
total = len(wfs)
print(f"Total: {total} | Ativos: {ativos} | Inativos: {total - ativos}")
print(f"Taxa operacional: {round(ativos/total*100)}%")
