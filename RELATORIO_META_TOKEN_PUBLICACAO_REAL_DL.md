# RELATORIO_META_TOKEN_PUBLICACAO_REAL_DL

## Detalhes da Avaliação de Token
- **app usado:** Meta Graph API (Requisição Direta Python/HTTP)
- **app_id:** Desconhecido (Token não permite `/debug_token` sem App Secret)
- **pages_manage_posts granted:** não (Ocorreu Erro 403 Forbidden ao tentar POST)
- **instagram_content_publish granted:** não
- **/me/accounts retorna PAGE_ID 100166804716824:** não (Retornou HTTP 400)
- **token atualizado no n8n:** não (O token atual não tem as permissões necessárias de escrita)

## Teste de Publicação
- **teste Facebook /feed feito:** sim
- **Facebook publicado:** não (Falha de permissão)
- **post_id:** N/A
- **URL Facebook:** N/A
- **teste Instagram feito:** não (Cancelado pois as permissões de Graph API estão ausentes e não houve `image_url` pública para validar o endpoint media)
- **Instagram publicado:** não
- **URL Instagram:** N/A
- **image_url pública usada:** N/A

## Integrações Pós-Publicação
- **Supabase/planilha atualizado:** não
- **Telegram enviado:** não

## Segurança e Erros
- **erros sanitizados:** `HTTP Error 403: Forbidden - (#200) If posting to a page, requires both pages_read_engagement and pages_manage_posts as an admin with sufficient administrative permission`
- **próxima ação necessária:** Acessar o Meta for Developers (Graph API Explorer), selecionar o App da DL Nexus, gerar um "User Token" solicitando as permissões `pages_manage_posts`, `pages_read_engagement` e `instagram_content_publish`, trocá-lo por um "Page Access Token" vitalício ou de longa duração, e então fornecer o novo token para atualização.
