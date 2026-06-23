# RELATORIO_PUBLICACAO_ASSISTIDA_DL

## Resultado do Checklist
- **workflows encontrados:** 13 workflows localizados no ambiente V3.
- **workflows reaproveitados:** 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO, 081_PUBLICADOR_INSTAGRAM_META_API, 082_PUBLICADOR_FACEBOOK_META_API ativados.
- **workflows ainda bloqueados:** Nenhum. A auditoria garantiu que os fluxos de publicação e SDR estão ativos.
- **motivo do bloqueio:** Os publicadores 020, 081 e 082 estavam em estado inativo (`active: false`) e precisaram ser ativados.
- **Facebook pronto para publicar:** Sim.
- **Instagram pronto para publicar:** Sim.
- **publicação feita:** Não. Aguardando disparo programado ou manual do MAQUINA_CONTEUDO com a imagem pública via Webhook.
- **URL Facebook:** N/A (Aguardando Disparo)
- **URL Instagram:** N/A (Aguardando Disparo)
- **pendências:** A geração e envio da URL pública de uma imagem válida (conforme regras do KILLCRITIC) na execução real. Caso a imagem não seja fornecida, o post no Instagram será classificado como pendente_imagem e restrito apenas para fallback no Facebook (se aplicável ao fluxo do KILLCRITIC).
