# RELATÓRIO DE PUBLICAÇÃO INSTAGRAM (GRAPH API) - PROVA REAL

- **Data/hora do teste:** 2026-06-23T04:33:13-03:00
- **App usado:** n8n_Integracao_Nexus (ID: 26503104075966862)
- **Instagram Business ID:** 17841403185822108 (dl.solucoescondominiais)
- **Permissões críticas confirmadas:** instagram_content_publish

## FASE 1: Media Container
- **Endpoint usado:** POST /17841403185822108/media
- **Image URL Pública usada:** https://picsum.photos/600/600.jpg
- **Caption:** Teste controlado de publicação via Meta API — DL Soluções Condominiais. Validação técnica do fluxo Instagram/n8n.
- **Creation ID Retornado:** `18470214712106195`

## FASE 2: Media Publish
- **Endpoint usado:** POST /18470214712106195/media_publish
- **Media ID (Post ID) Retornado:** `18322427701277075`
- **Permalink/URL base:** https://www.instagram.com/p/18322427701277075/

## Conclusão
**Instagram API validado.** O fluxo de dupla etapa da Meta operou perfeitamente. Confirmado bloqueio logístico anterior: a publicação só funciona se for providenciada uma URL HTTPS 100% pública.
