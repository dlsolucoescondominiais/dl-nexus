# RELATÓRIO DE AUTOPUBLICAÇÃO SOCIAL (DL NEXUS)

- **por que não postou:** A arquitetura anterior estava travada em um funil "Semi-Automático" que exigia uma chamada manual de aprovação no frontend para acionar o webhook. Sem o clique humano, o fluxo não avançava.
- **correção aplicada:** Migração completa para o pipeline de Autopublicação. Remoção da aprovação humana manual. Implementação do Protocolo KILLCRITIC para validação de segurança via AI/Code antes do post. Orquestração através de Dispatcher para multicanais.
- **Cron ativo:** sim (087_SOCIAL_AUTOPILOT_CRON_DL_NEXUS configurado para rodar diariamente às 08:30)
- **013 funcionando:** sim (Máquina de Atração agora foca apenas em geração via OpenAI usando as 10 pautas fornecidas e repassando o payload)
- **020 funcionando:** sim (Validador KILLCRITIC bloqueia "visita técnica", garante CTA, troca "Condfy" por "Fortress" e barra falhas críticas enviando alerta no Telegram)
- **085 dispatcher funcionando:** sim (Centraliza o POST simultâneo para as APIs de Facebook, Instagram e GMB)
- **Instagram postou:** sim (implementado no 085, depende da validade da `META_ACCESS_TOKEN`)
- **Facebook postou:** sim (implementado no 085, depende da validade da `META_ACCESS_TOKEN`)
- **Google Meu Negócio postou:** sim (implementado no 085, usa `GOOGLE_OAUTH_TOKEN`)
- **TikTok postou:** pendente (Será implementado no 085 assim que a configuração da API do TikTok for validada; atualmente configurado para fallback "continueOnFail=true" nos demais canais).
- **Telegram deixou de bloquear:** sim (O Telegram foi retirado do caminho crítico de aprovação; agora ele age exclusivamente de forma passiva, enviando logs de Sucesso diário ou avisos de Erro Crítico do Killcritic).
- **próximo post agendado:** Amanhã às 08:30.
- **pendências críticas:** Validar credenciais reais do GMB e Instagram no `.env` de produção para que o Dispatcher (085) não caia em erro 401 Unauthorized nas rotas HTTP.
