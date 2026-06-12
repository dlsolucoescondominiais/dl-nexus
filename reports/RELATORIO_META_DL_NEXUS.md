# Relatório Meta DL Nexus

## IDs configurados
- FACEBOOK_PAGE_ID: 100063696635033
- INSTAGRAM_BUSINESS_ACCOUNT_ID: 3136866194

## Tokens encontrados
- META_ACCESS_TOKEN: não
- PAGE_ACCESS_TOKEN: não

## Permissões detectadas
Nenhuma permissão pôde ser detectada porque não existem tokens válidos configurados no ambiente local.

## Validação Facebook Page
- Página acessível: não (Falta Token)
- Nome da página: N/A
- Admin/token válido: não

## Validação Instagram Business
- Conta acessível: não (Falta Token)
- Username: N/A
- Vinculada à página: não testado (Falta Token)

## Riscos
- Token expirado: N/A (Não há token atual configurado).
- Permissão ausente: Faltam todas as permissões (`pages_manage_posts`, `instagram_basic`, `instagram_content_publish`, etc.) devido à falta de um User/Page Access Token.
- App em modo desenvolvimento: Não foi possível checar o Meta App Id.
- Endpoint bloqueado: A API restringe todas as chamadas `GET` aos IDs fornecidos sem um Token válido no header.

## Próxima ação recomendada
Para habilitar a publicação segura no n8n:
1. Acesse o **Meta for Developers** (Graph API Explorer) e gere um Page Access Token válido para a página 100063696635033 com escopos apropriados (ex: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`).
2. Defina este Token como variável de ambiente `META_ACCESS_TOKEN` no `.env` do n8n / VPS.
3. Configure os App Secrets se for usar login nativo do n8n (`META_APP_ID` e `META_APP_SECRET`).
4. Re-execute o teste de leitura na Graph API para confirmar o acesso de leitura, o vínculo e permissão de publicação *antes* de ligar os fluxos definitivos.
