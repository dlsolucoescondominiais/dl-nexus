# Análise do Fluxo: 001_webhook_receptor (Enterprise)

## 1. Mapa Lógico de Execução
* **Trigger (Gatilho) [Meta API (Spam Protected)]:** Webhook POST para `/dl-receptor`, protegido por Header Auth e Rate Limit. Recebe payload nativo do WhatsApp/Meta.
* **Nó 1: Triagem [Triagem Avançada (Gemini Flash)]:** Classifica a intenção da mensagem (ex: Emergencia_eletrica, Energia_solar, Sem_perfil).
* **Nó 2: Roteamento [Roteamento Otimizado]:** Switch que divide o fluxo em 3 caminhos: Urgência (Saída 0), Comercial (Saída 1), Padrão/Fallback (Saída 2).
* **Nó 3A: Agente de Urgência [Resposta Técnica (Sonnet)]:** Claude 3.5 Sonnet age como Tecnólogo, acalma o cliente e propõe Avaliação Técnica.
* **Nó 3B: Agente Comercial [Resposta Comercial (GPT-4o)]:** GPT-4o age como Executivo B2B focado em OPEX e contratos.
* **Nós 4: Fallbacks:** Se as IAs principais falharem, o GPT-4o Mini assume como "Assistente Aninha". Se ele também falhar, um texto fixo ("Contingência Final") é enviado.
* **Nó 5: Persistência [Persistência Pipeline]:** Salva todo o log da conversa no banco Supabase (tabela `mensagens_whatsapp`).
* **Nó 6: Fila de Erros:** Captura falhas de banco de dados e salva na tabela `dl_erros_criticos`.

## 2. Configurações Críticas
* Header Auth (Webhook)
* Google Gemini API (models/gemini-2.5-flash)
* Anthropic Claude API (claude-3-5-sonnet-20240620)
* OpenAI API (gpt-4o e gpt-4o-mini)
* Supabase API (PostgreSQL)
