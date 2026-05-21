# Relatório Técnico: 090_GUARDIAO_N8N_DL_NEXUS_V3

## 🎯 Objetivo
Agente de verificação operacional que monitora a saúde do n8n, identifica erros de workflows, classifica falhas e envia relatório para Telegram. Este agente atua apenas de forma consultiva e não realiza alterações automáticas em produção.

## 🏗️ Estrutura do Workflow
1. **Verificação Periódica**: Schedule Trigger a cada 30 minutos.
2. **Verificar n8n Online**: HTTP Request para validar a disponibilidade do n8n via `/healthz`.
3. **Listar Workflows n8n**: HTTP Request consumindo a API interna do n8n para listar os workflows.
4. **Buscar Execuções com Falha**: HTTP Request para buscar as últimas execuções que terminaram com status de erro.
5. **CLASSIFICAR_FALHAS_N8N**: Code Node que categoriza o erro em tipos específicos (e.g. CREDENCIAL_AUSENTE, TOKEN_EXPIRADO, WEBHOOK_SEM_RESPOSTA).
6. **GERAR_RELATORIO_TECNICO**: Code Node que consolida as falhas e recomendações, formatando a saída esperada (status_geral, workflows_com_erro, etc).
7. **Tem Falha Crítica?**: IF Node que decide o tipo de notificação (alerta prioritário ou registro).
8. **Alerta Diogo/Raphael**: Envia um resumo da falha via Telegram, informando sempre que aprovação humana é necessária.
9. **Registrar Log Supabase**: Registra o log formatado na tabela `n8n_guardiao_logs`.

## 🌐 Endpoint /healthz
O workflow está configurado para acessar `https://n8n.dlsolucoescondominiais.com.br/healthz`.
**Atenção**: É necessário confirmar se o endpoint `/healthz` está exposto publicamente e ativo na atual configuração do container n8n na VPS. Caso não esteja, o node `Verificar n8n Online` falhará. Como medida de segurança, o node está configurado com `onError: "continueErrorOutput"`, permitindo que o restante da verificação prossiga.

## ✅ Validação de Segurança
- `active=false` garantido no JSON.
- O ID raiz `guardiaoN8nDlNexusV320260518` foi definido corretamente.
- **Zero segredos**: o workflow faz uso da funcionalidade de Credenciais do n8n (`httpHeaderAuth`, `telegramApi`, `supabaseApi`) para abstrair os tokens, não expondo nenhuma key no arquivo JSON.
- **Não altera produção**: o agente apenas realiza requests HTTP com o método GET e consolida resultados.
- **Sem envio ativo de mensagens**: não publica em redes sociais, não envia WhatsApp, enviando apenas notificações internas (Telegram).

## 🛠️ Próximos Passos (Ação Humana)
1. Importar o JSON na interface do n8n (o workflow foi salvo localmente).
2. Configurar e associar as credenciais necessárias na UI do n8n (Header Auth para a API interna do n8n, Token do bot Telegram, API Key do Supabase).
3. Testar a execução e verificar se o endpoint `/healthz` responde adequadamente.
4. Ativar o workflow (`active=true`) apenas via interface do n8n após as devidas validações.
