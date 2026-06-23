import json

file_path = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

with open(file_path, 'r', encoding='utf-8') as f:
    w20 = json.load(f)

# Fix connection name
for conn_name, output_ports in w20.get('connections', {}).items():
    if conn_name == "IF KILLCRITIC Aprovado?":
        for i, branch in enumerate(output_ports.get('main', [])):
            for j, dest in enumerate(branch):
                if dest.get('node') == 'Telegram Enviar Prévia':
                    w20['connections']['IF KILLCRITIC Aprovado?']['main'][i][j]['node'] = 'Telegram Aviso Publicacao'

# Fix Entrada do Post reference which crashes when triggered from Execute Workflow Trigger
for n in w20.get('nodes', []):
    if n['name'] == 'NORMALIZAR_SAIDA_IA_SOCIAL':
        n['parameters']['jsCode'] = n['parameters']['jsCode'].replace(
            "const entrada = $('Entrada do Post').item.json || {};",
            "let entrada = {}; try { entrada = $('Entrada do Post').item.json || {}; } catch(e) { entrada = $('Execute Workflow Trigger').item.json || {}; }"
        )
    if n['name'] == 'Telegram Alerta Bloqueio' or n['name'] == 'Telegram Aviso Publicacao':
        n['parameters']['text'] = n['parameters']['text'].replace(
            "$('Entrada do Post').item.json.tema",
            "(typeof $('Entrada do Post') !== 'undefined' ? $('Entrada do Post').item.json.tema : 'B2B Manus')"
        )
    if n['name'] == 'Facebook Publish' or n['name'] == 'Instagram Media Container':
        if 'bodyParameters' in n['parameters']:
            for param in n['parameters']['bodyParameters'].get('parameters', []):
                if 'Entrada do Post' in param.get('value', ''):
                    param['value'] = param['value'].replace(
                        "$('Entrada do Post').item.json.image_url",
                        "(typeof $('Entrada do Post') !== 'undefined' ? $('Entrada do Post').item.json.image_url : '')"
                    )
    if n['name'] == 'Facebook Publish':
        if 'url' in n['parameters']:
            n['parameters']['url'] = n['parameters']['url'].replace(
                "$('Entrada do Post').item.json.image_url",
                "(typeof $('Entrada do Post') !== 'undefined' ? $('Entrada do Post').item.json.image_url : '')"
            )

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(w20, f, indent=2, ensure_ascii=False)

print("FIX APLICADO NO 020")
