# Plano de Rollback de Emergência N8N V3

Se após o deploy um workflow estiver falhando criticamente ou ocorrer instabilidade no ambiente do `n8n-main`, inicie o processo de rollback imediatamente.

## 1. Identificar o Backup

Localize o backup realizado no checklist de deploy (Passo 4). O arquivo estará em `/tmp/` dentro do servidor ou no contêiner com nomenclatura semelhante a:
`backup_workflows_n8n_20260517.json`

## 2. Restauração Completa

Se desejar restaurar TODOS os workflows para o exato estado do backup, execute no host SSH:

```bash
docker exec -it n8n-main n8n import:workflow --input=/tmp/backup_workflows_n8n_YYYYMMDD.json
docker restart n8n-main
```

## 3. Restauração Específica (Parcial)

O n8n sobrescreve workflows pelo `id`. Se apenas UM workflow quebrou e você tem o arquivo local isolado dele (da versão antiga salva em `.agents/` ou git versioning), transfira-o para o container e importe:

```bash
docker cp fluxo_antigo_salvo.json n8n-main:/tmp/fluxo_antigo.json
docker exec -it n8n-main n8n import:workflow --input=/tmp/fluxo_antigo.json
docker restart n8n-main
```

## 4. Desativar Rapidamente um fluxo na interface

Se o rollback em CLI não for possível rapidamente por falhas de SSH, entre em https://n8n.dlsolucoescondominiais.com.br, localize o workflow causador do problema, desative (switch Inactive) e clique em Stop em execuções pendentes.
