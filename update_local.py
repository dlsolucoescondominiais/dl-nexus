import json

w = json.load(open(r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json', encoding='utf-8'))

nodes = w.get('nodes', [])
conns = w.get('connections', {})

gmb_node = {
  "parameters": {
    "method": "POST",
    "url": "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-nexus-post-google",
    "sendHeaders": True,
    "headerParameters": { "parameters": [ { "name": "Content-Type", "value": "application/json" } ] },
    "sendBody": True,
    "bodyParameters": { "parameters": [] },
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($node[\"NORMALIZAR_SAIDA_IA_SOCIAL\"].json) }}",
    "options": {}
  },
  "id": "http_gmb_020",
  "name": "HTTP: Google Business Profile",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [ 2400, -300 ]
}

tiktok_node = {
  "parameters": {
    "method": "POST",
    "url": "https://n8n.dlsolucoescondominiais.com.br/webhook/tiktok-assistido-dl-nexus",
    "sendHeaders": True,
    "headerParameters": { "parameters": [ { "name": "Content-Type", "value": "application/json" } ] },
    "sendBody": True,
    "bodyParameters": { "parameters": [] },
    "specifyBody": "json",
    "jsonBody": "={{ JSON.stringify($node[\"NORMALIZAR_SAIDA_IA_SOCIAL\"].json) }}",
    "options": {}
  },
  "id": "http_tiktok_020",
  "name": "HTTP: TikTok Assistido",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.1,
  "position": [ 2600, -300 ]
}

nodes = [n for n in nodes if n['name'] not in ['HTTP: Google Business Profile', 'HTTP: TikTok Assistido']]
nodes.extend([gmb_node, tiktok_node])

if 'Instagram Publish Container' in conns and 'main' in conns['Instagram Publish Container'] and len(conns['Instagram Publish Container']['main']) > 0:
    conns['Instagram Publish Container']['main'][0] = [{"node": "HTTP: Google Business Profile", "type": "main", "index": 0}]

conns['HTTP: Google Business Profile'] = { "main": [ [{"node": "HTTP: TikTok Assistido", "type": "main", "index": 0}] ] }
conns['HTTP: TikTok Assistido'] = { "main": [ [{"node": "Telegram Publish", "type": "main", "index": 0}] ] }

w['nodes'] = nodes
w['connections'] = conns

with open(r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json', 'w', encoding='utf-8') as f:
    json.dump(w, f, indent=2, ensure_ascii=False)

print("ARQUIVO LOCAL ATUALIZADO COM SUCESSO!")
