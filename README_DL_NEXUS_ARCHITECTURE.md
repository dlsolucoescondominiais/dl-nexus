# DL Nexus - Detalhamento da Arquitetura e Fluxos

## Estrutura de Pastas do Projeto

```text
/
├── .env.example                 # Exemplo de variáveis de ambiente
├── README.md                    # Este arquivo
├── AGENTE.md                    # Diretrizes do Cérebro DL Nexus
├── frontend/                    # [Camada 1] Interface de Usuário (React + Vite)
│   ├── render.yaml              # Configuração de Infraestrutura (IaC) para o Render
│   └── src/
│       ├── components/
│       │   ├── LeadCard.tsx     # Componente visual para listagem
│       │   └── ...              # [Incompleto] Outros modais, botões
│       ├── hooks/
│       │   └── useRealtimeMessages.ts # Hook que consome Supabase Realtime para WhatsApp
│       ├── lib/
│       │   └── supabaseClient.ts # Configuração do SDK Supabase com fallbacks mockados
│       └── pages/
│           ├── Dashboard.tsx    # Dashboard do Técnico (Painel Realtime)
│           └── Chat.tsx         # [Vazio] Visão do WhatsApp para o Time Interno
├── backend/
│   ├── n8n/                     # [Camada 2] Orquestrador e Recepção de Webhooks
│   │   ├── docker-compose.yml   # Deploy self-hosted (HostGator VPS)
│   │   ├── Caddyfile            # Reverse Proxy
│   │   └── workflows/           # Onde ficam os JSONs que definem os fluxos do n8n
│   │       ├── 001_webhook_receptor.json # Entrada das mensagens/leads
│   │       └── ...
│   └── supabase/                # [Camada 4] Banco de Dados
│       ├── MIGRATIONS_DL_NEXUS.sql # Schema V3 Principal
│       └── ...                  # [Faltando policies detalhadas, triggers complexos, seed]
└── antigravity/                 # [Camada 3] Cérebro de IA (FastAPI Python)
    ├── main.py                  # [Vazio] Ponto de entrada do FastAPI
    ├── core/
    │   └── llm_router.py        # Estratégia de Fallback Multi-LLM (OpenAI -> Gemini)
    ├── agents/                  # "A Fábrica de Robôs"
    │   ├── aninha.py            # Agente de Triagem
    │   └── diego.py             # [Vazio] Agente Orçamentista
    └── routes/
        └── webhook.py           # [Vazio] Endpoints que recebem chamadas do n8n
```

## Resumo dos Arquivos
- **Prontos:** `.env.example`, `frontend/src/lib/supabaseClient.ts`, `frontend/src/hooks/useRealtimeMessages.ts`, `frontend/src/pages/Dashboard.tsx`, `frontend/src/components/LeadCard.tsx`, `antigravity/core/llm_router.py`, `backend/supabase/MIGRATIONS_DL_NEXUS.sql`, `backend/n8n/workflows/001_webhook_receptor.json` (Parcial)
- **Vazios/Incompletos:** `frontend/src/pages/Chat.tsx`, `antigravity/main.py`, `antigravity/routes/webhook.py`, Arquivos de rotas do React (App.tsx), Configurações do Tailwind, Seed de Testes SQL.

## Diagrama da Arquitetura (4 Camadas)

```text
+-----------------------------------------------------------+
| 1. FRONTEND (Render)                                      |
| nexus.dlsolucoescondominiais.com.br                       |
| (React, Vite, TailwindCSS)                                |
| Dashboard Técnico | Portal do Síndico | CRM               |
+-----------------------------------------------------------+
        ^
        | (Supabase Realtime WebSocket)
        v
+-----------------------------------------------------------+
| 4. DATABASE (Supabase)                                    |
| PostgreSQL + RLS + Triggers + Realtime                    |
| Tabelas: leads, mensagens_whatsapp, avaliacoes_tecnicas   |
+-----------------------------------------------------------+
        ^
        | (Consultas via PostgREST API)
        v
+-----------------------------------------------------------+
| 3. AI BRAIN (HostGator VPS - Python/FastAPI)              |
| antigravity (api.dlsolucoescondominiais.com.br)           |
| Agentes: Aninha (Triagem), Diego (Orçamento)              |
| Multi-LLM Router: OpenAI -> Gemini -> Fallback            |
+-----------------------------------------------------------+
        ^
        | (HTTP POST c/ JWT + Background Tasks)
        v
+-----------------------------------------------------------+
| 2. ORCHESTRATION (HostGator VPS - Docker)                 |
| n8n (n8n.dlsolucoescondominiais.com.br)                   |
| Webhooks Meta, Disparo de Emails, Cron Jobs               |
+-----------------------------------------------------------+
        ^
        | (Webhooks Inbound / Outbound API)
        v
+-----------------------------------------------------------+
| MUNDO EXTERNO                                             |
| WhatsApp (Síndicos) | Site Institucional | HostGator Mail |
+-----------------------------------------------------------+
```

## Fluxo do Lead e do WhatsApp

1. **Recepção:** O Síndico envia mensagem no WhatsApp. A API Oficial do Meta (WhatsApp Business) dispara um webhook que é interceptado pelo **n8n** (Fluxo `001_webhook_receptor`).
2. **Registro Imediato:** O n8n salva a mensagem crua no **Supabase** na tabela `mensagens_whatsapp` para que apareça imediatamente no frontend.
3. **Delegação para IA:** O n8n faz um POST para a API Python **Antigravity** (Fluxo `002_roteador_aninha`). A chamada é feita de forma assíncrona para que o webhook não sofra *timeout*.
4. **Triagem (Aninha):** A API Python ativa a classe da Aninha. Ela lê o contexto, usa o `MultiLLMRouter` para decidir o que responder e se o usuário é um Lead qualificado (Síndico buscando serviços de Infra).
5. **Ação no Banco:** Se for Lead qualificado, Aninha insere ou atualiza um registro na tabela `leads` no Supabase com os campos categorizados (`tipo_servico`, `porte`). Ela também salva sua própria resposta em `mensagens_whatsapp` com `direcao = 'saida'`.
6. **Resposta ao Cliente:** O script Python (Antigravity) engatilha uma chamada de volta (callback) ou responde ao n8n para que este envie a mensagem final via API do WhatsApp de volta ao Síndico.
7. **Atualização do Frontend:** Como o **React** está inscrito via Supabase Realtime (`useRealtimeMessages` e `Dashboard.tsx`), o Card do Lead muda de cor e a mensagem aparece na tela do Técnico sem precisar atualizar a página.
8. **Avaliação Técnica:** O Técnico pega o celular, abre a rota `/checklist/:leadId`, preenche o formulário (Avaliação Técnica de Elétrica/CFTV/Solar) no local do condomínio. Ao salvar, os dados vão para a tabela `avaliacoes_tecnicas`.
9. **Geração de Proposta:** Uma `Background Task` do Python percebe a nova avaliação. O Agente **Diego** lê o Checklist, monta a proposta técnica e financeira usando um template, gera um PDF. O n8n pega o PDF e envia via email Titan HostGator (`orcamento@dlsolucoescondominiais.com.br`).

## Fluxos de Contingência e Multi-LLM

**O que acontece quando...**

*   **A OpenAI cai (GPT-4o fora do ar)?**
    O script em Python `antigravity/core/llm_router.py` usa uma estratégia de `fallback_chain`. A primeira requisição para OpenAI sofre um erro (ex: 502 Bad Gateway ou Timeout de 15s). O bloco `except` captura o erro, faz um log ("Provider openai falhou"), espera 1 segundo (Backoff) e automaticamente faz a requisição para a API do Google (Gemini 1.5 Pro). Para o cliente no WhatsApp e para o dashboard, o sistema funcionou com um atraso mínimo.

*   **A Anthropic/Claude cai?**
    Se configurado na cadeia (`['openai', 'anthropic', 'gemini']`), o sistema pula a Anthropic e vai direto para o Google Gemini. O fluxo é transparente e sequencial até achar um LLM que responda.

*   **Todos os LLMs caem (Cenário Caótico)?**
    O router lança uma exceção `CRITICAL`. O agente Python (Aninha) tem um bloco `try/except` envolta do roteador. Se ela pegar esse erro crítico, ela responde ao usuário uma mensagem *hardcoded* predefinida: *"Peço desculpas, mas nossos sistemas de atendimento estão passando por uma instabilidade momentânea. Por favor, deixe seu nome e a descrição do seu problema, e um técnico humano retornará em breve."*

*   **O Supabase cai (Banco de Dados Offline)?**
    O Frontend perde o Realtime e tenta exibir cache/estado local, mostrando um alerta de desconexão (gerenciado pelo cliente JS).
    O n8n (no Webhook Receptor) não vai conseguir salvar a mensagem na tabela `mensagens_whatsapp`. Para evitar perda de dados, o n8n deve ter um nó de tratamento de erro que salva o payload (o JSON da mensagem do Meta) em um arquivo de texto de contingência no disco do servidor HostGator ou envia um e-mail de emergência para o administrador.

*   **O n8n cai (VPS Offline / Docker crash)?**
    As mensagens do Meta (WhatsApp) ficarão represadas. A Meta possui uma política de *retry* que tenta reenviar webhooks falhos por até 24/48 horas com *backoff* exponencial. Quando o n8n for reiniciado via Docker Compose, a Meta voltará a enviar as mensagens perdidas.
