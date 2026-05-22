# Relatório: 082_PUBLICADOR_FACEBOOK_META_API

**Nome do Workflow:** 082_PUBLICADOR_FACEBOOK_META_API
**Objetivo:** Publicar na página do Facebook usando Meta Graph API após aprovação.

**Funcionalidades:**
- Recebe requisições no path `/webhook/publicador-facebook`.
- Valida `approved=true`.
- Valida conteúdo via Node KILLCRITIC para evitar falas proibidas na rede.
- Lida com publicações de foto (`/photos`) se `image_url` estiver presente ou feed normal (`/feed`).
- Autentica via credencial `facebookGraphApi`.

**Segurança:**
- `active=false`.
- Nenhuma chave API hardcoded no fluxo.
- `id` na raiz do JSON para versionamento.
