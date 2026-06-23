import urllib.request, json, ssl, time

webhook_url = "https://n8n.dlsolucoescondominiais.com.br/webhook/meta-social-sdr-dl"
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

tests = [
    {
        "name": "Mensagem Facebook Messenger",
        "payload": {
            "object": "page",
            "entry": [{"id": "100063696635033", "messaging": [{"sender": {"id": "controlled_fb_user"}, "message": {"mid": "mid.1", "text": "Quero orçamento para controle de acesso no condomínio."}}]}]
        }
    },
    {
        "name": "Mensagem Instagram Direct",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "controlled_ig_user"}, "message": {"mid": "mid.2", "text": "Preciso de câmeras para meu condomínio."}}]}]
        }
    },
    {
        "name": "Mensagem residencial",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "controlled_ig_user_res"}, "message": {"mid": "mid.3", "text": "Preciso de elétrica na minha casa."}}]}]
        }
    },
    {
        "name": "Mensagem DL Alerta",
        "payload": {
            "object": "page",
            "entry": [{"id": "100063696635033", "messaging": [{"sender": {"id": "controlled_fb_user_alerta"}, "message": {"mid": "mid.4", "text": "Preciso revisar prevenção de incêndio."}}]}]
        }
    },
    {
        "name": "Mensagem restaurante",
        "payload": {
            "object": "instagram",
            "entry": [{"id": "3136866194", "messaging": [{"sender": {"id": "controlled_ig_user_rest"}, "message": {"mid": "mid.5", "text": "Minha chapa Mult•Grill está parando."}}]}]
        }
    }
]

for t in tests:
    print(f"Running {t['name']}")
    req = urllib.request.Request(webhook_url, method='POST')
    req.add_header('Content-Type', 'application/json')
    data = json.dumps(t['payload']).encode('utf-8')
    try:
        with urllib.request.urlopen(req, data=data, context=ctx) as res:
            print("Status:", res.status)
    except Exception as e:
        print("Failed:", e)
    time.sleep(2)
