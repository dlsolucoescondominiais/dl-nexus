import urllib.request, json, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
headers = {'X-N8N-API-KEY': open('.env').read().split('N8N_API_KEY=')[1].split('\n')[0].strip(), 'Content-Type': 'application/json', 'Accept': 'application/json'}
base_url = open('.env').read().split('N8N_HOST=')[1].split('\n')[0].strip()
if not base_url.endswith('/'): base_url += '/'

req = urllib.request.Request(base_url+'workflows/publicadorSocialDlNexusV320260518', headers={'X-N8N-API-KEY': headers['X-N8N-API-KEY'], 'Accept': 'application/json'})
w = json.loads(urllib.request.urlopen(req, context=ctx).read().decode('utf-8'))

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

payload = {'name': w['name'], 'nodes': nodes, 'connections': conns, 'settings': w.get('settings', {})}

try:
    req_put = urllib.request.Request(base_url+'workflows/'+w['id'], data=json.dumps(payload).encode('utf-8'), headers=headers, method='PUT')
    urllib.request.urlopen(req_put, context=ctx)
    print("ATIVADO COM SUCESSO!")
except Exception as e:
    print('ERROR:', e)
