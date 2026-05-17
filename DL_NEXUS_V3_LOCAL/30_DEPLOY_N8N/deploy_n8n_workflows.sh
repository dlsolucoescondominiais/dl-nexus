#!/bin/bash
# Roda na VPS 129.121.35.90 - porta 22022
set -e

DATE=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="/tmp/backup_workflows_n8n_${DATE}.json"
IMPORT_DIR="/tmp/dl_nexus_import"

echo "1. Criando backup..."
docker exec -i n8n-main n8n export:workflow --all --output="$BACKUP_FILE"
echo "Backup gerado em $BACKUP_FILE"

mkdir -p "$IMPORT_DIR"
echo "2. Conferindo arquivos JSON para importar:"
ls -la "$IMPORT_DIR"/*.json || true

echo "3. Importando os workflows..."
for file in "$IMPORT_DIR"/*.json; do
  if [ -f "$file" ]; then
      echo "Validando $file..."

      # Validar JSON base
      jq empty "$file" || continue

      # Validar chaves criticas: id, name, nodes, connections, active=false
      if ! jq -e 'has("id") and has("name") and has("nodes") and has("connections") and .active == false' "$file" > /dev/null; then
          echo "Erro de estrutura no $file. O workflow precisa ter id, name, nodes, connections e active=false."
          continue
      fi

      filename=$(basename "$file")
      echo "Importando $filename..."
      docker exec -i n8n-main n8n import:workflow --input="/tmp/dl_nexus_import/$filename"
  fi
done

echo "4. Reiniciando o n8n..."
docker restart n8n-main

echo "5. Deploy concluído."
