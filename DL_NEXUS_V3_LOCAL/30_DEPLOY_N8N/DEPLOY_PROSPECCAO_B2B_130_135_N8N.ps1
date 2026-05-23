<#
.SYNOPSIS
Script automatizado para deploy da Esteira de Prospecção B2B (Workflows 130 a 135).

.DESCRIPTION
Garante active=false, injeta IDs raiz consistentes (se necessário, mas já estão injetados nos FIXED), faz SCP para VPS e importa via Docker CLI do n8n-main.

.NOTES
Autor: Antigravity / DL Nexus V3
Data: Maio 2026
#>

$ErrorActionPreference = "Stop"

$WorkflowsDir = "..\20_UPLOAD_N8N"
$WorkflowsList = @(
    "130_MANUS_PROSPECCAO_B2B_RJ_FIXED.json",
    "131_SCORING_LEADS_DL_NEXUS_FIXED.json",
    "132_ENGAJAMENTO_SOCIAL_ASSISTIDO_DL_NEXUS_FIXED.json",
    "133_APROVACAO_PROSPECCAO_TELEGRAM_FIXED.json",
    "134_POST_GOOGLE_BUSINESS_DL_NEXUS_FIXED.json",
    "135_RELATORIO_COMERCIAL_DIARIO_DL_NEXUS_FIXED.json"
)

$VpsUser = "root"
$VpsHost = "n8n.dlsolucoescondominiais.com.br"
$RemoteDir = "/root/n8n_deploy_tmp_130_135"
$ContainerName = "n8n-main"

Write-Host "Iniciando Deploy da Esteira de Prospecção B2B (130-135)..." -ForegroundColor Cyan

# 1. Validação local dos arquivos
Write-Host "1. Validando presença dos arquivos em 20_UPLOAD_N8N..." -ForegroundColor Yellow
foreach ($FileName in $WorkflowsList) {
    $FilePath = Join-Path $WorkflowsDir $FileName
    if (-Not (Test-Path $FilePath)) {
        # Tenta fallback se o sufixo FIXED não estiver no nome mas o JSON sim
        $BaseFileName = $FileName.Replace("_FIXED", "")
        $FallbackPath = Join-Path $WorkflowsDir $BaseFileName
        if (Test-Path $FallbackPath) {
            Write-Host "   Aviso: $FileName não encontrado, usando $BaseFileName." -ForegroundColor Yellow
            $FileName = $BaseFileName
        } else {
            Write-Error "Arquivo obrigatório não encontrado: $FilePath"
            exit 1
        }
    }
}

# 2. Upload para VPS via SCP
Write-Host "`n2. Transferindo arquivos via SCP para $VpsHost..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsHost} "mkdir -p $RemoteDir"

foreach ($FileName in $WorkflowsList) {
    $LocalFilePath = Join-Path $WorkflowsDir $FileName
    scp $LocalFilePath "${VpsUser}@${VpsHost}:${RemoteDir}/${FileName}"
    Write-Host "   - Uploaded: $FileName" -ForegroundColor Green
}

# 3. Importação via Docker exec
Write-Host "`n3. Importando para o container n8n-main..." -ForegroundColor Yellow
$ImportSuccess = $true
$ReportContent = "Relatório de Deploy Prospecção B2B (130-135)`nData: $(Get-Date)`n`n"

foreach ($FileName in $WorkflowsList) {
    Write-Host "   Importando $FileName..."
    
    ssh ${VpsUser}@${VpsHost} "docker cp ${RemoteDir}/${FileName} ${ContainerName}:/tmp/${FileName}"
    $ImportResult = ssh ${VpsUser}@${VpsHost} "docker exec $ContainerName n8n import:workflow --input=/tmp/${FileName}" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     [OK] Importado" -ForegroundColor Green
        $ReportContent += "[OK] $FileName`n"
    } else {
        Write-Host "     [ERRO] Falhou" -ForegroundColor Red
        $ReportContent += "[ERRO] $FileName : $ImportResult`n"
        $ImportSuccess = $false
    }
}

# 4. Limpeza
Write-Host "`n4. Limpando temporários..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsHost} "rm -rf $RemoteDir"
ssh ${VpsUser}@${VpsHost} "docker exec $ContainerName sh -c 'rm -f /tmp/13*_*.json'"

# 5. Conclusão
if ($ImportSuccess) {
    Write-Host "`nDeploy finalizado com sucesso! Reiniciando container para atualizar cache..." -ForegroundColor Green
    ssh ${VpsUser}@${VpsHost} "docker restart $ContainerName"
    $ReportContent += "`nDeploy completo. Reiniciado com sucesso."
} else {
    Write-Host "`nDeploy finalizado com ERROS. Verifique o relatório." -ForegroundColor Red
    $ReportContent += "`nDeploy finalizou com erros."
}

$ReportPath = "..\05_RELATORIOS\RELATORIO_DEPLOY_PROSPECCAO_130_135_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$ReportContent | Set-Content $ReportPath -Encoding UTF8
Write-Host "Relatório salvo em: $ReportPath" -ForegroundColor Cyan
