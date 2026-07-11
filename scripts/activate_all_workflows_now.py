"""
DL NEXUS - Ativacao em Massa de Workflows n8n
Sincronizacao: Jules <-> Antigravity <-> GitHub <-> n8n
"""
import os
import json
import urllib.request
import urllib.error
import ssl
import sys

# Forcar encoding UTF-8 no stdout
sys.stdout.reconfigure(encoding='utf-8')

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

# Carregar credenciais
keys_map = {}
n8n_host = ""
with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        for kname in ["N8N_API_KEY", "N8N_JULES_ANTIGRAVITY", "N8N_API_KEY_2"]:
            if line.startswith(f"{kname}="):
                keys_map[kname] = line.split("=", 1)[1].strip()
        if line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

# Testar qual API key e valida
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def test_key(key):
    url = n8n_host + "workflows?limit=1"
    req = urllib.request.Request(url, headers={"X-N8N-API-KEY": key, "Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            return r.status == 200
    except:
        return False

n8n_api_key = ""
for kname, kval in keys_map.items():
    print(f"  Testando chave {kname}...")
    if test_key(kval):
        n8n_api_key = kval
        print(f"  [OK] Chave valida: {kname}")
        break

if not n8n_api_key:
    print("  [ERRO] Nenhuma chave valida encontrada. Verifique as API Keys no n8n.")
    exit(1)

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def n8n_get(endpoint):
    url = n8n_host + endpoint
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

def n8n_patch(endpoint, payload=None):
    url = n8n_host + endpoint
    data = json.dumps(payload or {}).encode("utf-8") if payload else b"{}"
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

def activate_workflow(wf_id, wf_name):
    """Ativa um workflow via POST /workflows/{id}/activate"""
    url = n8n_host + f"workflows/{wf_id}/activate"
    req = urllib.request.Request(url, data=b"{}", headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            return True, None
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.read().decode('utf-8')[:200]}"
    except Exception as e:
        return False, str(e)

print("=" * 60)
print("  DL NEXUS - SYNC JULES <-> ANTIGRAVITY <-> N8N")
print("=" * 60)
print(f"  Host: {n8n_host}")
print()

# 1. Listar todos os workflows
print("[1/3] Listando todos os workflows...")
try:
    # n8n API pode paginar - buscar até 500
    result = n8n_get("workflows?limit=250&active=false")
    all_wfs = result.get("data", [])
    
    # Buscar também os ativos
    result_active = n8n_get("workflows?limit=250&active=true")
    all_wfs += result_active.get("data", [])
    
    # Deduplicar por ID
    seen_ids = set()
    unique_wfs = []
    for wf in all_wfs:
        if wf["id"] not in seen_ids:
            seen_ids.add(wf["id"])
            unique_wfs.append(wf)
    
    print(f"  Total encontrado: {len(unique_wfs)} workflows")
except Exception as e:
    print(f"  ERRO ao listar: {e}")
    exit(1)

# 2. Classificar
inactive = [w for w in unique_wfs if not w.get("active", False)]
active   = [w for w in unique_wfs if w.get("active", False)]
print(f"  Ativos: {len(active)} | Inativos: {len(inactive)}")
print()

# 3. Ativar todos os inativos
print("[2/3] Ativando workflows inativos...")
activated = []
failed = []

for wf in inactive:
    wf_id   = wf["id"]
    wf_name = wf.get("name", wf_id)
    ok, err = activate_workflow(wf_id, wf_name)
    if ok:
        activated.append(wf_name)
        print(f"  ✅ ATIVADO: {wf_name}")
    else:
        failed.append((wf_name, err))
        print(f"  ❌ FALHOU:  {wf_name} → {err}")

print()
print("[3/3] RELATÓRIO FINAL")
print("=" * 60)
print(f"  Já estavam ativos:   {len(active)}")
print(f"  Ativados agora:      {len(activated)}")
print(f"  Falhas:              {len(failed)}")
print()

if failed:
    print("  Workflows com falha:")
    for name, err in failed:
        print(f"    • {name}: {err}")

print()
print("  SYNC CONCLUÍDO: GitHub → Antigravity → n8n ✅")
print("=" * 60)
