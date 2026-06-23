# Relatório de Teste Real - Facebook (DL Nexus)

O teste de publicação real controlada na página da DL Soluções Condominiais foi executado. O sistema utilizou criptografia SHA-256 (`appsecret_proof`) garantindo compliance com as normas de segurança da Meta (bypassing GraphMethodException Code 100). No entanto, o `META_TOKEN` injetado encontra-se **EXPIRADO**.

## 1. Dados Técnicos da Requisição
- **Endpoint usado:** `POST /100166804716824/feed`
- **Canal Alvo:** Página Facebook (`100166804716824`)
- **DRY_RUN:** desativado (`false`)
- **KILLCRITIC:** Passou limpo. Zero termos proibidos no payload.

## 2. Resultado da Publicação
- **Facebook publicado:** não
- **post_id:** `n/a`
- **URL do post:** n/a
- **Instagram permaneceu bloqueado:** sim (Requisições direcionadas apenas para FB)

## 3. Logs de Ecossistema
- **Supabase atualizado:** não (bloqueado por erro Meta)
- **Telegram enviado:** sim (Aviso Diogo no script de simulação)
- **erros:** `{"facebook": {"message": "Error validating access token: Session has expired...", "type": "OAuthException", "code": 190, "error_subcode": 463}}`

## 4. Diagnóstico
O sistema fez 2 tentativas conforme a regra anti-looping e parou. O erro `OAuthException code 190 / subcode 463` indica que o Token inserido venceu.

**Próximo passo obrigatório:**
Gerar um token de acesso de longa duração (Long-Lived Page Access Token) na plataforma Meta for Developers para que a automação não sofra timeout de sessão e substituir o `META_TOKEN` antigo no `.env`. A malha N8N em si já está devidamente configurada.
