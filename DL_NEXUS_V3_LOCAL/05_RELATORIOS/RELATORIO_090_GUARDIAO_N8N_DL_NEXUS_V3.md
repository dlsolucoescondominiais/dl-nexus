# Relatório: 090_GUARDIAO_N8N_DL_NEXUS_V3

**Nome do Workflow:** 090_GUARDIAO_N8N_DL_NEXUS_V3
**Objetivo:** Monitorar o ambiente n8n, verificando healthcheck, listagem de workflows e execuções com erros.
**Funcionalidades:**
- Schedule Trigger a cada 30 minutos.
- HTTP Requests para n8n API (`/healthz`, `/api/v1/workflows`, `/api/v1/executions`).
- Code node para classificar erros conforme a matriz solicitada (CREDENCIAL_AUSENTE, TOKEN_EXPIRADO, etc).
- Telegram para enviar alertas.
- HttpRequest para salvar log no Supabase.
**Segurança e Conformidade:**
- `active = false` definido.
- Não contém segredos.
- Nenhuma correção executada diretamente; apenas alerta.
- `id` raiz configurado corretamente.
