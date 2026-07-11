import json
import os
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

filepath = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Coloca um ID fake para testar se o n8n aceita a ativação
fake_id = "1bH2Jk3L4mN5oP6qR7sT8uV9wX0yZ1aB2cD3eF4gH5i"

for node in data.get('nodes', []):
    if node.get('type') == 'n8n-nodes-base.googleSheets':
        if 'parameters' in node and 'documentId' in node['parameters']:
            node['parameters']['documentId']['value'] = fake_id

with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Agora tenta dar o PUT no workflow para atualizar a nuvem
api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST', 'https://n8n.dlsolucoescondominiais.com.br/api/v1')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

url = f"{host}/workflows/B9XUWs7kT21FVQeo"
response = requests.put(url, json=data, headers=headers, verify=False)
print("PUT Status:", response.status_code)
if response.status_code == 200:
    print("Atualizado com sucesso na nuvem.")
    
    # Tenta ativar
    act_url = f"{url}/activate"
    act_resp = requests.post(act_url, headers=headers, verify=False)
    print("Activate Status:", act_resp.status_code)
    print("Activate Response:", act_resp.text)
else:
    print("Erro PUT:", response.text)
