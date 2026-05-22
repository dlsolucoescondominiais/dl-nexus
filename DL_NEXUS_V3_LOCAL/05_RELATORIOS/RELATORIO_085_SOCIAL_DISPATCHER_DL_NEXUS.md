# Relatório: 085_SOCIAL_DISPATCHER_DL_NEXUS

**Nome do Workflow:** 085_SOCIAL_DISPATCHER_DL_NEXUS
**Objetivo:** Agir como o roteador central de publicações pós-aprovação do workflow 020.

**Funcionalidades:**
- Recebe o post final gerado e aprovado.
- Confirmação em redundância (`approved=true`).
- Switch Node para verificar o array de `platforms` (ex: `['INSTAGRAM', 'FACEBOOK']`).
- HTTP Requests isolados para acionar os micro-workflows responsáveis por cada rede (081, 082, 083, 084).

**Segurança:**
- Totalmente desacoplado: impede que o erro de uma API (ex: token do Facebook vencido) pare a publicação no Google Meu Negócio.
- `active=false` e sem IDs hardcoded no fluxo que representem senhas/tokens.
