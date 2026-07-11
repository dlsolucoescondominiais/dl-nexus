"""
DL NEXUS - Diagnostico do Agente DL no n8n
Verifica execucoes recentes, status e saude dos workflows de agente
"""
import os
import json
import urllib.request
import urllib.error
import ssl
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"

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

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Detectar key valida
n8n_api_key = ""
for kname, kval in keys_map.items():
    url = n8n_host + "workflows?limit=1"
    req = urllib.request.Request(url, headers={"X-N8N-API-KEY": kval, "Accept": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            if r.status == 200:
                n8n_api_key = kval
                break
    except:
        pass

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

print("=" * 65)
print("  DL NEXUS - STATUS DO AGENTE DL NO N8N")
print("=" * 65)

# 1. Listar todos os workflows
all_wfs = []
try:
    r1 = n8n_get("workflows?limit=250&active=true")
    r2 = n8n_get("workflows?limit=250&active=false")
    seen = set()
    for wf in r1.get("data", []) + r2.get("data", []):
        if wf["id"] not in seen:
            seen.add(wf["id"])
            all_wfs.append(wf)
except Exception as e:
    print(f"Erro ao listar workflows: {e}")
    exit(1)

# Keywords que identificam workflows de agente DL
AGENT_KEYWORDS = [
    "agente", "agent", "aninha", "inbound", "omnichannel",
    "zelador", "nexus", "atendimento", "prospeccao", "orcamento",
    "assistente", "bot", "chat", "ia", "ai", "motor", "publicador"
]

print(f"\nTotal de workflows no n8n: {len(all_wfs)}")
print()

# Filtrar workflows relacionados a agentes
agent_wfs = []
for wf in all_wfs:
    name_lower = wf.get("name", "").lower()
    if any(kw in name_lower for kw in AGENT_KEYWORDS):
        agent_wfs.append(wf)

print(f"[+] Workflows de Agente/IA encontrados: {len(agent_wfs)}")
print()
print(f"{'STATUS':<10} {'NOME':<55} {'ID'}")
print("-" * 90)

active_agents = []
inactive_agents = []

for wf in sorted(agent_wfs, key=lambda x: x.get("name", "")):
    status = "ATIVO" if wf.get("active") else "INATIVO"
    name = wf.get("name", "?")[:54]
    wf_id = wf.get("id", "?")
    marker = "[OK]" if wf.get("active") else "[--]"
    print(f"  {marker} {status:<8} {name:<55} {wf_id}")
    if wf.get("active"):
        active_agents.append(wf)
    else:
        inactive_agents.append(wf)

# 2. Verificar execucoes recentes
print()
print("[+] Execucoes recentes (ultimas 20):")
print("-" * 90)
try:
    exec_data = n8n_get("executions?limit=20&includeData=false")
    execs = exec_data.get("data", [])
    
    if not execs:
        print("  Nenhuma execucao encontrada.")
    else:
        # Mapear IDs para nomes
        id_to_name = {wf["id"]: wf.get("name", "?") for wf in all_wfs}
        
        for ex in execs:
            wf_id = ex.get("workflowId", "?")
            wf_name = id_to_name.get(wf_id, f"ID:{wf_id}")[:45]
            mode = ex.get("mode", "?")
            status = ex.get("status", "?")
            started = ex.get("startedAt", "?")
            
            # Formatar data
            if started and started != "?":
                try:
                    dt = datetime.fromisoformat(started.replace("Z", "+00:00"))
                    started = dt.strftime("%d/%m %H:%M")
                except:
                    started = started[:16]
            
            flag = "[OK]" if status in ("success", "running") else "[!!]"
            print(f"  {flag} {status:<10} {started:<12} {mode:<10} {wf_name}")
            
except Exception as e:
    print(f"  Erro ao buscar execucoes: {e}")

# 3. Resumo
print()
print("=" * 65)
print("  RESUMO DO AGENTE DL")
print("=" * 65)
print(f"  Workflows de agente ATIVOS:   {len(active_agents)}")
print(f"  Workflows de agente INATIVOS: {len(inactive_agents)}")
print()

if active_agents:
    print("  Agentes OPERACIONAIS agora:")
    for wf in active_agents:
        print(f"    + {wf.get('name')}")

if inactive_agents:
    print()
    print("  Agentes PARADOS:")
    for wf in inactive_agents:
        print(f"    - {wf.get('name')}")

print()
print("=" * 65)
