# Sincronização e Topologia (Supabase ⇄ n8n ⇄ Antigravity)

## 1. Visão Geral da Topologia
O ecossistema DL Nexus opera de forma distribuída, sincronizando estado, regras de negócio e logs entre três pilares fundamentais:
- **Supabase MCP:** Fonte da verdade (Source of Truth). Gerencia banco de dados (PostgreSQL), Feature Flags (`dl_feature_flags`), Execuções (`dl_nexus_execution_state`), Filas (DLQ) e Metrics.
- **n8n Cloud (n8n.dlsolucoescondominiais.com.br):** Orquestrador de workflows e integrações. Responsável por executar os agentes (DL-Jules, DL-Aninha, etc.) baseando-se no estado do Supabase.
- **Antigravity (win10 etc):** Motor FastAPI responsável por roteamento de IA, processamentos complexos em background e chamadas seguras (como o script de integração Stitch).

## 2. Fluxo de Sincronização

### A. Controle de Fluxo (Feature Flags & Estado)
1. **n8n** consulta `Supabase` (tabela `dl_feature_flags`) usando o template de Feature Flag antes de iniciar workflows opcionais.
2. **n8n** verifica cache/MD5 na tabela `dl_nexus_execution_state` no `Supabase` antes de repassar cargas repetitivas.

### B. Logs e Métricas
1. Workflows no **n8n** invocam o subworkflow `DL_GLOBAL_LOGGER`.
2. `DL_GLOBAL_LOGGER` escreve assincronamente as métricas no **Supabase** (`dl_nexus_metrics`).

### C. Antigravity ⇄ n8n
1. **Antigravity** expõe endpoints seguros (ex: porta 8000).
2. O **n8n** dispara Webhooks ou HTTP Requests para o Antigravity quando processamento avançado de IA (ex: RAG denso, geração via Stitch) é necessário.
3. O **Antigravity** processa a tarefa pesada localmente/em infra dedicada e devolve o payload para um webhook de callback do **n8n** ou escreve o resultado final diretamente no **Supabase** (mudando o estado para `completed`).

## 3. Segurança na Sincronização
- Todas as credenciais de sincronização estão armazenadas nativamente nas credenciais do n8n.
- A comunicação com o Antigravity requer validação JWT via Supabase (quando protegido).
- Operações do Antigravity contra o n8nCloud devem sempre validar SSL e obedecer o header de timeout configurado.
