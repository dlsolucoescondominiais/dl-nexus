import urllib.request, json, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
headers = {'X-N8N-API-KEY': open('.env').read().split('N8N_API_KEY=')[1].split('\n')[0].strip(), 'Accept': 'application/json'}
base_url = open('.env').read().split('N8N_HOST=')[1].split('\n')[0].strip()
if not base_url.endswith('/'): base_url += '/'

req = urllib.request.Request(base_url+'credentials', headers=headers)
try:
    res = urllib.request.urlopen(req, context=ctx)
    creds = json.loads(res.read().decode('utf-8'))
    for c in creds.get('data', []):
        print(f"Found Credential: {c['name']} | ID: {c['id']} | Type: {c['type']}")
except Exception as e:
    print('ERROR:', e)
