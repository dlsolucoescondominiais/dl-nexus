import json

file_path = "d:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"
out_path = "d:/AntiGravity/projeto_01/DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_FIXED.json"

with open(file_path, "r", encoding="utf-8") as f:
    wf = json.load(f)

nodes = wf.get("nodes", [])
connections = wf.get("connections", {})

# Remove old nodes
nodes_to_remove = ["Facebook Publish", "Instagram Media Container", "Instagram Publish Container"]
new_nodes = [n for n in nodes if n["name"] not in nodes_to_remove]

# Add Python Node
python_node = {
    "parameters": {
        "command": "python d:/AntiGravity/projeto_01/execution/post_social_api.py {{{{ Buffer.from(JSON.stringify($('NORMALIZAR_SAIDA_IA_SOCIAL').item.json)).toString('base64') }}}}",
    },
    "id": "python_fb_ig",
    "name": "Python FB/IG",
    "type": "n8n-nodes-base.executeCommand",
    "typeVersion": 1,
    "position": [1800, -300]
}
new_nodes.append(python_node)

# Add Schedule Trigger
schedule_node = {
    "parameters": {
        "rule": {
            "interval": [
                {
                    "field": "cronExpression",
                    "expression": "0 9 * * *"
                }
            ]
        }
    },
    "id": "schedule_trigger",
    "name": "Schedule Trigger",
    "type": "n8n-nodes-base.scheduleTrigger",
    "typeVersion": 1.1,
    "position": [0, -200]
}
new_nodes.append(schedule_node)

wf["nodes"] = new_nodes

# Update connections
# Telegram Aviso Publicacao -> Python FB/IG
if "Telegram Aviso Publicacao" in connections:
    connections["Telegram Aviso Publicacao"]["main"] = [[{"node": "Python FB/IG", "type": "main", "index": 0}]]

# Python FB/IG -> HTTP: Google Business Profile
connections["Python FB/IG"] = {
    "main": [[{"node": "HTTP: Google Business Profile", "type": "main", "index": 0}]]
}

# Remove old connections
for node_name in nodes_to_remove:
    if node_name in connections:
        del connections[node_name]
        
# Add Schedule Trigger to set_entrada
connections["Schedule Trigger"] = {
    "main": [[{"node": "Entrada do Post", "type": "main", "index": 0}]]
}

wf["connections"] = connections

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)

print("Workflow modificado com sucesso.")
