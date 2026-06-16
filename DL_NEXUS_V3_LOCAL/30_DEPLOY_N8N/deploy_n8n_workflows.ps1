# ==============================================================================
# DEPLOY DINÂMICO N8N - DL NEXUS V3
# Script de validação e simulação de deploy seguro (Sem aplicar direto)
# ==============================================================================

$UploadDir = "..\20_UPLOAD_N8N"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "=========================================="
Write-Host "🚀 INICIANDO PLANO DE DEPLOY N8N V3"
Write-Host "=========================================="

if (-not (Test-Path $UploadDir) -or (Get-ChildItem -Path $UploadDir\*.json -ErrorAction SilentlyContinue).Count -eq 0) {
    Write-Host "⚠️  Nenhum workflow encontrado em $UploadDir"
    Write-Host "Cancelando plano de deploy."
    return 0
}

Write-Host "🔍 Passo 1: Executando Validação KILLCRITIC v3..."
$env:PYTHONPATH = ".."
$process = Start-Process -FilePath python3 -ArgumentList "..\validar_killcritic_v3.py", "$UploadDir" -PassThru -Wait -NoNewWindow

if ($process.ExitCode -ne 0) {
    Write-Host "❌ Falha na validação KILLCRITIC. Deploy abortado."
    return 1
}

Write-Host "✅ Validação KILLCRITIC passou."

Write-Host ""
Write-Host "📦 Passo 2: Gerando comandos para importação manual (SIMULAÇÃO)"
Write-Host "--------------------------------------------------------"
Write-Host "⚠️  ATENÇÃO: Execute os comandos abaixo NO SERVIDOR DE PRODUÇÃO"
Write-Host "Após realizar o backup da base atual."
Write-Host ""
Write-Host "--- COMANDOS DE BACKUP (RECOMENDADO) ---"
$dateStr = Get-Date -Format "yyyyMMdd"
Write-Host "docker exec -it n8n-main n8n export:workflow --all --output=/tmp/backup_workflows_n8n_$dateStr.json"
Write-Host ""
Write-Host "--- COMANDOS DE IMPORTAÇÃO ---"

$files = Get-ChildItem -Path $UploadDir\*.json
foreach ($wf in $files) {
    $filename = $wf.Name
    Write-Host "docker cp $($wf.FullName) n8n-main:/tmp/$filename"
    Write-Host "docker exec -it n8n-main n8n import:workflow --input=/tmp/$filename"
}

Write-Host ""
Write-Host "--- RESTART DO CONTAINER ---"
Write-Host "docker restart n8n-main"
Write-Host "=========================================="
Write-Host "✅ Plano de deploy concluído com sucesso."
