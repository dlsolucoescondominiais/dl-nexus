<#
.SYNOPSIS
Script para deploy dos workflows de Social Media (140 a 149) no n8n.

.DESCRIPTION
Este script fará o upload dos arquivos JSON localizados na pasta 12_N8N_WORKFLOWS_PROXIMOS
para a API do n8n. Os workflows ficarão com status active=false inicialmente.
#>

$WorkflowsDir = "..\12_N8N_WORKFLOWS_PROXIMOS"
$TargetWorkflows = @(
    "140_ZELADOR_MIDIAS_GOOGLE_DRIVE.json",
    "141_REVISOR_MIDIAS_DL_NEXUS.json",
    "142_CLASSIFICADOR_TEMA_MIDIA.json",
    "143_GERADOR_POST_EDUCATIVO_DL.json",
    "144_REVISOR_IA_DUPLO.json",
    "145_CRIADOR_CARROSSEL_SOCIAL.json",
    "146_PUBLICADOR_MULTICANAL_DL.json",
    "147_SENTINELA_NOTICIAS_VERIFICADAS.json",
    "148_LOG_E_MEMORIA_SOCIAL.json",
    "149_RELATORIO_SOCIAL_DIARIO.json"
)

Write-Host "Iniciando processo de deploy para Social Media Workflows (Fase 1)..." -ForegroundColor Cyan

foreach ($file in $TargetWorkflows) {
    $filePath = Join-Path $WorkflowsDir $file
    if (Test-Path $filePath) {
        Write-Host "Preparando deploy: $file" -ForegroundColor Yellow
        # AQUI VIRÁ A LÓGICA DE CHAMADA DA API DO N8N
        # Invoke-RestMethod -Uri $N8nApiUrl -Method Post -Body $jsonContent -Headers $headers
        Write-Host "Deploy simulado concluído para: $file (active=false)" -ForegroundColor Green
    } else {
        Write-Host "Arquivo não encontrado: $file" -ForegroundColor Red
    }
}

Write-Host "Processo de deploy finalizado." -ForegroundColor Cyan
