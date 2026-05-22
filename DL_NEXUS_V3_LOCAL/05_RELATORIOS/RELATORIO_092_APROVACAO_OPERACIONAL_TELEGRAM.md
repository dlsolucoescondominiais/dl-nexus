# Relatório: 092_APROVACAO_OPERACIONAL_TELEGRAM

**Nome do Workflow:** 092_APROVACAO_OPERACIONAL_TELEGRAM
**Objetivo:** Receber a decisão humana (via Telegram) para ações de médio ou alto risco operacionais e tratar/logar a resposta ou encaminhar para o workflow Executor Seguro (091).
**Funcionalidades:**
- Webhook node no path `/webhook/aprovacao-operacional-dl-nexus`.
- Code node que avalia a matriz de risco (`BAIXO`, `MEDIO`, `ALTO`, `PROIBIDO`) juntamente com a aprovação recebida.
- If node para decidir se chama o webhook do workflow 091.
- Telegram Log e HTTP Request (encaminhamento).
**Segurança e Conformidade:**
- `active = false` definido.
- Não possui segredos hardcoded.
- Implementa restrições diretas onde ações de `ALTO` risco ou `PROIBIDO` são travadas e necessitam intervenção manual explícita (bloqueadas no fluxo do n8n).
- `id` raiz configurado.
