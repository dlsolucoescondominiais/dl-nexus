import json

f = open(r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json', 'r', encoding='utf-8')
data = json.load(f)
f.close()

print(f"Nodes: {len(data['nodes'])}")
print(f"Connections: {len(data['connections'])}")
for n in data['nodes']:
    print(f"  - {n['name']} ({n['type']})")
print("\nJSON válido: SIM")
