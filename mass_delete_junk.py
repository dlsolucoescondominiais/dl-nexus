import os
import urllib.request, json, ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
headers={'X-N8N-API-KEY':key}
host = "https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows"

junk_names = [
    "000_email_receptor",
    "001_webhook_receptor_enterprise",
    "My workflow"
]

print("Iniciando varredura final de lixo...")

try:
    req = urllib.request.Request(host, headers=headers, method="GET")
    resp = urllib.request.urlopen(req, context=ctx)
    data = json.loads(resp.read().decode('utf-8'))
    workflows = data.get('data', [])
    
    count = 0
    for w in workflows:
        w_name = w.get('name')
        w_id = w.get('id')
        
        if w_name in junk_names:
            print(f"Alvo detectado: {w_name} (ID: {w_id}). Deletando...")
            try:
                del_req = urllib.request.Request(f"{host}/{w_id}", headers=headers, method="DELETE")
                urllib.request.urlopen(del_req, context=ctx)
                print(f"[OK] {w_name} deletado com sucesso.")
                count += 1
            except Exception as e:
                print(f"[ERRO] Falha ao deletar {w_name}: {e}")
                
    print(f"\nOperacao concluida. Total de workflows deletados: {count}")
    
except Exception as e:
    print(f"Erro ao buscar workflows: {e}")
