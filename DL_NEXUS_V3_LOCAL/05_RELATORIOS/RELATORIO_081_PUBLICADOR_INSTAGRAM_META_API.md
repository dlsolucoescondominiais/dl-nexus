# Relatório: 081_PUBLICADOR_INSTAGRAM_META_API

**Nome do Workflow:** 081_PUBLICADOR_INSTAGRAM_META_API
**Objetivo:** Publicar no Instagram via Meta Graph API garantindo conformidade e aprovação.

**Funcionalidades:**
- Webhook node no path `/webhook/publicador-instagram`.
- Verifica se a flag `approved=true` está presente, bloqueando envio não autorizado.
- Validação KILLCRITIC, garantindo ausência de termos proibidos (ex: "visita técnica").
- Post via Meta Graph API divido em `Create Media Container` e `Publish Media Container`.
- Usa credential `facebookGraphApi` do n8n.

**Segurança:**
- `active=false`
- Não contém tokens ou senhas hardcoded.
- Sem envio automático de WhatsApp.
- `id` definido na raiz.
