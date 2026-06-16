#!/bin/bash
# ==============================================================================
# DEPLOY DINÂMICO N8N - DL NEXUS V3
# Script de validação e simulação de deploy seguro (Sem aplicar direto)
# ==============================================================================

UPLOAD_DIR="../20_UPLOAD_N8N"
SCRIPT_DIR=$(dirname "$0")

echo "=========================================="
echo "🚀 INICIANDO PLANO DE DEPLOY N8N V3"
echo "=========================================="

if [ ! -d "$UPLOAD_DIR" ] || [ -z "$(ls -A $UPLOAD_DIR/*.json 2>/dev/null)" ]; then
    echo "⚠️  Nenhum workflow encontrado em $UPLOAD_DIR"
    echo "Cancelando plano de deploy."
    return 0
fi

echo "🔍 Passo 1: Executando Validação KILLCRITIC v3..."
if ! PYTHONPATH=".." python3 ../validar_killcritic_v3.py "$UPLOAD_DIR"; then
    echo "❌ Falha na validação KILLCRITIC. Deploy abortado."
    return 1
fi

echo "✅ Validação KILLCRITIC passou."

echo ""
echo "📦 Passo 2: Gerando comandos para importação manual (SIMULAÇÃO)"
echo "--------------------------------------------------------"
echo "⚠️  ATENÇÃO: Execute os comandos abaixo NO SERVIDOR DE PRODUÇÃO"
echo "Após realizar o backup da base atual."
echo ""
echo "--- COMANDOS DE BACKUP (RECOMENDADO) ---"
echo "docker exec -it n8n-main n8n export:workflow --all --output=/tmp/backup_workflows_n8n_\$(date +%Y%m%d).json"
echo ""
echo "--- COMANDOS DE IMPORTAÇÃO ---"

for wf in "$UPLOAD_DIR"/*.json; do
    if [ -f "$wf" ]; then
        filename=$(basename "$wf")
        echo "docker cp $wf n8n-main:/tmp/$filename"
        echo "docker exec -it n8n-main n8n import:workflow --input=/tmp/$filename"
    fi
done

echo ""
echo "--- RESTART DO CONTAINER ---"
echo "docker restart n8n-main"
echo "=========================================="
echo "✅ Plano de deploy concluído com sucesso."
