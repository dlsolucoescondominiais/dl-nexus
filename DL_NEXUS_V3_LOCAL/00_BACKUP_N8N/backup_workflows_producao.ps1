# Script de Backup Automático dos Workflows em Produção (n8n)
# Autor: Antigravity
# Descrição: Exporta os workflows vitais que não estão salvos no repositório local.

$N8N_URL = "https://n8n.dlsolucoescondominiais.com.br/api/v1/workflows"
$N8N_API_KEY = (Get-Content "..\..\.env" | Select-String "N8N_API_KEY" | ForEach-Object { $_.Line.Split("=")[1] })

if ([string]::IsNullOrWhiteSpace($N8N_API_KEY)) {
    Write-Host "Erro: N8N_API_KEY não encontrada no .env" -ForegroundColor Red
    exit
}

$Headers = @{
    "X-N8N-API-KEY" = $N8N_API_KEY
    "Accept" = "application/json"
}

$BackupFolder = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
New-Item -ItemType Directory -Force -Path $BackupFolder | Out-Null

Write-Host "Iniciando backup via API..." -ForegroundColor Cyan

try {
    $Workflows = Invoke-RestMethod -Uri $N8N_URL -Headers $Headers -Method Get
    
    foreach ($wf in $Workflows.data) {
        $Id = $wf.id
        $Name = $wf.name -replace '[\\/:*?"<>|]', '_'
        $IsActive = $wf.active
        
        # Filtra apenas os vitais que queremos garantir backup (ou pega todos)
        Write-Host "Fazendo download do workflow: $Name (ID: $Id) - Ativo: $IsActive"
        
        $WfData = Invoke-RestMethod -Uri "$N8N_URL/$Id" -Headers $Headers -Method Get
        
        $JsonStr = $WfData | ConvertTo-Json -Depth 10
        $FilePath = Join-Path -Path $BackupFolder -ChildPath "$($Id)_$($Name).json"
        
        [System.IO.File]::WriteAllText($FilePath, $JsonStr)
    }
    
    Write-Host "`n✅ Backup concluído com sucesso na pasta: $BackupFolder" -ForegroundColor Green
} catch {
    Write-Host "Erro ao conectar com a API do n8n: $_" -ForegroundColor Red
}
