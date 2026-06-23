import json

file_path = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json"

with open(file_path, 'r', encoding='utf-8') as f:
    w20 = json.load(f)

# Modificar 020
for n in w20.get('nodes', []):
    if n['name'] == 'Gerar Textos IA':
        n['parameters']['messages']['messageValues'][1]['content'] = '={{ "A Estratégia Ditada pelo Manus AI é:\\n\\n" + JSON.stringify($json) + "\\n\\nCanais Oficiais DL Soluções (use sempre no CTA):\\n- Site: https://dlsolucoescondominiais.com\\n- Instagram: https://www.instagram.com/dl.solucoescondominiais/\\n- WhatsApp da Aninha (CTA Principal): https://wa.me/5521968907139?text=Quero+agendar+uma+Avaliação+Técnica\\n\\nRegras obrigatórias:\\n- O CTA DEVE sempre ser \\"Avaliação Técnica\\" e direcionar pro WhatsApp da Aninha final 39.\\n- NUNCA prometer \\"visita técnica\\".\\n- Alvo: síndicos, colégios e pequenos/médios condomínios do RJ.\\n\\nForneça a resposta em JSON estrito com as chaves: legenda_facebook, legenda_instagram, texto_telegram, hashtags, cta" }}'

has_ewt = any(n['type'] == 'n8n-nodes-base.executeWorkflowTrigger' for n in w20.get('nodes', []))
if not has_ewt:
    w20['nodes'].append({'parameters': {}, 'id': 'execute_workflow_trigger', 'name': 'Execute Workflow Trigger', 'type': 'n8n-nodes-base.executeWorkflowTrigger', 'typeVersion': 1, 'position': [-200, 200]})
    w20['connections']['Execute Workflow Trigger'] = {'main': [[{'node': 'Gerar Textos IA', 'type': 'main', 'index': 0}]]}

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(w20, f, indent=2, ensure_ascii=False)

print("020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json modificado LOCALMENTE com sucesso!")
