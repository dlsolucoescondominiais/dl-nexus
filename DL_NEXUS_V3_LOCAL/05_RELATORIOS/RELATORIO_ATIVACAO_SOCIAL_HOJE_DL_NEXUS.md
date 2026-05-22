# Relatório: Ativação Social DL Nexus V3 (Piloto Automático)

**Data de Preparação:** Hoje
**Responsável Técnico:** Jules (Agente) / Raphael (Aprovação Final)

## O que pode ser ativado hoje
1. **084_PUBLICADOR_TIKTOK_ASSISTIDO**: Como não utiliza APIs externas de postagem e opera via Telegram, pode ser ativado e testado sem riscos de credenciais ausentes.
2. **085_SOCIAL_DISPATCHER_DL_NEXUS**: O roteador central pode ser ativado para testes direcionados (ex: apenas para a rota do TikTok).

## Quais IDs faltam (Necessário injetar via N8N no momento da ativação)
- `instagram_account_id` para o Graph API.
- `page_id` da página oficial do Facebook DL Soluções.
- `google_account_id` e `google_location_id` do Google Meu Negócio.

## Quais credenciais faltam (Necessário configurar na VPS N8N)
- Credencial `facebookGraphApi` (Token de Longa Duração do Aplicativo Meta).
- Credencial `googleApi` (OAuth 2.0 para o Google My Business).

## Ordem de Teste (Mock)
1. Ativar 084 (TikTok Assistido).
2. Ativar 085 (Roteador).
3. Enviar requisição POST manual (Postman/Curl) para o 085 simulando um post aprovado voltado para o TikTok.
4. Validar recebimento no Telegram.

## Ordem de Ativação (Produção)
1. Importar todos os JSONs (081 a 085) mantendo `active=false`.
2. Configurar e vincular credenciais (Meta e Google) manualmente na UI do n8n.
3. Obter os IDs faltantes via chamadas `GET` de teste no Graph API e Google API.
4. Atualizar as variáveis de ID nos HTTP requests (ou no Payload gerador do 020).
5. Ativar 081, 082, 083.
6. Testar envio isolado.
7. Conectar a saída humana do 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO ao Webhook do 085.

## Riscos
- **Bloqueio de API:** O envio consecutivo de testes falhos no Meta pode restringir o App.
- Solução: Use o nó do KILLCRITIC para sanitizar e teste com moderação.

## Checklist para Raphael
- [ ] Criar/Validar App no Meta Developers (Escopos: `pages_manage_posts`, `pages_read_engagement`, `instagram_basic`, `instagram_content_publish`).
- [ ] Criar/Validar App no Google Cloud Console (API Perfil da Empresa ativada e OAuth configurado).
- [ ] Logar na VPS e importar os JSONs gerados na pasta `09_PRONTOS_PARA_PRODUCAO`.
- [ ] Criar as credenciais dentro da interface do n8n.
