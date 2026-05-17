# Rollback de Deploy do n8n

Para realizar o rollback:
1. Encontre o último backup do dia em `/tmp/` na VPS:
   `ls -la /tmp/backup_workflows_n8n_*`
2. Execute o import do backup antigo:
   `docker exec -i n8n-main n8n import:workflow --input=/tmp/backup_workflows_n8n_YYYYMMDD_HHMMSS.json`
3. Reinicie a instância.
