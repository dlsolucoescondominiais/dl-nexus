import os
import urllib.request, json, ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
key=os.environ.get('N8N_API_KEY')
req=urllib.request.Request('https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows', headers={'X-N8N-API-KEY':key})
res=urllib.request.urlopen(req, context=ctx)
data=json.loads(res.read())['data']
for w in data:
  req2 = urllib.request.Request(f'https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows/{w["id"]}', headers={'X-N8N-API-KEY':key})
  w_full=json.loads(urllib.request.urlopen(req2, context=ctx).read())
  for n in w_full.get('nodes',[]):
    if n['type']=='n8n-nodes-base.webhook' and n.get('parameters',{}).get('path') in ['dl-aninha', 'dl-aninha-atendimento'] and w_full.get('active'):
      print('CONFLITO ATIVO:', w['name'], w['id'], 'Path:', n.get('parameters',{}).get('path'))
