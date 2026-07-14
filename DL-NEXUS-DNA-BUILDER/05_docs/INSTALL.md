# DNA-Builder Agent - Guia de Instalação

## 1. Configuração do Banco de Dados (Supabase)
1. Acesse o SQL Editor no seu projeto Supabase.
2. Execute o conteúdo do arquivo `04_sql/supabase_schema.sql` para criar as tabelas `dl_nexus_workflows`, `dl_nexus_agent_logs` e `dl_nexus_credentials`.

## 2. Configuração de Credenciais no n8n
Antes de importar os workflows, crie as seguintes credenciais no n8n:
1. **n8nApi**: Credencial do tipo `n8n API` apontando para sua própria instância.
2. **Supabase DB**: Credencial do tipo `Postgres` apontando para o banco Supabase configurado no passo 1.
3. **Telegram Bot**: Credencial do tipo `Telegram API` com o token do bot criado via BotFather.

## 3. Importação dos Workflows
1. No n8n, acesse `Workflows` -> `Add Workflow`.
2. Use a opção `Import from File` ou copie o conteúdo dos JSONs para importar os 4 workflows na seguinte ordem:
   - `DNA_Builder_Self_Healing.json`
   - `DNA_Builder_Health_Check.json`
   - `DNA_Builder_Telegram_Bot.json`
   - `DNA_Builder_Engine.json` (Localizado em `07_shared/builder_engine.json`)

## 4. Configuração Extra
1. Edite os nós `Alert Telegram...` no workflow `DNA_Builder_Self_Healing` e substitua `ADMIN_CHAT_ID_AQUI` pelo ID do chat do administrador no Telegram.

## 5. Ativação
1. Nas configurações (`Settings`) de todos os workflows, certifique-se de que o `Error Workflow` está apontando para o workflow `DNA_Builder_Self_Healing`.
2. Ative o workflow `DNA_Builder_Health_Check`.
3. Ative o workflow `DNA_Builder_Telegram_Bot`.
4. Ative o workflow `DNA_Builder_Engine`.
