# AJUSTE FINAL DE SEGURANÇA OPERACIONAL (DL Nexus v8.1-FINAL)

**Ambiente:** n8n da DL Nexus. Antes de qualquer importação ou alteração real, gerar artefatos em modo seguro, sem ativar workflows automaticamente.

## Regras Absolutas de Segurança Operacional

- Entregar todos os workflows com `active: false`.
- Não ativar automaticamente nenhum workflow.
- Não executar chamadas reais de APIs durante a geração.
- Não assumir que backup, rollback ou credenciais já estão funcionando.
- Usar variáveis e credenciais n8n como placeholders (ex: `PLACEHOLDER_CREDENTIAL_ID`).
- Consultar feature flags na tabela `dl_feature_flags` via Supabase antes de executar funcionalidades opcionais.
