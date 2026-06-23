import os
import json
import urllib.request
import ssl

filepath = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

with open(filepath, "r", encoding="utf-8") as f:
    data = json.loads(f.read())

nodes = data.get("nodes", [])

for n in nodes:
    if n.get("name") == "Gerar Textos IA":
        n["credentials"] = {
            "openAiApi": {
                "id": "1", # Ou um ID fixo, mas n8n v1 aceita o ID da string as vezes, mas a api precisa ter. Vou tentar injetar sem o ID exato ou procurar o node.
                "name": "OpenAi Api"
            }
        }

data["nodes"] = nodes

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
