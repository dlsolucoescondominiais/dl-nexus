import urllib.request, json, ssl, os

ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

env_path = r'd:\AntiGravity\projeto_01\.env'
env_vars = {}
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '=' in line:
            k, v = line.strip().split('=', 1)
            env_vars[k] = v

n8n_key = env_vars.get('N8N_API_KEY')
n8n_host = env_vars.get('N8N_HOST')

if not n8n_host.endswith('/'):
    n8n_host += '/'

headers = {'X-N8N-API-KEY': n8n_key, 'Content-Type': 'application/json', 'Accept': 'application/json'}

# 1. Obter todos os workflows existentes
print("Buscando workflows existentes no n8n...")
req_get = urllib.request.Request(n8n_host + 'workflows', headers=headers)
try:
    res = urllib.request.urlopen(req_get, context=ctx)
    existing_wfs = json.loads(res.read().decode('utf-8')).get('data', [])
    existing_map = {w['name']: w for w in existing_wfs}
    print(f"Encontrados {len(existing_wfs)} workflows no n8n.")
except Exception as e:
    print("ERRO ao buscar workflows:", e)
    existing_map = {}

folder = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS'
files = [f for f in os.listdir(folder) if f.endswith('.json')]

resultados = {'sucesso': 0, 'erro': 0, 'erros_detalhes': []}

for f in files:
    try:
        w_data = json.load(open(os.path.join(folder, f), encoding='utf-8'))
        w_name = w_data.get('name')
        if not w_name:
            continue
            
        payload = {
            'name': w_name,
            'nodes': w_data.get('nodes', []),
            'connections': w_data.get('connections', {}),
            'settings': w_data.get('settings', {})
        }
        
        wf_id = None
        
        if w_name in existing_map:
            # UPDATE
            wf_id = existing_map[w_name]['id']
            print(f"[{f}] Atualizando workflow existente ({wf_id})...")
            req_put = urllib.request.Request(n8n_host + 'workflows/' + wf_id, data=json.dumps(payload).encode('utf-8'), headers=headers, method='PUT')
            try:
                urllib.request.urlopen(req_put, context=ctx)
            except urllib.error.HTTPError as e:
                # Fallback to empty settings if validation fails
                payload['settings'] = {}
                req_put2 = urllib.request.Request(n8n_host + 'workflows/' + wf_id, data=json.dumps(payload).encode('utf-8'), headers=headers, method='PUT')
                urllib.request.urlopen(req_put2, context=ctx)
        else:
            # CREATE
            print(f"[{f}] Criando novo workflow...")
            req_post = urllib.request.Request(n8n_host + 'workflows', data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            try:
                res_post = urllib.request.urlopen(req_post, context=ctx)
                created_wf = json.loads(res_post.read().decode('utf-8'))
                wf_id = created_wf['id']
            except urllib.error.HTTPError as e:
                # Fallback to empty settings if validation fails
                payload['settings'] = {}
                req_post2 = urllib.request.Request(n8n_host + 'workflows', data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
                res_post2 = urllib.request.urlopen(req_post2, context=ctx)
                created_wf = json.loads(res_post2.read().decode('utf-8'))
                wf_id = created_wf['id']
        
        # ACTIVATE
        if wf_id:
            try:
                req_act = urllib.request.Request(n8n_host + 'workflows/' + wf_id + '/activate', data=b'{}', headers=headers, method='POST')
                urllib.request.urlopen(req_act, context=ctx)
                print(f"[{f}] -> ATIVADO COM SUCESSO!")
                resultados['sucesso'] += 1
            except urllib.error.HTTPError as act_e:
                print(f"[{f}] -> ERRO AO ATIVAR: {act_e.read().decode('utf-8')}")
                resultados['erros_detalhes'].append(f"{f}: Erro Ativação ({act_e.code})")
                resultados['erro'] += 1
                
    except Exception as e:
        print(f"[{f}] -> ERRO GERAL: {e}")
        resultados['erros_detalhes'].append(f"{f}: {str(e)}")
        resultados['erro'] += 1

print("\n--- RESUMO DA OPERAÇÃO ---")
print(f"Workflows ativados com sucesso: {resultados['sucesso']}")
print(f"Workflows com erro: {resultados['erro']}")
if resultados['erros_detalhes']:
    for err in resultados['erros_detalhes']:
        print("  -", err)
