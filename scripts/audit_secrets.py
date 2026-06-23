import os
import re
import subprocess
from datetime import datetime

# Termos a auditar
SUSPICIOUS_TERMS = [
    r"access_token", r"refresh_token", r"client_secret", r"client_id", 
    r"service_role", r"SUPABASE_SERVICE_ROLE_KEY", r"META_PAGE_ACCESS_TOKEN_DL", 
    r"META_ACCESS_TOKEN", r"META_TOKEN", r"OPENAI_API_KEY", r"GEMINI_API_KEY", 
    r"DEEPSEEK_API_KEY", r"GOOGLE_APPLICATION_CREDENTIALS", r"TELEGRAM_BOT_TOKEN", 
    r"MANUS_API_KEY", r"password", r"senha", r"Bearer", r"Authorization"
]

# Regex para detectar valores literais de segredos expostos (ex: apiKey = "AIzaSy..." ou token: 'EAF4...')
# Procura atribuição de strings de comprimento mínimo 10 que não sejam referências a process.env ou variáveis.
SECRET_ASSIGNMENT_REGEX = re.compile(
    r'(?:' + '|'.join(SUSPICIOUS_TERMS) + r')\s*(?:[:=]|\bhas\b)\s*[\'"`]([a-zA-Z0-9_\-\.\#\@\$\%\^\&\*\!\?\=\+\/]{8,})[\'"`]',
    re.IGNORECASE
)

# Termos adicionais: cadeias de caracteres muito longas que parecem tokens (ex: EAF4..., eyJhbGci...)
TOKEN_LIKE_REGEX = re.compile(
    r'\b(EAF4[a-zA-Z0-9]{30,}|eyJ[a-zA-Z0-9_\-]{10,}\.eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{20,}|sbp_[a-zA-Z0-9]{30,}|sk-svcacct-[a-zA-Z0-9_\-]{30,}|AIzaSy[a-zA-Z0-9_\-]{30,}|sk-proj-[a-zA-Z0-9_\-]{30,})\b'
)

def get_git_files():
    # Obtém arquivos modificados e não rastreados que estão na lista de commit candidatos
    try:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        files = []
        ignored_extensions = {
            ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".zip", ".pdf", 
            ".mp4", ".mp3", ".woff", ".woff2", ".ttf", ".eot", ".map", ".tar.gz", ".tgz"
        }
        ignored_filenames = {"package-lock.json", "pnpm-lock.yaml", "yarn.lock"}
        
        for line in res.stdout.splitlines():
            if not line.strip():
                continue
            # O status do git status --porcelain tem 2 caracteres, depois o arquivo
            status = line[:2].strip()
            filepath = line[2:].strip().strip('"')
            
            # Ignorar deletados
            if "D" in status:
                continue
                
            # Filtros de exclusão
            basename = os.path.basename(filepath)
            _, ext = os.path.splitext(filepath.lower())
            
            if filepath == "scripts/audit_secrets.py" or filepath == "scripts/sanitize_all.py" or filepath == "scripts/sanitize_regex.py" or filepath == ".gitignore" or "RELATORIO_AUDITORIA_" in filepath:
                continue
            if ext in ignored_extensions or basename in ignored_filenames:
                continue
            if "node_modules" in filepath or ".next" in filepath or "dist/" in filepath or "build/" in filepath or "backend/picoclaw/" in filepath:
                continue
            if "backup-" in filepath or ".git/" in filepath:
                continue
                
            files.append((status or "?", filepath))
        return files
    except Exception as e:
        print(f"Erro ao obter arquivos do git: {e}")
        return []

def audit_file(filepath):
    findings = []
    if not os.path.exists(filepath):
        return findings
    
    # Pular diretórios
    if os.path.isdir(filepath):
        return findings
        
    try:
        # Pular arquivos maiores que 500 KB para evitar lentidão
        file_size = os.path.getsize(filepath)
        if file_size > 500 * 1024:
            # Apenas logs ou JSONs de workflow podem ser grandes, mas vamos pular no commit
            print(f"[Aviso] Pulando arquivo grande (>500KB): {filepath} ({file_size} bytes)")
            return findings

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        for line_num, line in enumerate(lines, 1):
            # 1. Checar por atribuições de valores literais suspeitos
            for match in SECRET_ASSIGNMENT_REGEX.finditer(line):
                secret_val = match.group(1)
                # Ignorar placeholders óbvios ou valores inofensivos
                if secret_val.lower() in ["true", "false", "null", "undefined", "senha", "password", "none", "presente", "mascarado"]:
                    continue
                # Se for atribuição de string curta e comum
                if len(secret_val) < 8:
                    continue
                findings.append((line_num, line.strip(), secret_val, "Atribuição de literal suspeita"))
            
            # 2. Checar por cadeias longas parecidas com tokens de API
            for match in TOKEN_LIKE_REGEX.finditer(line):
                token_val = match.group(1)
                findings.append((line_num, line.strip(), token_val, "Padrão de Token detectado"))
                
    except Exception as e:
        print(f"Erro ao ler arquivo {filepath}: {e}")
        
    return findings

def main():
    print("Iniciando auditoria de segredos pré-commit...")
    files = get_git_files()
    
    all_findings = {}
    added_files = []
    modified_files = []
    
    for status, filepath in files:
        if "A" in status or "?" in status:
            added_files.append(filepath)
        else:
            modified_files.append(filepath)
            
        findings = audit_file(filepath)
        if findings:
            all_findings[filepath] = findings

    # Obter git diff resumido
    git_diff_summary = ""
    try:
        res_diff = subprocess.run(["git", "diff", "--stat"], capture_output=True, text=True)
        git_diff_summary = res_diff.stdout
    except Exception:
        git_diff_summary = "Não foi possível obter o git diff."

    # Gerar Relatório MD
    report_lines = []
    report_lines.append("# RELATÓRIO DE AUDITORIA PRÉ-COMMIT — DL NEXUS")
    report_lines.append(f"**Data da Auditoria:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Status da Verificação:** {'🔴 BLOQUEADO (Segredos Encontrados)' if all_findings else '🟢 APROVADO'}\n")
    
    report_lines.append("## Resumo do Status Git")
    report_lines.append(f"- **Arquivos Adicionados:** {len(added_files)}")
    for f in added_files:
        report_lines.append(f"  - `{f}`")
    report_lines.append(f"- **Arquivos Modificados:** {len(modified_files)}")
    for f in modified_files:
        report_lines.append(f"  - `{f}`")
    report_lines.append("")
    
    report_lines.append("## Auditoria de Segurança (KILLCRITIC)")
    if all_findings:
        report_lines.append("> [!CAUTION]")
        report_lines.append("> **SEGREDOS DETECTADOS!** O commit foi preventivamente bloqueado para evitar vazamento de credenciais na branch do GitHub.")
        report_lines.append("")
        for filepath, findings in all_findings.items():
            report_lines.append(f"### Arquivo: `{filepath}`")
            report_lines.append("| Linha | Tipo de Alerta | Trecho do Código (Mascarado) |")
            report_lines.append("|---|---|---|")
            for line_num, snippet, secret_val, alert_type in findings:
                # Mascarar o segredo no snippet para não vazar no próprio relatório
                masked_val = secret_val[:4] + "..." + secret_val[-4:] if len(secret_val) > 8 else "..."
                masked_snippet = snippet.replace(secret_val, masked_val)
                report_lines.append(f"| {line_num} | {alert_type} | `{masked_snippet}` |")
            report_lines.append("")
    else:
        report_lines.append("> [!NOTE]")
        report_lines.append("> **NENHUM SEGREDO DETECTADO.** Todos os arquivos analisados estão em conformidade e livres de chaves/tokens em formato literal.")
        report_lines.append("")

    report_lines.append("## Estatísticas do Git Diff")
    report_lines.append("```text")
    report_lines.append(git_diff_summary if git_diff_summary else "Nenhuma modificação staged/unstaged detectada ou arquivo binário.")
    report_lines.append("```\n")

    report_lines.append("---")
    report_lines.append("**Resultado Final KILLCRITIC:** " + ("BLOQUEADO" if all_findings else "APROVADO"))

    report_content = "\n".join(report_lines)
    
    # Salvar relatório na raiz
    with open("RELATORIO_AUDITORIA_PRE_COMMIT_DL_NEXUS.md", "w", encoding="utf-8") as rf:
        rf.write(report_content)
        
    print(f"Auditoria concluída. Relatório salvo em: RELATORIO_AUDITORIA_PRE_COMMIT_DL_NEXUS.md")
    
    if all_findings:
        print("[ALERTA] Segredos foram encontrados nos arquivos locais. Verifique o relatorio.")
        # Retorna codigo 1 para bloquear o processo se necessario
        exit(1)
    else:
        print("[SUCESSO] Nenhum segredo exposto nos arquivos candidatos.")
        exit(0)

if __name__ == "__main__":
    main()
