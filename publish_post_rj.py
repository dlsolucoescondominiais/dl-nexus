import urllib.request, urllib.parse, json
import os

# Buscar o token do .env
token = None
env_path = r'd:\AntiGravity\projeto_01\.env'
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('META_ACCESS_TOKEN='):
            token = line.split('=', 1)[1].strip()
            break

if not token:
    print("Erro: META_ACCESS_TOKEN não encontrado no .env")
    exit(1)

msg = '''Síndico de condomínio de pequeno ou médio porte no Rio de Janeiro, sabemos o quanto a gestão das manutenções pode ser desafiadora e consumir o seu tempo! ⏱️

Problemas com portões falhando, iluminação intermitente ou câmeras inoperantes geram dores de cabeça e insegurança para os moradores.

Com o DL Partner, oferecemos a manutenção continuada preventiva e corretiva que o seu condomínio precisa. Integrando as soluções do DL Volt (elétrica) e DL Guardião (segurança e CFTV), nós garantimos tranquilidade e um SLA ágil para resolver problemas técnicos antes que eles virem prejuízos.

Foque no que realmente importa na sua gestão! 

👉 Envie uma mensagem no Direct ou acesse nosso site para agendar a sua Avaliação Técnica exclusiva para condomínios da capital do RJ! 🏙️🏢

#SindicaturaProfissionalRJ #DLPartner #DLVolt #CondominiosRJ #ManutencaoCondominial #SindicosRJ #DLSolucoesCondominiais'''

page_id = '100166804716824'

url = f'https://graph.facebook.com/v25.0/{page_id}/feed'
data = urllib.parse.urlencode({'message': msg, 'access_token': token}).encode('utf-8')
req = urllib.request.Request(url, data=data)

try:
    res = urllib.request.urlopen(req)
    response_data = json.loads(res.read().decode())
    print("Post publicado com sucesso!")
    print(f"Post ID: {response_data.get('id')}")
    print(f"URL: https://www.facebook.com/{page_id}/posts/{response_data.get('id').split('_')[1]}")
except urllib.error.HTTPError as e:
    print(f'HTTP Error {e.code}: {e.reason}')
    print(e.read().decode())
