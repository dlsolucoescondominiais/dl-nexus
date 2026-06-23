import json

file_path_70 = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json"

with open(file_path_70, "r", encoding="utf-8") as f:
    w70 = json.load(f)

# Remover Chamar MarkSolar (020)
w70["nodes"] = [n for n in w70["nodes"] if n["name"] != "Chamar MarkSolar (020)"]

# Atualizar as conexões do Status Pronto?
if "Status Pronto?" in w70["connections"]:
    # O nó "Status Pronto?" tinha dois outputs no branch "done" (0): Chamar MarkSolar (020) e Telegram Entrega.
    # Vamos deixar apenas o Telegram Entrega.
    w70["connections"]["Status Pronto?"]["main"][0] = [
        dest for dest in w70["connections"]["Status Pronto?"]["main"][0]
        if dest["node"] != "Chamar MarkSolar (020)"
    ]

with open(file_path_70, "w", encoding="utf-8") as f:
    json.dump(w70, f, indent=2, ensure_ascii=False)

print("070_CRON_MANUS_DIARIO.json corrigido: desvinculado do 020.")
