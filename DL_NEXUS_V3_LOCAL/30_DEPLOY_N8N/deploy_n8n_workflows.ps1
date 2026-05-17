# Script para rodar no PC local (Windows)

$ProjectPath = "D:\AntiGravity\projeto_01"
$UploadDir = "DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N"

if (Push-Location $ProjectPath -ErrorAction SilentlyContinue) {
    Write-Host "Verificando arquivos prontos para deploy..."
    $Files = Get-ChildItem "$UploadDir\*.json"

    if ($Files.Count -eq 0) {
        Write-Host "Nenhum arquivo JSON em $UploadDir."
        return
    }

    $Files | ForEach-Object { Write-Host $_.Name }

    $confirmation = Read-Host "Deseja enviar estes workflows para a VPS? (s/n)"
    if ($confirmation -eq 's') {
        Write-Host "Enviando via SCP..."
        scp -P 22022 "$UploadDir\*.json" root@129.121.35.90:/tmp/dl_nexus_import/
        Write-Host "Concluído. Para importar, execute via SSH:"
        Write-Host "ssh root@129.121.35.90 -p 22022"
        Write-Host "bash /tmp/deploy_n8n_workflows.sh"
    } else {
        Write-Host "Cancelado."
    }
} else {
    Write-Host "Projeto não encontrado em $ProjectPath"
}
