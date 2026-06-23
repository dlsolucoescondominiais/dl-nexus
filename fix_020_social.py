import json
from pathlib import Path

base = Path(r"D:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N")

src = base / "020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_config.json"
dst = base / "020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_config_FIXED.json"

with open(src, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

data["id"] = "publicadorSocialDlNexusV320260518"
data["name"] = "020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO"
data["active"] = False

with open(dst, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Arquivo corrigido:", dst)
print("id:", data["id"])
print("name:", data["name"])
print("active:", data["active"])
