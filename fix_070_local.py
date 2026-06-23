import json
import urllib.request
import ssl
import os

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""
with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="): n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="): n8n_host = line.split("=", 1)[1].strip()
if not n8n_host.endswith("/"): n8n_host += "/"

headers = {"X-N8N-API-KEY": n8n_api_key, "Accept": "application/json"}
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Baixar 070
req = urllib.request.Request(n8n_host + "workflows/UBH2RWc3CK2AyVR3", headers=headers)
res = urllib.request.urlopen(req, context=ctx).read().decode('utf-8')
w70 = json.loads(res)

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

# Salvar localmente
file_path_70 = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json"
with open(file_path_70, "w", encoding="utf-8") as f:
    json.dump(w70, f, indent=2, ensure_ascii=False)

print("070_CRON_MANUS_DIARIO.json modificado e salvo LOCALMENTE com sucesso!")
