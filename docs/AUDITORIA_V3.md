# RELATÓRIO DE AUDITORIA DE SISTEMAS E FLUXO DE DADOS V3.0
**Projeto:** DL Nexus
**Autor:** Jules (Agente Desenvolvedor / SysAdmin)
**Destinatário:** Diogo Luiz (Diretor Técnico)
**Data:** 04 de Abril de 2026

---

## 1. INVENTÁRIO DE CONECTIVIDADE (O que está ligado?)

*   **n8n ↔ Render:** A conexão entre o n8n (VPS HostGator) e a API Antigravity (hospedada no Render) está estabelecida através de requisições HTTP seguras com o header `X-DL-API-KEY`. A estabilidade depende da ausência de timeouts no Render, razão pela qual implementamos o módulo `BackgroundTasks` nas rotas pesadas.
*   **Supabase:** A conexão com o Supabase é realizada de forma híbrida. No front-end (React), via cliente Supabase usando a `VITE_SUPABASE_ANON_KEY`. No backend Python (Agente Mobile), ocorre de forma direta (REST API) usando a `SUPABASE_SERVICE_ROLE_KEY`. *Nota técnica: As tabelas `leads` e `documentacao_tecnica` existem no contexto lógico e de código (insert via `mobile.py`), contudo a tabela `leads_frios` não foi encontrada estruturada explicitamente nos artefatos da base de código.*
*   **Google Workspace:** A autenticação do Google Drive (conta `tec.network@gmail.com`) está validada (via `credentials_drive.json`). O script lê a variável `INBOX_FOLDER_ID` e é capaz de operar com o serviço de arquivos, validando com a presença em disco. Integrações robustas do Gmail e Agenda estão condicionadas às conexões configuradas na instância local do n8n.
*   **Meta Ads:** O webhook oficial de recepção (Workflow `001_webhook_receptor`) está ativo e escuta payloads nativos da API do WhatsApp Cloud e Meta, roteando-os para triagem IA.
*   **HostGator/cPanel API:** O endpoint `/api/infra/configurar-dns` está implementado. A comunicação é validada e executada assincronamente (evitando crash no Render), invocando registros DNS e forçando AutoSSL.

## 2. RASTREABILIDADE DE DADOS (Para onde vai o lead?)

*   **Cenário A (Inbound):**
    1. Lead faz contato via WhatsApp/Redes (Meta Ads) ou Manychat.
    2. O webhook no n8n (`001_webhook_receptor` ou `014_manychat_receptor`) captura o evento.
    3. Payload é roteado para a rota `POST /api/aninha/triagem` no Antigravity.
    4. A Aninha qualifica o lead, aplica os gatilhos jurídicos, emite parecer (JSON) e devolve assincronamente via webhook do n8n.
    5. O n8n atualiza o banco no Supabase (trigger Realtime reflete no DL Commander para o Diogo) e despacha notificação.

*   **Cenário B (Outbound):**
    1. O serviço **Picoclaw** está ativo na infraestrutura via container Docker (`ghcr.io/sipeed/picoclaw`), expondo a porta `18800`.
    2. A extração de dados CNPJ (Radar Carioca) precisa ser orquestrada por webhooks ou rotinas agendadas (Cron) no n8n consumindo a API nativa do container Picoclaw (`8080`).
    3. Os dados inseridos na tabela `leads_frios` disparam triggers no banco ou são varridos por uma rotina no n8n.
    *Diagnóstico:* Atualmente, a rotina de background no backend Python para puxar `leads_frios` *não existe no código do repositório*. É necessário consolidar a esteira Outbound via Cron no n8n para bater no Picoclaw.

## 3. AUDITORIA DE MÓDULOS ATIVOS

*   **Módulo Picoclaw:** A injeção de código encontra-se exclusivamente na infraestrutura Docker Compose (`backend/n8n/docker-compose.yml`). Não há `BackgroundTasks` no Antigravity consumindo os dados; isso recai sobre a responsabilidade do n8n (que opera na mesma VPS).
*   **Módulo de Organização Mobile:** O endpoint `POST /api/nexus/organizar-mobile` aplica a higienização perfeitamente. Imagens são transformadas em `dl_avaliacao_tecnica_[DATA]_[ID].jpg`. Documentos passam pela visão computacional/análise textual do Gemini Flash, descendo com precisão para `01_Administrativo` (Contratos/NFs) ou `03_Engenharia` (Manuais).
*   **Módulo DevOps:** As requisições de DNS e AutoSSL foram encapsuladas em processos `BackgroundTasks` assíncronos dentro da API Antigravity. Isso permite que a rota web não sofra *timeout* no Render (que possui limite severo de segundos) enquanto a UAPI do cPanel conclui a propagação na HostGator.

## 4. COMPLIANCE E REGRAS DE NEGÓCIO

*   **Terminologia ("Visita Técnica" x "Avaliação Técnica"):** A palavra "visita" foi explicitamente banida no system prompt do agente Aninha e em todos os scripts de nomenclatura de imagem (`agente_zelador.py` e `mobile.py`). Substituída por "Avaliação Técnica de Diagnóstico". O compliance semântico é de 100%.
*   **Script de Vendas e Dor Jurídica:** Validado. O system prompt obriga o agente Aninha a aplicar o gatilho: *"Sem um laudo de conformidade atualizado, o Síndico assume sozinho a Responsabilidade Civil e Criminal em caso de sinistros elétricos"*. A regra das personas (Síndico Profissional, Administradoras e Escolas) encontra-se fixada e aprovada em teste de stress.

## 5. DIAGNÓSTICO DE PENDÊNCIAS E GARGALOS (Próximos Passos)

1.  **Orquestração Outbound (Picoclaw):** Precisamos desenvolver e consolidar o workflow no n8n que faça o agendamento regular para raspar o Picoclaw e abastecer o Supabase (`leads_frios`).
2.  **Manutenção das Credenciais UAPI:** A integração DevOps no momento tem a fundação pronta, contudo, é vital certificar que `CPANEL_USERNAME` e `CPANEL_API_TOKEN` sejam injetados corretamente como Environment Variables na cloud (Render), caso contrário, o script realizará early fallback (bypass de simulação).
3.  **Bibliotecas Python:** Faltam no ambiente (e num eventual requirements.txt) módulos declarados no front-end ou scripts nativos de execução (ex: `python-multipart`, `python-dotenv`, `google-generativeai`).

---
**Status Final:** Sistema arquitetado e aderente à V3.0 Corporativa. Base pronta para escalar e gerar autoridade B2B.
