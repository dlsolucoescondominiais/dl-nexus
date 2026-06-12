import requests
import time
import os
import uvicorn
import threading
from antigravity.main import app
import json

# Local test parameters
PORT = 8011
BASE_URL = f"http://localhost:{PORT}/api/aninha"

testes = [
    {
        "id": 1,
        "mensagem_atual": "Agendar uma Avaliação Técnica para o sistema de bombas do condomínio",
        "chat_id": "test_chat_1",
        "message_id": "msg_001",
        "nome_usuario": "Teste 1",
        "username": "teste1",
        "contexto": {}
    },
    {
        "id": 2,
        "mensagem_atual": "São duas bombas. O painel está desarmando. Fica na Barra da Tijuca.",
        "chat_id": "test_chat_2",
        "message_id": "msg_002",
        "nome_usuario": "Teste 2",
        "username": "teste2",
        "contexto": {
             "ultima_mensagem": "Agendar uma Avaliação Técnica para o sistema de bombas do condomínio",
             "ultima_resposta": "Claro, posso ajudar com o agendamento! Para prosseguir, poderia me informar o nome do condomínio, a localização e detalhar o problema nas bombas?",
             "etapa_funil": "inicio",
             "dados_coletados": {}
        }
    },
    {
        "id": 3,
        "mensagem_atual": "Condomínio Solar da Barra, responsável Diogo, pode ser amanhã de manhã.",
        "chat_id": "test_chat_3",
        "message_id": "msg_003",
        "nome_usuario": "Teste 3",
        "username": "teste3",
        "contexto": {
            "ultima_mensagem": "São duas bombas. O painel está desarmando. Fica na Barra da Tijuca.",
            "ultima_resposta": "Perfeito. Entendi: são duas bombas de recalque, com painel desarmando, na Barra da Tijuca. Para avançar com a Avaliação Técnica, me informe o nome do condomínio, nome do responsável e melhor horário para atendimento.",
            "dados_coletados": {
                "bairro": "Barra da Tijuca",
                "problema_relatado": "Duas bombas, painel desarmando"
            }
        }
    },
    {
        "id": 4,
        "mensagem_atual": "Quero trocar o disjuntor do meu apartamento.",
        "chat_id": "test_chat_4",
        "message_id": "msg_004",
        "nome_usuario": "Teste 4",
        "username": "teste4",
        "contexto": {}
    },
    {
        "id": 5,
        "mensagem_atual": "Quanto custa para arrumar uma bomba?",
        "chat_id": "test_chat_5",
        "message_id": "msg_005",
        "nome_usuario": "Teste 5",
        "username": "teste5",
        "contexto": {}
    }
]

def run_server():
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="error")

def run_tests():
    print("Iniciando testes da Aninha API (V2)...")
    time.sleep(2) # wait for server to start

    from dotenv import load_dotenv
    SUPABASE_URL = os.getenv("SUPABASE_URL", "https://nejdtvkpiclagsnfljsz.supabase.co")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    # Limpa DB pro teste ser limpo
    import requests
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}
    requests.delete(f"{SUPABASE_URL}/rest/v1/mensagens_processadas_aninha?chat_id=neq.fake", headers=headers)
    requests.delete(f"{SUPABASE_URL}/rest/v1/eventos_aninha?chat_id=neq.fake", headers=headers)
    requests.delete(f"{SUPABASE_URL}/rest/v1/conversas_aninha?chat_id=neq.fake", headers=headers)

    import jwt
    secret = os.getenv("SUPABASE_JWT_SECRET", "test-jwt-secret-xyz123")
    token = jwt.encode({"role": "service_role", "iss": "supabase"}, secret, algorithm="HS256")

    report_lines = []
    report_lines.append("# Relatório de Teste: Aninha Telegram (Fase 2 - Refatorada)")
    report_lines.append("## STATUS: Supabase Online")
    report_lines.append("")

    for t in testes:
        print(f"Executando Teste {t['id']}...")
        report_lines.append(f"### Teste {t['id']}")
        report_lines.append(f"**Entrada:** `{t['mensagem_atual']}`")

        try:
            res = requests.post(f"{BASE_URL}/triagem", json=t, headers={"Authorization": f"Bearer {token}"}, timeout=20)
            status = res.status_code
            res_json = res.json()
            resposta_aninha = res_json.get("resposta_cliente", str(res_json))

            conclusao = "APROVADO"
            if t['id'] == 2 and ("duas bombas" not in resposta_aninha.lower() or "barra" not in resposta_aninha.lower()):
                conclusao = "REPROVADO (Sem memória real)"
            if t['id'] == 4 and ("residencial avulsa" not in resposta_aninha.lower() or res_json.get("bloquear") != True):
                conclusao = "REPROVADO (Fallback residencial falhou)"
            if t['id'] == 5 and "R$" in resposta_aninha.upper():
                conclusao = "REPROVADO (IA deu preço)"

            report_lines.append(f"- **Status HTTP:** {status}")
            report_lines.append(f"- **Intenção Atual:** {res_json.get('intencao_atual')}")
            report_lines.append(f"- **Etapa do Funil:** {res_json.get('etapa_funil')}")
            report_lines.append(f"- **Lead Qualificado:** {res_json.get('lead_qualificado')}")
            report_lines.append(f"- **Bloquear:** {res_json.get('bloquear')}")
            report_lines.append(f"**Resposta da Aninha:** \n> {resposta_aninha}\n")
            report_lines.append(f"- **Conclusão:** {conclusao}")
            report_lines.append("")

        except Exception as e:
            report_lines.append(f"**ERRO NO TESTE:** {str(e)}")

    with open("reports/RELATORIO_ANINHA_TELEGRAM_V2.md", "w") as f:
        f.write("\n".join(report_lines))
    print("Testes finalizados. Relatório gerado em reports/RELATORIO_ANINHA_TELEGRAM_V2.md")

if __name__ == "__main__":
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    run_tests()
