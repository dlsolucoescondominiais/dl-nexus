# RELATORIO_STATUS_REAL_POSTAGENS_DL

## 1. Workflows Reativados
- `020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO`
- `081_PUBLICADOR_INSTAGRAM_META_API`
- `082_PUBLICADOR_FACEBOOK_META_API`

## 2. Status Real
- **Facebook:** Workflow reativado localmente, mas a publicação real na rede ainda não foi comprovada na prática.
- **Instagram:** Workflow reativado localmente, porém encontra-se pendente de uma `image_url` pública válida (obrigatória para a Meta API do Instagram).
- **Publicação feita:** Não.
- **URL Facebook:** Ausente.
- **URL Instagram:** Ausente.
- **Status Geral:** Pronto para tentativa assistida; nenhuma publicação efetiva realizada ainda.
- **Bloqueios de Workflow:** Sem bloqueio de workflow local, mas com pendências operacionais de publicação real.

## 3. Pendências Reais Antes da Publicação
Para que o status de publicação seja efetivamente "Sim", as seguintes etapas devem ser cumpridas:
1. Acionar o webhook de publicação (entrada do fluxo 020 ou 081/082 diretamente).
2. Fornecer uma `image_url` pública válida e acessível (exigência do Instagram).
3. Confirmar o retorno (Status 200 OK e post_id) da API Meta.
4. Registrar a URL real gerada do post.
5. Registrar o resultado definitivo no banco (Supabase).
6. Enviar alerta final de sucesso ou erro da API no Telegram.
