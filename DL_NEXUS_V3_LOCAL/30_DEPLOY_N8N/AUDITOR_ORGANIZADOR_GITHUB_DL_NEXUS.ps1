<#
.SYNOPSIS
Script de Auditoria e Organização do GitHub para a DL Nexus V3.

.DESCRIPTION
Este script varre todo o repositório em busca de anomalias (segredos expostos, arquivos muito grandes, duplicados, código de terceiros e scripts soltos). 
Ao final, gera um relatório Markdown detalhado para análise humana.
Não apaga e não move nenhum arquivo (Safe-Mode).

.NOTES
Autor: Antigravity / DL Nexus V3
Data: Maio 2026
#>

$ErrorActionPreference = "Stop"
$RepoRoot = "..\..\" # Sobe da 30_DEPLOY_N8N para a raiz do projeto D:\AntiGravity\projeto_01
$ReportPath = "..\05_RELATORIOS\RELATORIO_AUDITORIA_GITHUB_ORGANIZACAO_DL_NEXUS.md"

Write-Host "Iniciando Auditoria do GitHub DL Nexus V3..." -ForegroundColor Cyan

# Padrões de segredos (expressões regulares simples)
$SecretPatterns = @(
    "(?i)senha\s*[:=]\s*['""][^'""]+['""]",
    "(?i)password\s*[:=]\s*['""][^'""]+['""]",
    "(?i)token\s*[:=]\s*['""][^'""]+['""]",
    "(?i)jwt\s*[:=]\s*['""][^'""]+['""]",
    "(?i)api_key\s*[:=]\s*['""][^'""]+['""]",
    "(?i)secret\s*[:=]\s*['""][^'""]+['""]",
    "(?i)bearer\s+[a-z0-9\-\._~\+\/]+=*",
    "sk-[a-zA-Z0-9]{32,}",
    "AIza[a-zA-Z0-9_-]{35}",
    "eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
)

# Inicializar Markdown
$ReportContent = @"
# Auditoria de Organização GitHub - DL Nexus V3
**Data da Auditoria:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**Diretório Alvo:** $($RepoRoot | Resolve-Path)

> Este relatório foi gerado automaticamente pelo AUDITOR_ORGANIZADOR_GITHUB_DL_NEXUS.ps1. Nenhuma ação destrutiva foi executada.

"@

# 1 e 2. Listar Arquivos Rastreados e Não Rastreados via Git
Write-Host "Executando comandos Git..." -ForegroundColor Yellow
$OriginalLocation = Get-Location
Set-Location $RepoRoot

$TrackedFiles = git ls-files
$UntrackedFiles = git ls-files --others --exclude-standard

$ReportContent += "## 1. Status do Repositório (Git)`n"
$ReportContent += "- **Arquivos rastreados:** $($TrackedFiles.Count)`n"
$ReportContent += "- **Arquivos não rastreados (sujos):** $($UntrackedFiles.Count)`n`n"

# 3. Detectar Arquivos Grandes (> 5MB)
Write-Host "Procurando arquivos grandes..." -ForegroundColor Yellow
$LargeFiles = Get-ChildItem -Path . -Recurse -File -Exclude ".git" | Where-Object { $_.Length -gt 5MB }
$ReportContent += "## 2. Arquivos Grandes (> 5MB)`n"
if ($LargeFiles.Count -gt 0) {
    foreach ($File in $LargeFiles) {
        $ReportContent += "- `$($File.FullName)` ($([math]::Round($File.Length / 1MB, 2)) MB)`n"
    }
} else {
    $ReportContent += "*Nenhum arquivo grande encontrado.*`n"
}

# 4 e 5. Detectar Duplicados (Nomes exatos em pastas diferentes)
Write-Host "Procurando arquivos duplicados..." -ForegroundColor Yellow
$AllFiles = Get-ChildItem -Path . -Recurse -File -Exclude ".git"
$Duplicates = $AllFiles | Group-Object Name | Where-Object { $_.Count -gt 1 }
$ReportContent += "`n## 3. Arquivos Duplicados (Atenção para Workflows)`n"
if ($Duplicates.Count -gt 0) {
    foreach ($Group in $Duplicates) {
        if ($Group.Name.EndsWith(".json") -and $Group.Name -match "^\d{3}_") {
            $ReportContent += "### ⚠️ Workflow Duplicado: $($Group.Name)`n"
            foreach ($File in $Group.Group) {
                $ReportContent += "- `$($File.FullName)``n"
            }
        }
    }
} else {
    $ReportContent += "*Nenhum arquivo duplicado crítico encontrado.*`n"
}

# 6. Detectar JSON sem id raiz
Write-Host "Procurando JSONs de workflow inválidos..." -ForegroundColor Yellow
$JsonFiles = Get-ChildItem -Path . -Recurse -Filter "*.json" -Exclude "package.json","package-lock.json" | Where-Object { $_.FullName -match "N8N_WORKFLOWS" }
$ReportContent += "`n## 4. Auditoria de Workflows JSON`n"
foreach ($Json in $JsonFiles) {
    try {
        $Content = Get-Content $Json.FullName -Raw | ConvertFrom-Json
        if (-not $Content.id) {
            $ReportContent += "- ⚠️ Sem ID raiz: `$($Json.Name)` `n"
        }
    } catch {
        $ReportContent += "- ❌ Erro de Parse JSON: `$($Json.Name)` `n"
    }
}

# 7. Detectar Scripts Soltos na Raiz
Write-Host "Procurando scripts soltos..." -ForegroundColor Yellow
$RootScripts = Get-ChildItem -Path . -File | Where-Object { $_.Extension -match "\.(py|ps1|bat|sh)$" }
$ReportContent += "`n## 5. Scripts Soltos na Raiz`n"
if ($RootScripts.Count -gt 0) {
    foreach ($Script in $RootScripts) {
        $ReportContent += "- `$($Script.Name)` (Sugerido mover para pasta de automação ou deletar)`n"
    }
} else {
    $ReportContent += "*Limpo.*`n"
}

# 8. Detectar Pastas de Terceiros / Cópia Externa
Write-Host "Procurando projetos de terceiros..." -ForegroundColor Yellow
$ForeignDirs = @("backend/picoclaw", "frontend_react_dl") # Exemplos de projetos inteiros injetados
$ReportContent += "`n## 6. Módulos Externos ou Subprojetos Injetados`n"
foreach ($Dir in $ForeignDirs) {
    if (Test-Path $Dir) {
        $ReportContent += "- ⚠️ Encontrado: `$Dir` (Verificar se deveria estar no `.gitignore` ou em submódulo)`n"
    }
}

# 9. Scan de Segredos (Aviso: processo demorado)
Write-Host "Escaneando por segredos em arquivos de texto..." -ForegroundColor Yellow
$ReportContent += "`n## 7. Risco de Segurança (Possíveis Segredos Expostos)`n"
$SafeExtensions = @(".json", ".js", ".ts", ".py", ".md", ".txt", ".ps1", ".env")
$TextFiles = $AllFiles | Where-Object { $SafeExtensions -contains $_.Extension }

$SecretFoundTotal = 0
foreach ($File in $TextFiles) {
    # Evitar o .env real se estiver na raiz, mas para fins de auditoria logamos o perigo se for commitável
    if ($File.FullName -match "node_modules|\.git|venv") { continue }
    
    $FileContent = Get-Content $File.FullName -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($FileContent)) { continue }

    $FileHasSecret = $false
    foreach ($Pattern in $SecretPatterns) {
        if ($FileContent -match $Pattern) {
            if (-not $FileHasSecret) {
                $ReportContent += "### 🔴 Arquivo Suspeito: `$($File.Name)`\n"
                $ReportContent += "Caminho: `$($File.FullName)`\n"
                $FileHasSecret = $true
            }
            $ReportContent += "- Padrão Detectado: `$Pattern`\n"
            $SecretFoundTotal++
        }
    }
}

if ($SecretFoundTotal -eq 0) {
    $ReportContent += "*Nenhum segredo aparente encontrado no código-fonte rastreado.*`n"
}

Set-Location $OriginalLocation

# Salvar relatório
Set-Content -Path $ReportPath -Value $ReportContent -Encoding UTF8
Write-Host "Auditoria concluída! Relatório salvo em: $ReportPath" -ForegroundColor Green
