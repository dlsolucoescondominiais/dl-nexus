import json
from pathlib import Path

base = Path(r"D:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N")

# ---------- 019 ORÇAMENTO ----------
orc_path = base / "019_GERADOR_ORCAMENTO_RAPIDO_config.json"
orc_out = base / "019_GERADOR_ORCAMENTO_RAPIDO_config_FIXED.json"

with open(orc_path, "r", encoding="utf-8-sig") as f:
    orc = json.load(f)

orc["id"] = orc.get("id") or "orcamentoRapidoSafe20260517"
orc["active"] = False

with open(orc_out, "w", encoding="utf-8") as f:
    json.dump(orc, f, ensure_ascii=False, indent=2)

# ---------- 060 MANUS SEGURO ----------
manus_path = base / "060_AGENT_MANUS_PROSPECCAO_ATIVA_config.json"
manus_out = base / "060_AGENT_MANUS_PROSPECCAO_ATIVA_config_SAFE_SEM_DISPARO.json"

with open(manus_path, "r", encoding="utf-8-sig") as f:
    manus = json.load(f)

manus["id"] = manus.get("id") or "manusProspeccaoSafe20260517"
manus["name"] = "060_AGENT_MANUS_PROSPECCAO_ATIVA_SAFE_SEM_DISPARO"
manus["active"] = False

for node in manus.get("nodes", []):
    if node.get("name") == "Disparar WhatsApp (Meta API)":
        node["disabled"] = True
        node["name"] = "DESATIVADO - Disparar WhatsApp (Meta API)"

connections = manus.get("connections", {})
if "IA Escreve a Mensagem" in connections:
    connections["IA Escreve a Mensagem"]["main"] = [[]]

with open(manus_out, "w", encoding="utf-8") as f:
    json.dump(manus, f, ensure_ascii=False, indent=2)

print("Arquivos criados com segurança:")
print(orc_out)
print(manus_out)

for path in [orc_out, manus_out]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print("")
    print("Arquivo:", path.name)
    print("id:", data.get("id"))
    print("name:", data.get("name"))
    print("active:", data.get("active"))
    print("nodes:", len(data.get("nodes", [])))
    print("connections:", bool(data.get("connections")))
