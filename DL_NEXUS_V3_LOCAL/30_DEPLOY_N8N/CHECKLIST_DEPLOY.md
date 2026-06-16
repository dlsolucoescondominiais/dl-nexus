# Checklist de Deploy Dinâmico N8N V3

Para garantir total controle e estabilidade do ambiente do N8N na DL Soluções, siga este checklist antes de qualquer alteração nos fluxos de produção.

- [ ] **1. Copiar Arquivos**: Transferir os workflows `.json` revisados que desejam ser atualizados para a pasta `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N`.
- [ ] **2. Validar Estrutura**: Certificar-se de que os arquivos contêm a key "id" no root e "active": false.
- [ ] **3. Executar Validador**: Rodar o `./deploy_n8n_workflows.sh` (ou `.ps1` no Windows) e aguardar o resultado da validação `validar_killcritic_v3.py`.
- [ ] **4. Backup OBRIGATÓRIO**: Conectar via SSH ao servidor e executar o backup da base atual do n8n utilizando o comando sugerido pelo script de deploy. Fazer download ou cópia segura do arquivo `/tmp/backup_workflows_n8n_YYYYMMDD.json`.
- [ ] **5. Importar (Deploy)**: Copiar as linhas geradas `docker exec -it n8n-main n8n import:workflow --input=...` e executá-las no servidor Linux / VPS.
- [ ] **6. Reiniciar Container**: Executar `docker restart n8n-main` para forçar recarregamento das instâncias em memória e caches.
- [ ] **7. Verificação Física**: Acessar https://n8n.dlsolucoescondominiais.com.br e visualizar os workflows, conferir se as tags e websockets conectaram corretamente.
- [ ] **8. Ativação Manual**: Ligar o switch "Active" para true diretamente na UI do n8n se o comportamento estiver 100% testado.
- [ ] **9. Limpeza Local**: Remover os JSONs da pasta `/20_UPLOAD_N8N/` para evitar re-deploys acidentais no futuro.
