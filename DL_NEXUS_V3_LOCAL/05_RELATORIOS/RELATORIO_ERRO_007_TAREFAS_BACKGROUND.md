# Relatório de Erro - 007_tarefas_background

- **causa provável**: O workflow executa de forma repetida devido ao uso de um **Schedule Trigger** configurado para rodar a cada 5 minutos. A falha recorrente nas execuções (85-90) provavelmente é causada por um erro no Supabase, como **credencial ausente/inválida** (credential ID: `QzziIRhKJMDNAE1m`) ou a tabela `tarefas` estar inacessível/inexistente.
- **node com erro**: `Read Tasks` (Node do tipo `n8n-nodes-base.supabase`).
- **risco operacional**: Baixo a Médio. A interrupção deste fluxo afeta o processamento de tarefas em background, mas não deve quebrar os fluxos principais de atendimento (recebimento de mensagens via webhooks).
- **se pode ficar desativado temporariamente**: Sim, pode ser desativado temporariamente na UI do n8n para cessar os erros recorrentes até que o problema de permissão/credencial seja solucionado.
- **dependências**: Tabela `tarefas` no Supabase, credencial `supabaseApi` configurada corretamente no n8n.
- **correção recomendada**: Verificar e reautenticar a credencial do Supabase em produção. Confirmar a existência da tabela `tarefas`. Adicionar tratamento de erro (ex: `continueErrorOutput`) no node caso falhas de rede isoladas aconteçam.
- **se ele deve virar 007_tarefas_fundo_v3**: Sim, idealmente ele deve ser migrado para o padrão arquitetural V3 (ex: `007_tarefas_fundo_v3_killcritic`) durante o processo de modernização.
- **próxima ação segura**: Desativar o workflow temporariamente na interface do n8n em produção para parar o loop de falhas. Em seguida, validar as credenciais e recriar ou ajustar o workflow em staging (V3) antes do novo deploy. Nenhuma alteração foi feita em produção neste momento.
