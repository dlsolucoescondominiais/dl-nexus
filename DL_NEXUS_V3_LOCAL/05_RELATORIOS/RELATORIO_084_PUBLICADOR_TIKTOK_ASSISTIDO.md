# Relatório: 084_PUBLICADOR_TIKTOK_ASSISTIDO

**Nome do Workflow:** 084_PUBLICADOR_TIKTOK_ASSISTIDO
**Objetivo:** Preparar pacotes de roteiro, legenda e hashtags para a rede TikTok, operando em modo "Assistido" (sem automação direta de POST na rede).

**Funcionalidades:**
- Recebe requisições via webhook após aprovação.
- Passa o conteúdo raiz pelo KILLCRITIC.
- Formata a mensagem com ganchos e CTAs adaptados para vídeo vertical.
- Envia o pacote estruturado via Telegram para que o humano (Raphael/Equipe) apenas grave e publique manualmente.

**Segurança:**
- Modo completamente manual/assistido (não há node da API do TikTok).
- Elimina chance de postagem automática sem aprovação de edição de vídeo.
- `active=false` e sem segredos de terceiros.
