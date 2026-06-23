import urllib.request, json, ssl
ctx=ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
headers = {'X-N8N-API-KEY': open('.env').read().split('N8N_API_KEY=')[1].split('\n')[0].strip(), 'Content-Type': 'application/json'}
base_url = open('.env').read().split('N8N_HOST=')[1].split('\n')[0].strip()
if not base_url.endswith('/'): base_url += '/'

w20 = json.load(open(r'DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json', encoding='utf-8'))

for n in w20.get('nodes', []):
    if n['name'] in ['Facebook Publish', 'Instagram Media Container', 'Instagram Publish Container']:
        n['parameters']['authentication'] = 'predefinedCredentialType'
        n['parameters']['nodeCredentialType'] = 'facebookGraphApi'
        n['credentials'] = {'facebookGraphApi': {'id': 'cqXYWs4nW9rPg4cs', 'name': 'Facebook Graph account'}}
        # remove previous custom header auth
        if 'sendHeaders' in n['parameters']: del n['parameters']['sendHeaders']
        if 'specifyHeaders' in n['parameters']: del n['parameters']['specifyHeaders']
        if 'headerParameters' in n['parameters']: del n['parameters']['headerParameters']

    if n['name'] == 'Gerar Textos IA':
        n['credentials'] = {'openAiApi': {'id': 'qkc9MhPz7FAiygil', 'name': 'OpenAi account 2'}}
    if n['name'] in ['Telegram Entrega', 'Telegram Alerta Bloqueio', 'Telegram Aviso Publicacao', 'Telegram Publish'] or n['type'] == 'n8n-nodes-base.telegram':
        n['credentials'] = {'telegramApi': {'id': 'j1fpzPAZUa1A0i6r', 'name': 'Telegram account 2'}}
    if n['name'] == 'SMTP Relatório Final':
        n['credentials'] = {'smtp': {'id': 'cH1s64M4P6PVE3wU', 'name': 'SMTP - Suporte DL'}}

payload = {'name': w20['name'], 'nodes': w20['nodes'], 'connections': w20.get('connections', {}), 'settings': w20.get('settings', {})}

try:
    req = urllib.request.Request(base_url+'workflows/publicadorSocialDlNexusV320260518', data=json.dumps(payload).encode('utf-8'), headers=headers, method='PUT')
    urllib.request.urlopen(req, context=ctx)
    print('WORKFLOW ATUALIZADO COM CREDENCIAL NATIVA!')
except Exception as e:
    print('PUT ERROR:', e)

try:
    print('DISPARANDO WEBHOOK PARA POSTAR NA HORA...')
    r = urllib.request.urlopen(urllib.request.Request(base_url.replace('/api/v1/', '/webhook/disparo-automatico')), context=ctx)
    print('STATUS DISPARO:', r.status)
except urllib.error.HTTPError as e:
    print('ERRO DISPARO HTTP:', e.code, e.read().decode('utf-8'))
except Exception as e:
    print('ERRO DISPARO:', str(e))
