<#
.SYNOPSIS
Script automatizado para deploy seguro da esteira social DL Nexus V3 (Workflows 081 a 085).

.DESCRIPTION
Realiza a correção de IDs raiz, garante active=false, envia para a VPS via scp, copia para o container n8n-main, e executa a importação via CLI do n8n na ordem correta, gerando um relatório final e reiniciando o container em caso de sucesso.

.NOTES
Autor: Antigravity (DL Nexus V3)
Data: 22 de Maio de 2026
#>

$ErrorActionPreference = "Stop"

$WorkflowsDir = "..\20_UPLOAD_N8N"
$WorkflowsList = @(
    "084_PUBLICADOR_TIKTOK_ASSISTIDO_config.json",
    "082_PUBLICADOR_FACEBOOK_META_API_config.json",
    "081_PUBLICADOR_INSTAGRAM_META_API_config.json",
    "083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE_config.json",
    "085_SOCIAL_DISPATCHER_DL_NEXUS_config.json"
)

# Configurações SSH e VPS
$VpsUser = "root" # Altere se necessário
$VpsHost = "n8n.dlsolucoescondominiais.com.br"
$RemoteDir = "/root/n8n_deploy_tmp"
$ContainerName = "n8n-main"

Write-Host "Iniciando Deploy Social 08X DL Nexus V3..." -ForegroundColor Cyan

# 1. Corrigir IDs, forçar active=false e gerar *_FIXED.json
Write-Host "1. Processando e validando arquivos JSON..." -ForegroundColor Yellow
$FixedFiles = @()

foreach ($FileName in $WorkflowsList) {
    $FilePath = Join-Path $WorkflowsDir $FileName
    if (-Not (Test-Path $FilePath)) {
        Write-Error "Arquivo não encontrado: $FilePath"
        exit 1
    }

    $JsonContent = Get-Content $FilePath -Raw | ConvertFrom-Json
    
    # Extrair ID do nome do arquivo (ex: "081")
    $WorkflowId = $FileName.Substring(0, 3)
    
    # Corrigir ID raiz
    $JsonContent.id = $WorkflowId
    
    # Forçar active=false
    $JsonContent.active = $false

    $FixedFileName = $FileName.Replace(".json", "_FIXED.json")
    $FixedFilePath = Join-Path $WorkflowsDir $FixedFileName
    
    $JsonContent | ConvertTo-Json -Depth 10 | Set-Content $FixedFilePath -Encoding UTF8
    $FixedFiles += $FixedFileName
    
    Write-Host "   - $FixedFileName gerado com sucesso (ID: $WorkflowId, active: false)." -ForegroundColor Green
}

# 2. Enviar para VPS via SCP
Write-Host "`n2. Transferindo arquivos para VPS via SCP ($VpsHost)..." -ForegroundColor Yellow
# Cria diretório temporário na VPS se não existir
ssh ${VpsUser}@${VpsHost} "mkdir -p $RemoteDir"

foreach ($FixedFileName in $FixedFiles) {
    $LocalFilePath = Join-Path $WorkflowsDir $FixedFileName
    scp $LocalFilePath "${VpsUser}@${VpsHost}:${RemoteDir}/${FixedFileName}"
}
Write-Host "   - Transferência concluída." -ForegroundColor Green

# 3. Copiar para container n8n-main e importar
Write-Host "`n3. Copiando para container $ContainerName e executando importação..." -ForegroundColor Yellow

$ImportSuccess = $true
$ReportContent = "Relatório de Deploy - Social 08X`nData: $(Get-Date)`n`n"

foreach ($FixedFileName in $FixedFiles) {
    Write-Host "   Importando $FixedFileName..."
    
    # Copiar do host da VPS para dentro do container
    ssh ${VpsUser}@${VpsHost} "docker cp ${RemoteDir}/${FixedFileName} ${ContainerName}:/tmp/${FixedFileName}"
    
    # Executar n8n import
    $ImportResult = ssh ${VpsUser}@${VpsHost} "docker exec $ContainerName n8n import:workflow --input=/tmp/${FixedFileName}" 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "     [OK] Sucesso" -ForegroundColor Green
        $ReportContent += "[OK] $FixedFileName importado com sucesso.`n"
    } else {
        Write-Host "     [ERRO] Falha ao importar" -ForegroundColor Red
        $ReportContent += "[ERRO] Falha em $FixedFileName: $ImportResult`n"
        $ImportSuccess = $false
    }
}

# 4. Limpeza VPS
Write-Host "`n4. Limpando arquivos temporários na VPS..." -ForegroundColor Yellow
ssh ${VpsUser}@${VpsHost} "rm -rf $RemoteDir"
ssh ${VpsUser}@${VpsHost} "docker exec $ContainerName sh -c 'rm -f /tmp/*_FIXED.json'"

# 5. Reiniciar container se sucesso total
if ($ImportSuccess) {
    Write-Host "`n5. Todos os workflows importados com sucesso. Reiniciando n8n-main..." -ForegroundColor Yellow
    ssh ${VpsUser}@${VpsHost} "docker restart $ContainerName"
    Write-Host "   - Container reiniciado." -ForegroundColor Green
    $ReportContent += "`nDeploy finalizado com sucesso. Container reiniciado."
} else {
    Write-Host "`n5. Ocorreram erros durante a importação. Container NÃO foi reiniciado." -ForegroundColor Red
    $ReportContent += "`nDeploy finalizado com erros. Container não reiniciado."
}

# 6. Gerar relatório final
$ReportPath = "..\05_RELATORIOS\RELATORIO_DEPLOY_SOCIAL_08X_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
$ReportContent | Set-Content $ReportPath -Encoding UTF8
Write-Host "`nRelatório gerado em: $ReportPath" -ForegroundColor Cyan
Write-Host "Deploy Script Concluído." -ForegroundColor Cyan
