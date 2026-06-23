"""
[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.
Este script foi desativado.
"""
import sys
sys.exit("Script obsoleto. Manus.IA foi removido.")

import os
import json
import urllib.request
import urllib.error
import ssl

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

def n8n_request(endpoint, method="GET", data=None):
    url = n8n_host + endpoint
    headers = {
        "X-N8N-API-KEY": n8n_api_key,
        "Accept": "application/json"
    }
    if data is not None:
        data = json.dumps(data).encode('utf-8')
        headers["Content-Type"] = "application/json"
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            res_body = response.read().decode('utf-8')
            return json.loads(res_body) if res_body else {}, None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return None, str(e)

w70, err = n8n_request("workflows/UBH2RWc3CK2AyVR3")
if err: print(f"Err 070: {err}")
else:
    for k in ['createdAt','updatedAt','id']: w70.pop(k, None)
    for n in w70['nodes']:
        if n['name'] == 'Preparar Prompt Diário':
            n['parameters']['jsCode'] = 'const date = new Date().toLocaleDateString(\'pt-BR\'); return {json: {prompt: `Você é Manus AI, o Diretor de Marketing B2B da DL Soluções Condominiais.\\nHoje é dia ${date}. Vasculhe e pense em condomínios pequenos/médios, colégios e restaurantes na zona e região do Rio de Janeiro.\\nSua missão: Gerar a estratégia do dia de postagem para o Agente MarkSolar (Copywriter).\\nA estratégia DEVE focar em um ou mais de nossos produtos chave: DL Fortress, DL Guardião e DL Acqua.\\n\\nVocê DEVE retornar sua saída estritamente em um JSON válido com a seguinte estrutura:\\n{\\n  "estrategia_texto": "Descreva o gancho, a dor do público e o tom que o MarkSolar deve usar no post.",\\n  "produto": "Nome do produto foco",\\n  "publico_alvo": "Ex: Síndicos de pequenos condomínios",\\n  "bairro": "Ex: Zona Sul, Barra ou Tijuca",\\n  "canal_destino": "Instagram, Facebook e TikTok",\\n  "objetivo": "Agendar Avaliação Técnica"\\n}`}};'
        if n['name'] == 'HTTP Request Manus API':
            n['parameters']['bodyParameters']['parameters'][1]['value'] = '[{"role": "user", "content": "{{ $json.prompt }}"}]'
            n['parameters']['options'] = {'response': {'response': {'responseFormat': 'json'}}}
        if n['name'] == 'Telegram Entrega':
            n['parameters']['text'] = '🎯 *DIRETRIZ B2B DO MANUS GERADA E ENVIADA AO MARKSOLAR*\\n\\n*Público:* {{ $json.publico_alvo }}\\n*Produto:* {{ $json.produto }}\\n*Região:* {{ $json.bairro }}\\n\\n*Estratégia:* {{ $json.estrategia_texto }}'

    parse_node = {'parameters': {'jsCode': 'let content = $input.all()[0].json.choices[0].message.content; if(content.includes("```json")){content = content.replace(/```json/g, "").replace(/```/g, "").trim();} try{return {json: JSON.parse(content)};}catch(e){return {json: {estrategia_texto: content, produto: "DL Guardião", publico_alvo: "Síndicos", bairro: "Rio de Janeiro"}};} '}, 'id': 'parse_manus_json', 'name': 'Limpar JSON do Manus', 'type': 'n8n-nodes-base.code', 'typeVersion': 2, 'position': [600, 100]}
    call_020 = {'parameters': {'workflowId': 'publicadorSocialDlNexusV320260518', 'mode': 'wait'}, 'id': 'call_020', 'name': 'Chamar MarkSolar (020)', 'type': 'n8n-nodes-base.executeWorkflow', 'typeVersion': 1, 'position': [800, 100]}

    w70['nodes'] = [n for n in w70['nodes'] if n['name'] not in ['Limpar JSON do Manus', 'Chamar MarkSolar (020)']]
    w70['nodes'].extend([parse_node, call_020])
    w70['connections']['HTTP Request Manus API'] = {'main': [[{'node': 'Limpar JSON do Manus', 'type': 'main', 'index': 0}]]}
    w70['connections']['Limpar JSON do Manus'] = {'main': [[{'node': 'Chamar MarkSolar (020)', 'type': 'main', 'index': 0}, {'node': 'Telegram Entrega', 'type': 'main', 'index': 0}]]}

    res, err = n8n_request("workflows/UBH2RWc3CK2AyVR3", method="PUT", data=w70)
    if err: print(f"Erro ao salvar 070: {err}")
    else: print("070 Atualizado com sucesso")


w20, err = n8n_request("workflows/publicadorSocialDlNexusV320260518")
if err: print(f"Err 020: {err}")
else:
    for k in ['createdAt','updatedAt','id']: w20.pop(k, None)
    for n in w20['nodes']:
        if n['name'] == 'Gerar Textos IA':
            n['parameters']['messages']['messageValues'][1]['content'] = '={{ "A Estratégia Ditada pelo Manus AI é:\\n\\n" + JSON.stringify($json) + "\\n\\nCanais Oficiais DL Soluções (use sempre no CTA):\\n- Site: https://dlsolucoescondominiais.com\\n- Instagram: https://www.instagram.com/dl.solucoescondominiais/\\n- WhatsApp da Aninha (CTA Principal): https://wa.me/5521968907139?text=Quero+agendar+uma+Avaliação+Técnica\\n\\nRegras obrigatórias:\\n- O CTA DEVE sempre ser \\"Avaliação Técnica\\" e direcionar pro WhatsApp da Aninha final 39.\\n- NUNCA prometer \\"visita técnica\\".\\n- Alvo: síndicos, colégios e pequenos/médios condomínios do RJ.\\n\\nForneça a resposta em JSON estrito com as chaves: legenda_facebook, legenda_instagram, texto_telegram, hashtags, cta" }}'

    if not any(n['type'] == 'n8n-nodes-base.executeWorkflowTrigger' for n in w20['nodes']):
        w20['nodes'].append({'parameters': {}, 'id': 'execute_workflow_trigger', 'name': 'Execute Workflow Trigger', 'type': 'n8n-nodes-base.executeWorkflowTrigger', 'typeVersion': 1, 'position': [-200, 200]})
        w20['connections']['Execute Workflow Trigger'] = {'main': [[{'node': 'Gerar Textos IA', 'type': 'main', 'index': 0}]]}

    res, err = n8n_request("workflows/publicadorSocialDlNexusV320260518", method="PUT", data=w20)
    if err: print(f"Erro ao salvar 020: {err}")
    else: print("020 Atualizado com sucesso")
