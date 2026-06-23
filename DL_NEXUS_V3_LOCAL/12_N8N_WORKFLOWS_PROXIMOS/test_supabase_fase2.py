import os
import json
import urllib.request
import ssl
from dotenv import load_dotenv

load_dotenv(r'd:\AntiGravity\projeto_01\.env')

supabase_url = os.environ.get('SUPABASE_URL')
anon_key = os.environ.get('SUPABASE_ANON_KEY')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def make_request(method, endpoint, body=None):
    url = f"{supabase_url}/rest/v1/{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header('apikey', anon_key)
    req.add_header('Authorization', f'Bearer {anon_key}')
    if body is not None:
        req.add_header('Content-Type', 'application/json')
        req.add_header('Prefer', 'return=representation')
        data = json.dumps(body).encode('utf-8')
    else:
        data = None
    
    try:
        with urllib.request.urlopen(req, data=data, context=ctx) as res:
            return res.status, json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return 500, str(e)

print("--- Validando Tabelas ---")
tables = ['dl_social_conversas', 'dl_social_mensagens', 'dl_social_leads']
for t in tables:
    status, res = make_request('GET', f"{t}?limit=1")
    if status == 200:
        print(f"[OK] Tabela {t} existe e está acessível via API.")
    else:
        print(f"[ERRO] Tabela {t}: {status} - {res}")

print("\n--- Teste de Gravação (DRY_RUN) ---")
# 1. Criar conversa
conversa_body = {
    "canal_origem": "instagram_direct",
    "sender_id": "fake_test_123",
    "status_conversa": "ativa",
    "etapa_funil": "recepcao",
    "dry_run": True
}
status, res = make_request('POST', 'dl_social_conversas', conversa_body)
print(f"Criar conversa status: {status}")
if status == 201 or status == 200:
    if isinstance(res, list):
        conversa_id = res[0]['id']
    else:
        conversa_id = res['id']
    print(f"Conversa ID criada: {conversa_id}")
    
    # 2. Criar mensagem inbound
    msg_body = {
        "conversa_id": conversa_id,
        "canal_origem": "instagram_direct",
        "message_id": "mid.fake.inbound",
        "direction": "inbound",
        "texto": "Teste de gravação inbound"
    }
    status_msg, res_msg = make_request('POST', 'dl_social_mensagens', msg_body)
    print(f"Criar mensagem status: {status_msg}")

    # 3. Criar lead
    lead_body = {
        "conversa_id": conversa_id,
        "canal_origem": "instagram_direct",
        "sender_id": "fake_test_123",
        "status_lead": "qualificado_cftv",
        "nome_contato": "Sr. Teste",
        "telefone": "21999999999",
        "dry_run": True
    }
    status_lead, res_lead = make_request('POST', 'dl_social_leads', lead_body)
    print(f"Criar lead status: {status_lead}")
    
    # 4. Atualizar status da conversa
    update_body = {
        "etapa_funil": "qualificacao",
        "precisa_humano": True
    }
    status_up, res_up = make_request('PATCH', f'dl_social_conversas?id=eq.{conversa_id}', update_body)
    print(f"Atualizar conversa status: {status_up}")

    # 5. Limpar os dados de teste
    print("\n--- Limpando dados de teste ---")
    status_del_lead, _ = make_request('DELETE', f'dl_social_leads?sender_id=eq.fake_test_123')
    print(f"Deletar lead status: {status_del_lead}")
    
    status_del_msg, _ = make_request('DELETE', f'dl_social_mensagens?conversa_id=eq.{conversa_id}')
    print(f"Deletar mensagens status: {status_del_msg}")
    
    status_del_conv, _ = make_request('DELETE', f'dl_social_conversas?id=eq.{conversa_id}')
    print(f"Deletar conversa status: {status_del_conv}")
else:
    print(f"Falha ao criar conversa: {res}")
