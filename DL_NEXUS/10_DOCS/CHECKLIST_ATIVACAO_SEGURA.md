# Checklist de Ativação Segura - DL Nexus MVP Comercial (v8.1-FINAL)

🔒 **APÓS A GERAÇÃO DESTE ECOSSISTEMA, SIGA ESTA ORDEM ESTRITA PARA ATIVAÇÃO:**

1. **Executar Migration SQL:**
   - Acesse o Supabase e execute o arquivo `supabase_schema.sql` (que deve conter as tabelas e as seeds das Feature Flags, todas com `enabled = false`).

2. **Configurar Credenciais n8n:**
   - Para todos os workflows, substitua as strings `"PLACEHOLDER_CREDENTIAL_ID"` pelas credenciais reais previamente cadastradas no n8n.

3. **Importar os Workflows:**
   - Importe os arquivos JSON gerados para a sua instância do n8n (garantindo que `active: false` seja mantido até a homologação individual).

4. **Ativação Incremental (Um por Vez):**
   - **DL_BIZ_LEAD_SCORING** → Realize o teste com 1 lead real.
   - **DL_BIZ_ECONOMY_ENGINE** → Valide os cálculos executando manualmente.
   - **DL_BIZ_QUICK_QUOTE** → Realize um teste supervisionado com o time de vendas.
   - **DL_BIZ_PROPOSAL_ENGINE** → Gere 1 proposta real.
   - **DL_BIZ_FOLLOWUP_ENGINE** → Valide os agendamentos.
   - **DL_BIZ_SINDICO_TRACKER** → Cadastre 3 síndicos reais de teste.
   - **DL_BIZ_REGULATORY_ALERTS** → Insira 1 trigger (evento) de teste e acompanhe.

5. **Liberação das Feature Flags:**
   - Após validar cada workflow com sucesso na etapa anterior, ative a feature flag correspondente executando o seguinte SQL no Supabase:
   ```sql
   UPDATE dl_feature_flags SET enabled = true WHERE flag_name = 'ENABLE_[NOME_DA_FEATURE]';
   ```

*Este checklist garante uma subida para produção totalmente controlada, sem surpresas.*
