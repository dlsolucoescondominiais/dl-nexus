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

# Pegar execucoes 3218 e 3217 (as mais recentes - nossos testes de planilha)
for ex_id in ['3218', '3217']:
    print(f"=== Detalhes execucao {ex_id} ===")
    r = requests.get(f"{host}/executions/{ex_id}?includeData=true", headers=headers, verify=False, timeout=15)
    if r.status_code == 200:
        data = r.json()
        # Imprimir tudo relevante
        run_data = data.get('data', {}).get('resultData', {})
        
        # Erro geral
        last_error = run_data.get('error', {})
        if last_error:
            print(f"  ERRO GERAL: {json.dumps(last_error, indent=2)[:500]}")
        
        # Erros por node
        for node_name, runs in run_data.get('runData', {}).items():
            for run in runs:
                err = run.get('error')
                if err:
                    print(f"  Node [{node_name}]:")
                    print(f"    message: {err.get('message', 'N/A')[:300]}")
                    print(f"    description: {err.get('description', 'N/A')[:300]}")
                    print(f"    httpCode: {err.get('httpCode', 'N/A')}")
    else:
        print(f"  HTTP {r.status_code}: {r.text[:200]}")
    print()
