import urllib.request, urllib.parse, json
import os

env_path = r'd:\AntiGravity\projeto_01\.env'
token = None
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('META_ACCESS_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

# SIMULACAO N8N FACEBOOK
print("--- TESTE N8N 082 (Simulado Local) ---")
msg_n8n = "Teste controlado via n8n cloud — DL Soluções Condominiais. Validação técnica do publicador 082."
url_fb = f'https://graph.facebook.com/v25.0/100166804716824/feed'
data_fb = urllib.parse.urlencode({'message': msg_n8n, 'access_token': token}).encode('utf-8')
req_fb = urllib.request.Request(url_fb, data=data_fb)

fb_post_id = None
try:
    res_fb = urllib.request.urlopen(req_fb)
    data_res_fb = json.loads(res_fb.read().decode())
    fb_post_id = data_res_fb.get('id')
    print("N8N FB POST ->", data_res_fb)
except urllib.error.HTTPError as e:
    print('N8N FB POST Error ->', e.code, e.read().decode())

# INSTAGRAM FASE 1: MEDIA CONTAINER
print("\n--- TESTE INSTAGRAM ---")
ig_id = '17841403185822108'
image_url = 'https://picsum.photos/600/600.jpg'
caption = "Teste controlado de publicação via Meta API — DL Soluções Condominiais. Validação técnica do fluxo Instagram/n8n."

url_media = f'https://graph.facebook.com/v25.0/{ig_id}/media'
data_media = urllib.parse.urlencode({'image_url': image_url, 'caption': caption, 'access_token': token}).encode('utf-8')
req_media = urllib.request.Request(url_media, data=data_media)

creation_id = None
try:
    res_media = urllib.request.urlopen(req_media)
    data_res_media = json.loads(res_media.read().decode())
    creation_id = data_res_media.get('id')
    print("INSTAGRAM MEDIA CREATION ->", data_res_media)
except urllib.error.HTTPError as e:
    print('INSTAGRAM MEDIA Error ->', e.code, e.read().decode())

# INSTAGRAM FASE 2: PUBLISH MEDIA
if creation_id:
    url_publish = f'https://graph.facebook.com/v25.0/{ig_id}/media_publish'
    data_publish = urllib.parse.urlencode({'creation_id': creation_id, 'access_token': token}).encode('utf-8')
    req_publish = urllib.request.Request(url_publish, data=data_publish)
    
    try:
        res_publish = urllib.request.urlopen(req_publish)
        data_res_publish = json.loads(res_publish.read().decode())
        print("INSTAGRAM PUBLISH ->", data_res_publish)
    except urllib.error.HTTPError as e:
        print('INSTAGRAM PUBLISH Error ->', e.code, e.read().decode())

