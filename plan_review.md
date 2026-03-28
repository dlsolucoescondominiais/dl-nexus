# Análise do Workflow 013 (Motor de Atração)
Revisando com base no "BIBLIA_ARQUITETURAL_DL_NEXUS.md" e nos requisitos técnicos das APIs.

## Falhas Críticas Identificadas
1. **Violação da Diretriz de Aprovação Humana (Semi-automática):**
   - Na memória: "Social media automation (Workflow 013) employs a semi-automatic strategy where AI generates content, the user manually approves it via the Dashboard, and n8n schedules it to Meta APIs."
   - O fluxo criado dispara direto para as redes sociais (Facebook, Instagram, Google, TikTok) no mesmo instante em que a IA gera o conteúdo. Isso viola a regra de revisão do Síndico/Diogo e corre o risco de postar alucinações da IA.
2. **Ausência de Fallbacks e Tratamento de Erros:**
   - Se a IA falhar ao gerar o post ou a imagem, o fluxo inteiro quebra e as APIs da Meta rejeitarão requisições vazias. Não há nó "If" (Switch/Condicional) validando se `imagem_url` e `post_texto` existem.
3. **TikTok exige Vídeo, Instagram aceita Imagem/Vídeo:**
   - O fluxo envia `imagem_url` pro IG, mas envia `video_url` pro TikTok. Se a IA só gerar uma imagem, o nó do TikTok vai falhar miseravelmente.

## Pontos de Melhoria
1. **Estratégia "Hold & Approve" (Nó Wait ou Webhook no Dashboard):**
   - O fluxo deve ter duas partes. Parte 1: Cron gera o post e SALVA no banco de dados (Supabase `posts_pendentes`). O Dashboard React lê isso. Diogo clica em "Aprovar".
   - Parte 2: O clique no Dashboard dispara um *Webhook* pro n8n, que então faz o *Publish* nas 4 redes.
2. **Google Meu Negócio (GMB) Payload Validation:**
   - A API do GMB é rigorosa. O `callToAction` URL precisa ser validado, e posts locais expiram em 7 dias ou precisam do tipo "OFFER" ou "EVENT" dependendo do CTA.
3. **Tratamento de Rate Limits:**
   - Postar simultaneamente em 4 redes pode esbarrar em limitação de concorrência ou timeout do proxy/Caddy. É prudente adicionar um nó de *Wait/Delay* (3-5 segundos) entre cada postagem.
