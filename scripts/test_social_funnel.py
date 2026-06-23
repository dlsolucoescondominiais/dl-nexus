import json

print("--- SIMULAÇÃO DE ARQUITETURA DO FUNIL SOCIAL ---")

print("\n1. GERADOR DE CAMPANHA (Auto-Publish Ativo)")
mock_json_gerador = {
  "campanha": "Captação Guarita CFTV 01",
  "linha_servico": "DL Guardião",
  "publicacao": {
    "status": "killcritic_approved",
    "exige_aprovacao_humana": False,
    "permitir_publicacao_automatica": True
  },
  "killcritic": {
    "aprovado": True,
    "riscos": []
  }
}
print(f"Post gerado. Permitir Publicação Automática: {mock_json_gerador['publicacao']['permitir_publicacao_automatica']}")
print("-> Salvo em 'dl_campaigns' com status 'killcritic_approved'. Na fila de auto-publish.")

print("\n2. SOCIAL LISTENER (Recebendo Webhook da Meta)")
webhook_payload = {
  "entry": [
    {
      "messaging": [
        {
          "sender": {"id": "123456789"},
          "message": {"text": "Oi, gostaria de uma Avaliação do CFTV do meu prédio."}
        }
      ]
    }
  ]
}

canal = 'facebook_instagram'
origem = 'direct'
usuario_id = webhook_payload['entry'][0]['messaging'][0]['sender']['id']
mensagem = webhook_payload['entry'][0]['messaging'][0]['message']['text']
keyword = 'AVALIAÇÃO' if 'avaliação' in mensagem.lower() or 'avaliacao' in mensagem.lower() else None

print(f"Origem: {origem}")
print(f"Canal: {canal}")
print(f"Mensagem: {mensagem}")
print(f"Palavra-Chave Detectada: {keyword}")
print("-> Salvo em 'dl_social_events' (Anti-duplicidade ativado)")

print("\n3. LEAD ROUTER E ANINHA ATENDIMENTO (CRM)")
print("Sessão da Aninha verificada em 'dl_aninha_sessions'. Nova Sessão iniciada.")

prompt_aninha = f"Você é a Aninha... O usuário {usuario_id} enviou: '{mensagem}'."
print("Aninha dispara para o LLM...")
print("Resposta Aninha: 'Olá! Sou a Aninha da DL. Qual o nome do seu condomínio, bairro e qual a urgência do CFTV?'")

# Simulating user response parsing
simulacao_lead_qualificado = {
    "nome": "João Síndico",
    "empresa_condominio": "Condomínio das Flores",
    "bairro": "Tijuca",
    "servico": "CFTV",
    "urgencia": "Média"
}

print(f"-> Lead qualificado pelo parser! Inserindo na tabela 'dl_leads'...")
print(json.dumps(simulacao_lead_qualificado, indent=2, ensure_ascii=False))
print("-> Fim do fluxo: Alerta disparado para Diogo no Telegram!")
