import os
import sys
import json
import requests
import urllib3

# Fix encoding no Windows
sys.stdout.reconfigure(encoding='utf-8')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('N8N_API_KEY')
host = os.getenv('N8N_HOST', 'https://n8n.dlsolucoescondominiais.com.br/api/v1')
headers = {'X-N8N-API-KEY': api_key, 'Content-Type': 'application/json'}

print("=" * 70)
print("  DIAGNOSTICO COMPLETO DO N8N - DL SOLUCOES CONDOMINIAIS")
print("=" * 70)

# 1. TESTE DE CONECTIVIDADE
print("\n[1/6] TESTE DE CONECTIVIDADE...")
try:
    r = requests.get(f"{host}/workflows", headers=headers, verify=False, timeout=15)
    if r.status_code == 200:
        print("   [OK] API do n8n ONLINE e respondendo.")
    else:
        print(f"   [ERRO] API respondeu com erro: HTTP {r.status_code}")
        print(f"      Detalhe: {r.text[:200]}")
except Exception as e:
    print(f"   [FALHA] CONEXAO: {e}")
    sys.exit(1)

# 2. INVENTARIO DE WORKFLOWS
print("\n[2/6] INVENTARIO DE WORKFLOWS...")
data = r.json()
workflows = data.get('data', [])
total = len(workflows)
ativos = [w for w in workflows if w.get('active')]
inativos = [w for w in workflows if not w.get('active')]
print(f"   Total: {total} workflows")
print(f"   [OK] Ativos: {len(ativos)}")
print(f"   [!!] Inativos: {len(inativos)}")

# 3. LISTAR CREDENCIAIS
print("\n[3/6] VERIFICACAO DE CREDENCIAIS...")
try:
    cred_r = requests.get(f"{host}/credentials", headers=headers, verify=False, timeout=15)
    if cred_r.status_code == 200:
        creds = cred_r.json().get('data', [])
        print(f"   Total de credenciais registradas: {len(creds)}")
        for c in creds:
            print(f"   [CHAVE] [{c.get('type', 'N/A')}] {c.get('name')} (ID: {c.get('id')})")
    else:
        print(f"   [!!] Nao foi possivel listar credenciais: HTTP {cred_r.status_code}")
except Exception as e:
    print(f"   [ERRO] Erro ao buscar credenciais: {e}")

# 4. VERIFICAR EXECUCOES RECENTES
print("\n[4/6] EXECUCOES RECENTES (ultimas 20)...")
try:
    exec_r = requests.get(f"{host}/executions?limit=20", headers=headers, verify=False, timeout=15)
    if exec_r.status_code == 200:
        executions = exec_r.json().get('data', [])
        print(f"   Total retornado: {len(executions)}")
        sucesso = 0
        erro = 0
        esperando = 0
        for ex in executions:
            status = ex.get('status', 'unknown')
            wf_name = ex.get('workflowData', {}).get('name', ex.get('workflowId', 'N/A'))
            finished = ex.get('stoppedAt', 'em andamento')
            if status == 'success':
                sucesso += 1
            elif status == 'error':
                erro += 1
                print(f"   [ERRO] {wf_name} | Finalizado: {finished}")
            elif status in ('running', 'waiting'):
                esperando += 1
        print(f"   [OK] Sucesso: {sucesso} | [ERRO] Erro: {erro} | [WAIT] Aguardando: {esperando}")
    else:
        print(f"   [!!] Nao foi possivel listar execucoes: HTTP {exec_r.status_code}")
except Exception as e:
    print(f"   [ERRO] Erro ao buscar execucoes: {e}")

# 5. LISTAR WORKFLOWS INATIVOS
print("\n[5/6] WORKFLOWS INATIVOS (detalhes)...")
for w in inativos:
    print(f"   [OFF] [{w.get('id')}] {w.get('name')}")

# 6. TENTAR ATIVAR OS INATIVOS
print("\n[6/6] TENTATIVA DE ATIVACAO EM MASSA DOS INATIVOS...")
ativados_ok = 0
ativados_erro = 0
erros_detalhados = []

for w in inativos:
    wid = w.get('id')
    wname = w.get('name')
    try:
        act_r = requests.post(f"{host}/workflows/{wid}/activate", headers=headers, verify=False, timeout=15)
        if act_r.status_code == 200:
            ativados_ok += 1
            print(f"   [ATIVADO] {wname}")
        else:
            ativados_erro += 1
            try:
                msg = act_r.json().get('message', act_r.text[:150])
            except:
                msg = act_r.text[:150]
            erros_detalhados.append({'name': wname, 'id': wid, 'error': msg})
            print(f"   [FALHA] {wname} -> {msg[:120]}")
    except Exception as e:
        ativados_erro += 1
        erros_detalhados.append({'name': wname, 'id': wid, 'error': str(e)})
        print(f"   [REDE] {wname} -> {e}")

# RESUMO FINAL
print("\n" + "=" * 70)
print("  RESUMO DO DIAGNOSTICO")
print("=" * 70)
print(f"  API Online: SIM")
print(f"  Workflows Totais: {total}")
print(f"  Ja Ativos: {len(ativos)}")
print(f"  Ativados Agora: {ativados_ok}")
print(f"  Falharam na Ativacao: {ativados_erro}")

if erros_detalhados:
    print(f"\n  === DETALHES DOS ERROS DE ATIVACAO ===")
    for e in erros_detalhados:
        print(f"  [{e['id']}] {e['name']}")
        print(f"     Erro: {e['error'][:250]}")
        print()
