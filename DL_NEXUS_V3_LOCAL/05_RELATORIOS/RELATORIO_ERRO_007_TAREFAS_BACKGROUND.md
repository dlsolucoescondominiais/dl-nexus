# Relatório de Erro - Workflow 007_tarefas_background

- **Causa provável**: O node "Read Tasks" está falhando ao tentar ler a tabela "tarefas" no Supabase. O erro é desencadeado repetidamente porque o workflow é acionado por um Schedule (Cron) configurado para rodar a cada 5 minutos.
- **Node com erro**: "Read Tasks" (tipo: n8n-nodes-base.supabase). Este é o provável ponto de falha reportando os erros vistos (Exec IDs ~85 a 90), possivelmente devido a credencial ausente/inválida, tabela inexistente ou problemas de permissão.
- **Risco operacional**: Alto (em nível de logs/API). Devido à execução repetitiva a cada 5 minutos através do Schedule Trigger, o erro constante corre o risco de floodar os logs do sistema e possivelmente exaurir a cota da API ou os limites de processamento do n8n se não tratado.
- **Se pode ficar desativado temporariamente**: Sim. A trigger pode (e deve) ser pausada temporariamente para cessar as execuções e evitar logs/consumo desnecessário enquanto o erro de conexão/dados for investigado.
- **Dependências**:
  - Gatilho: Node "Schedule" (n8n-nodes-base.scheduleTrigger).
  - Ação: Supabase API conectando à tabela "tarefas".
- **Correção recomendada**:
  - Validar e atualizar as credenciais do Supabase no ambiente de produção.
  - Verificar se a tabela "tarefas" existe e tem as devidas permissões RLS.
  - Implementar o padrão de arquitetura n8n configurando `onError` para `continueErrorOutput` no node do Supabase para evitar falhas silenciosas ou paradas abruptas e, então, adicionar uma rota de tratamento de erro (ex: notificação via Telegram/Slack ou registro de log secundário).
- **Se ele deve virar 007_tarefas_fundo_v3**: Sim. Para adequar à arquitetura V3, o workflow deve ser copiado e recriado como, por exemplo, `007_tarefas_background_v3_killcritic` (ou `_fundo_v3`), incorporando o tratamento de erros exigido e sendo movido para a pasta correta, sem que o JSON de produção seja deletado.
- **Próxima ação segura**: Desativar a chave do Schedule via interface do n8n em produção. Em seguida, duplicar o workflow atual para a estrutura V3 local e aplicar o tratamento de erros, solicitando aprovação para o novo deploy. Não apagar ou alterar o JSON do workflow original `007_tarefas_background.json`.
