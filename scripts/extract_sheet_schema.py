import json

filepath = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_MAQUINA_CONTEUDO_META_DL_4X_DIA.json'

with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Achar conexões para o node "Registro Final Google Sheets"
target_nodes = ["Registro Final Google Sheets", "Registro Bloqueado Sheets"]

print("=== Fluxo de Dados para as Planilhas ===")
for src_node, outputs in data.get('connections', {}).items():
    for out_type, out_links in outputs.items():
        for links in out_links:
            for link in links:
                if link['node'] in target_nodes:
                    print(f"[{src_node}] -> [{link['node']}]")
                    
                    # Vamos achar o src_node na lista de nodes para ver o que ele gera
                    for n in data.get('nodes', []):
                        if n['name'] == src_node:
                            print(json.dumps(n['parameters'], indent=2))
