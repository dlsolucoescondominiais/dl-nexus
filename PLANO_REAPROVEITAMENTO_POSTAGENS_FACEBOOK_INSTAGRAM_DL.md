# PLANO_REAPROVEITAMENTO_POSTAGENS_FACEBOOK_INSTAGRAM_DL

## Estratégia de Reaproveitamento
1. **Ativação dos Componentes Base:** Ao invés de criar novos workflows, reativamos o `020_PUBLICADOR_SOCIAL`, `081_PUBLICADOR_INSTAGRAM` e `082_PUBLICADOR_FACEBOOK`.
2. **Integração de Notícias:** Utilização do `147_SENTINELA_NOTICIAS_VERIFICADAS` para injetar contexto real através das rotas de classificação e geração (142 e 143).
3. **Auditoria Dupla:** O post passará pelo `144_REVISOR_IA_DUPLO` e pelo *KILLCRITIC* embutido nos publicadores para barrar falhas comerciais ou promessas irreais.
4. **SDR (Aninha):** Engajamento de direct acoplado ao `050_AGENTE_SDR_SOCIAL_DL` para captura e roteamento.

## Execução
O fluxo de postagem utilizará a esteira de `150_MAQUINA_CONTEUDO_DIARIA_DL`, onde posts gerados serão encaminhados automaticamente para aprovação/disparo.
