import os
import hmac
import hashlib
import urllib.request
import urllib.error
import urllib.parse
import json

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
meta_token = ""
meta_app_secret = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("META_TOKEN="):
            meta_token = line.split("=", 1)[1].strip().strip('"').strip("'")
        elif line.startswith("META_APP_SECRET="):
            meta_app_secret = line.split("=", 1)[1].strip().strip('"').strip("'")

if not meta_token or not meta_app_secret:
    print("ERRO: META_TOKEN ou META_APP_SECRET não encontrados.")
    exit(1)

# Gerar appsecret_proof
appsecret_proof = hmac.new(
    meta_app_secret.encode('utf-8'),
    msg=meta_token.encode('utf-8'),
    digestmod=hashlib.sha256
).hexdigest()

FACEBOOK_PAGE_ID = "100166804716824"
INSTAGRAM_BUSINESS_ACCOUNT_ID = "17841403185822108"

print("========================================")
print("TESTE DE ESCRITA - FACEBOOK PAGE")
print("========================================")

fb_text = "Teste técnico de integração DL Nexus. Publicação de validação automática."
fb_url = f"https://graph.facebook.com/v20.0/{FACEBOOK_PAGE_ID}/feed"

fb_data = urllib.parse.urlencode({
    "message": fb_text,
    "access_token": meta_token,
    "appsecret_proof": appsecret_proof
}).encode('utf-8')

req = urllib.request.Request(fb_url, data=fb_data, method='POST')

try:
    response = urllib.request.urlopen(req)
    res_body = response.read().decode('utf-8')
    status = response.getcode()
    print(f"Status HTTP: {status}")
    print(f"Response: {res_body}")
    data = json.loads(res_body)
    print(f"page_post_id: {data.get('id')}")
    print(f"post_url: https://facebook.com/{data.get('id')}")
except urllib.error.URLError as e:
    print(f"ERRO: {e.reason}")
    if hasattr(e, 'read'):
        print(f"Details: {e.read().decode('utf-8')}")

print("\n========================================")
print("TESTE DE ESCRITA - INSTAGRAM BUSINESS")
print("========================================")

ig_media_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
image_url = "https://upload.wikimedia.org/wikipedia/commons/e/e1/FullMoon2010.jpg" # Usando o logo como teste

ig_data = urllib.parse.urlencode({
    "image_url": image_url,
    "caption": "Teste técnico de integração DL Nexus. Container de mídia.",
    "access_token": meta_token,
    "appsecret_proof": appsecret_proof
}).encode('utf-8')

req_ig = urllib.request.Request(ig_media_url, data=ig_data, method='POST')

container_id = None
try:
    res_ig = urllib.request.urlopen(req_ig)
    body_ig = res_ig.read().decode('utf-8')
    status = res_ig.getcode()
    print(f"Status HTTP (Container): {status}")
    print(f"Response: {body_ig}")
    data_ig = json.loads(body_ig)
    container_id = data_ig.get('id')
    print(f"container_id: {container_id}")
except urllib.error.URLError as e:
    print(f"ERRO: {e.reason}")
    if hasattr(e, 'read'):
        print(f"Details: {e.read().decode('utf-8')}")

if container_id:
    print("\nPublicando Container...")
    publish_url = f"https://graph.facebook.com/v20.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    pub_data = urllib.parse.urlencode({
        "creation_id": container_id,
        "access_token": meta_token,
        "appsecret_proof": appsecret_proof
    }).encode('utf-8')
    req_pub = urllib.request.Request(publish_url, data=pub_data, method='POST')
    try:
        res_pub = urllib.request.urlopen(req_pub)
        body_pub = res_pub.read().decode('utf-8')
        print(f"Status HTTP (Publish): {res_pub.getcode()}")
        print(f"Response: {body_pub}")
        data_pub = json.loads(body_pub)
        print(f"media_id: {data_pub.get('id')}")
    except urllib.error.URLError as e:
        print(f"ERRO Publish: {e.reason}")
        if hasattr(e, 'read'):
            print(f"Details: {e.read().decode('utf-8')}")
