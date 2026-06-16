# Script para resolver falhas do MCP - Instalação do Node.js
Write-Host "Iniciando verificação/instalação do Node.js para restaurar servidores MCP..." -ForegroundColor Cyan

# Verifica se o Node já está instalado (pode estar apenas fora do PATH)
$nodePath = Get-Command node -ErrorAction SilentlyContinue
if ($nodePath) {
    Write-Host "O Node.js já foi detectado no sistema: $($nodePath.Source)" -ForegroundColor Yellow
    Write-Host "Porém, o VS Code/Cursor pode estar rodando com variáveis antigas." -ForegroundColor Yellow
    Write-Host "Siga as instruções para reiniciar o seu editor." -ForegroundColor Yellow
    return
}

# Tenta usar o winget
$wingetPath = Get-Command winget -ErrorAction SilentlyContinue
if ($wingetPath) {
    Write-Host "Winget detectado. Instalando a versão LTS do Node.js..." -ForegroundColor Green
    Start-Process winget -ArgumentList "install OpenJS.NodeJS.LTS --silent --accept-source-agreements --accept-package-agreements" -Wait -NoNewWindow
    Write-Host "Instalação via Winget finalizada." -ForegroundColor Green
} else {
    Write-Host "Winget não encontrado. Baixando e instalando o instalador MSI oficial do Node.js..." -ForegroundColor Yellow
    $url = "https://nodejs.org/dist/v20.12.2/node-v20.12.2-x64.msi" # Versão LTS
    $output = "$env:TEMP\nodejs.msi"

    Invoke-WebRequest -Uri $url -OutFile $output
    Write-Host "Download concluído. Iniciando instalação silenciosa..." -ForegroundColor Green

    Start-Process msiexec.exe -ArgumentList "/i `"$output`" /qn /norestart" -Wait -NoNewWindow
    Write-Host "Instalação finalizada." -ForegroundColor Green
}

Write-Host ""
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "                       ATENÇÃO                            " -ForegroundColor Red
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "O Node.js foi instalado com sucesso. No entanto, o PATH do"
Write-Host "seu Windows mudou. O seu editor de código AINDA não sabe disso."
Write-Host ""
Write-Host "AÇÃO OBRIGATÓRIA PARA VOLTAR A USAR OS MCPS:" -ForegroundColor Red
Write-Host "1. Feche COMPLETAMENTE o seu editor (VS Code, Cursor)."
Write-Host "   (Verifique se não ficou nenhum processo rodando em segundo plano)"
Write-Host "2. Reabra o editor."
Write-Host "3. Os servidores MCP vão inicializar corretamente agora."
Write-Host "==========================================================" -ForegroundColor Cyan
