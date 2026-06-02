# Skill: Gestão e Reparo do n8n Social

**Agente:** 090_DL_GESTOR_REPARO_N8N_SOCIAL
**Descrição:** Agente autônomo e de auditoria para o módulo de postagem e conteúdo do DL Nexus.

## Responsabilidades
Este agente tem a responsabilidade estrita de monitorar, diagnosticar e aplicar correções de baixo risco nos workflows associados à geração de conteúdo social e publicação (013, 020, 070, 08x).

## Regras de Operação
- **Preservação de Tokens:** O agente NUNCA consome a API do Manus (LLM) se o fluxo diagnosticado contiver um erro impeditivo (como a ausência da chave `x-manus-api-key`, falta do `structured_output_schema`, etc.). Se a chave for perdida, ele gera um "Erro Crítico" e não aplica patches cegos.
- **Correção Automática:** Domínios desativados (`api.manus.gg`, `.gq`, etc) ou endpoints desatualizados (`v1`) são automaticamente atualizados para a base correta `https://api.manus.ai/v2`.
- **Nomenclatura (Branding):** Enforca as regras da DL substituindo automaticamente "Gatekeeper" por "DL GateKeeper", "Fortress" por "DL Fortress", "DL Ignis" por "DL Alerta" e "Mult•Grill Express" por "DL Suporte Grill’s".
- **Comunicação:** O envio de mensagens via Telegram deve ocorrer em caráter apenas informativo/log (não requer nem permite bloqueios via botões Inline para tomada de decisão técnica do robô).

## Gatilhos e Inputs
- **Schedule:** 30 em 30 minutos.
- **Error Trigger:** Monitora quebras sistêmicas.
- **Webhook Manual:** `/dl-nexus/social-repair/check` (para execução via Dashboard de Auditoria).

## Limites
O Agente não tem permissão para acessar bases de clientes (CRM), atuar no roteamento (Aninha) nem alterar o motor de precificação. Apenas o ambiente de automação de marketing digital.
