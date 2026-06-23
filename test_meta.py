import os
import urllib.request
import urllib.parse
import json

msg = '''Um equipamento parado na sua cozinha é prejuízo na certa. Chapas, grills, fritadeiras e sistemas de exaustão precisam de manutenção precisa para manter a sua operação comercial fluindo nos horários de pico.
Com a DL Express, você conta com suporte técnico especializado e ágil para restaurantes, lanchonetes e confeitarias, garantindo que o seu foco continue sendo encantar seus clientes.

Restaurante, lanchonete ou confeitaria: envie DL Express no direct e agende sua Avaliação Técnica!

#DLExpress #ManutencaoComercial #RestaurantesRJ #Lanchonetes #DLSolucoesCondominiais'''

access_token = os.environ.get('META_PAGE_ACCESS_TOKEN_DL')
page_id = '100166804716824'

url = f'https://graph.facebook.com/v25.0/{page_id}/feed'
data = urllib.parse.urlencode({'message': msg, 'access_token': access_token}).encode('utf-8')
req = urllib.request.Request(url, data=data)

try:
    res = urllib.request.urlopen(req)
    print(res.read().decode())
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.reason}")
    print(e.read().decode())
