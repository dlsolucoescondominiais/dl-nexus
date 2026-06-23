import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
headers={'X-N8N-API-KEY':key}

# IDs das versões que ficaram inativas/lixo
workflows_to_delete = {
    "002_roteador_aninha_v2": "E8a4tj2C0tSdROE6",
    "002_roteador_aninha_v3_killcritic": "jlzetL3lL0s4iOZ3",
    "002_roteador_aninha_v3_atendimento": "0AXm58td3Et7NYw0"
}

for name, wid in workflows_to_delete.items():
    req = urllib.request.Request(f'https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows/{wid}', headers=headers, method='DELETE')
    try:
        urllib.request.urlopen(req, context=ctx)
        print(f"🗑️ Deletado com sucesso: {name} (ID: {wid})")
    except Exception as e:
        print(f"Erro ao deletar {name}: {e}")
