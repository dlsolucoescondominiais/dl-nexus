"""
DEPLOY MASTER v2 — DL NEXUS
Fix: remove 'active' from body (read-only), use POST for activate
"""
import json, os, sys, requests, urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

from dotenv import load_dotenv
load_dotenv(r'd:\AntiGravity\projeto_01\.env')

N8N_HOST = os.getenv('N8N_HOST', '').rstrip('/')
N8N_API_KEY = os.getenv('N8N_API_KEY', '')

if '/api/v1' in N8N_HOST:
    API = N8N_HOST
else:
    API = f'{N8N_HOST}/api/v1'

H = {'Content-Type': 'application/json', 'X-N8N-API-KEY': N8N_API_KEY}
DIR = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS'

# ── FASE 1: Listar existentes ──
print('FASE 1: Listando...')
name_to_id = {}
try:
    r = requests.get(f'{API}/workflows?limit=200', headers=H, verify=False, timeout=30)
    r.raise_for_status()
    data = r.json().get('data', [])
    for w in data:
        name_to_id[w['name']] = {'id': w['id'], 'active': w.get('active', False)}
    print(f'  {len(data)} workflows no servidor')
except Exception as e:
    print(f'  ERRO: {e}')

# ── FASE 2: Deploy ──
print('\nFASE 2: Deploy...')
deploy = [
    '020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json',
    '070_CRON_MANUS_DIARIO.json',
    '092_MESA_APROVACAO_TELEGRAM_ANINHA.json',
    '140_ORGANIZADOR_DRIVE_MIDIA.json',
    '179_TESTES_PRECIFICACAO.json',
    '181_ORCAMENTO_INTERNO_WEBHOOK.json',
    '182_GERADOR_PROPOSTA_CATALOGO.json',
    '183_MOTOR_IA1_TECNICA.json',
    '184_MOTOR_IA2_COMERCIAL.json',
    '185_MOTOR_IA3_REDATORA.json',
    '190_MOTOR_ORCAMENTO_MASTER.json'
]

deployed = []
for fname in deploy:
    fp = os.path.join(DIR, fname)
    if not os.path.exists(fp):
        print(f'  SKIP {fname}')
        continue
    
    with open(fp, 'r', encoding='utf-8') as f:
        wf = json.load(f)
    
    wf_name = wf.get('name', fname.replace('.json',''))
    
    # Remove campos read-only e problemáticos
    for field in ['id','versionId','meta','pinData','active','createdAt','updatedAt']:
        wf.pop(field, None)
    wf['settings'] = {}
    
    # Limpar credenciais placeholder
    for node in wf.get('nodes', []):
        creds = node.get('credentials', {})
        if creds:
            placeholder = any('credential_id' in str(v.get('id','')) for v in creds.values() if isinstance(v, dict))
            if placeholder:
                node.pop('credentials')
    
    info = name_to_id.get(wf_name)
    if info:
        wf_id = info['id']
        try:
            r = requests.put(f'{API}/workflows/{wf_id}', headers=H, json=wf, verify=False, timeout=30)
            if r.status_code == 200:
                print(f'  OK {fname} -> ATUALIZADO (id={wf_id})')
                deployed.append((wf_id, wf_name))
            else:
                print(f'  FAIL {fname} -> {r.status_code}: {r.text[:150]}')
        except Exception as e:
            print(f'  FAIL {fname}: {e}')
    else:
        try:
            r = requests.post(f'{API}/workflows', headers=H, json=wf, verify=False, timeout=30)
            if r.status_code in [200, 201]:
                nid = r.json().get('id','?')
                print(f'  OK {fname} -> CRIADO (id={nid})')
                deployed.append((nid, wf_name))
            else:
                print(f'  FAIL {fname} -> {r.status_code}: {r.text[:150]}')
        except Exception as e:
            print(f'  FAIL {fname}: {e}')

# ── FASE 3: Ativar ──
print('\nFASE 3: Ativando...')
for wf_id, wf_name in deployed:
    try:
        # n8n API: Para ativar, faz POST /workflows/{id}/activate
        r = requests.post(f'{API}/workflows/{wf_id}/activate', headers=H, verify=False, timeout=30)
        if r.status_code == 200:
            print(f'  OK {wf_name} -> ATIVADO')
        else:
            # Fallback: tenta PATCH
            r2 = requests.patch(f'{API}/workflows/{wf_id}', headers=H, json={'active': True}, verify=False, timeout=30)
            if r2.status_code == 200:
                print(f'  OK {wf_name} -> ATIVADO (PATCH)')
            else:
                # Fallback 2: PUT com active=true removido do body mas no query
                print(f'  WARN {wf_name} -> {r.status_code}: {r.text[:100]}')
    except Exception as e:
        print(f'  FAIL {wf_name}: {e}')

# ── FASE 4: Ativar inativos existentes ──
print('\nFASE 4: Ativando inativos...')
deployed_ids = [d[0] for d in deployed]
ok = 0
for name, info in name_to_id.items():
    if info['active'] or info['id'] in deployed_ids:
        continue
    wid = info['id']
    try:
        r = requests.post(f'{API}/workflows/{wid}/activate', headers=H, verify=False, timeout=30)
        if r.status_code == 200:
            print(f'  OK {name}')
            ok += 1
        else:
            r2 = requests.patch(f'{API}/workflows/{wid}', headers=H, json={'active': True}, verify=False, timeout=30)
            if r2.status_code == 200:
                print(f'  OK {name} (PATCH)')
                ok += 1
            else:
                err = r.text[:80]
                print(f'  WARN {name}: {err}')
    except Exception as e:
        print(f'  FAIL {name}: {e}')

print(f'\nDONE: {len(deployed)} deployados, {ok} inativos ativados')
