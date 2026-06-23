import urllib.request, urllib.parse, json
import os

env_path = r'd:\AntiGravity\projeto_01\.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('META_ACCESS_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

if not token:
    print("Erro: META_ACCESS_TOKEN não encontrado.")
    exit(1)

# 1. GET /me
url_me = f'https://graph.facebook.com/v25.0/me?fields=id,name&access_token={token}'
req_me = urllib.request.Request(url_me)
try:
    res_me = urllib.request.urlopen(req_me)
    data_me = json.loads(res_me.read().decode())
    print("GET /me ->", data_me)
    if data_me.get('id') != '100166804716824':
        print("FALHA: O token não é um Page Access Token da página correta.")
        exit(1)
except urllib.error.HTTPError as e:
    print('GET /me Error ->', e.code, e.read().decode())
    exit(1)

# 2. POST /feed
msg = "Teste controlado de publicação via Meta API — DL Soluções Condominiais. Publicação técnica para validação do fluxo n8n/Meta. Este post será removido após o teste."
url_feed = f'https://graph.facebook.com/v25.0/100166804716824/feed'
data_feed = urllib.parse.urlencode({'message': msg, 'access_token': token}).encode('utf-8')
req_feed = urllib.request.Request(url_feed, data=data_feed)

try:
    res_feed = urllib.request.urlopen(req_feed)
    data_feed_res = json.loads(res_feed.read().decode())
    print("POST /feed ->", data_feed_res)
except urllib.error.HTTPError as e:
    print('POST /feed Error ->', e.code, e.read().decode())
