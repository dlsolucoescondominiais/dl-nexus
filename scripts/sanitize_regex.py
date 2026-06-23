import os
import re

TOKEN_LIKE_REGEX = re.compile(
    r'\b(EAF4[a-zA-Z0-9]{30,}|eyJ[a-zA-Z0-9_\-]{10,}\.eyJ[a-zA-Z0-9_\-]{10,}\.[a-zA-Z0-9_\-]{20,}|sbp_[a-zA-Z0-9]{30,}|sk-svcacct-[a-zA-Z0-9_\-]{30,}|AIzaSy[a-zA-Z0-9_\-]{30,}|sk-proj-[a-zA-Z0-9_\-]{30,})\b'
)

# Arquivos a processar
FILES_TO_CLEAN = [
    r"check_meta_token.py",
    r"cleanup_n8n.py",
    r"create_ai_credentials.py",
    r"create_credentials.py",
    r"deploy_150.py",
    r"deploy_151.py",
    r"deploy_aninha_executiva.py",
    r"deploy_aninha_executiva_v2.py",
    r"deploy_aninha_executiva_v3.py",
    r"deploy_aninha_v3.py",
    r"find_conflict.py",
    r"mass_delete_junk.py",
    r"scripts/debug_n8n.py",
    r"scripts/fetch_070_from_n8n.py",
    r"scripts/fetch_070_original.py",
    r"scripts/update_env_meta.py",
    r"test_meta.py",
    r"update_nvidia_cred.py",
    r"analyze_marketing.py",
    r"scripts/clean_supabase_tokens.py",
    r"backend/supabase/run_sql.js",
    r"start_mcp_n8n.bat",
    r"REFERENCIA_CATALOG_API.md"
]

def clean_file(filepath, rel_path):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        modified = False
        
        # 1. Procurar todos os tokens usando a regex
        matches = TOKEN_LIKE_REGEX.findall(content)
        for token in set(matches):
            # Determinar o substituto adequado
            if token.startswith("eyJ"):
                # JWT (provavelmente n8n ou supabase anon)
                if "clean_supabase_tokens" in rel_path:
                    replacement = "process.env.SUPABASE_ANON_KEY"
                else:
                    replacement = "os.environ.get('N8N_API_KEY')" if rel_path.endswith(".py") else "process.env.N8N_API_KEY"
            elif token.startswith("EAF4"):
                # Meta Token
                replacement = "os.environ.get('META_PAGE_ACCESS_TOKEN_DL')" if rel_path.endswith(".py") else "process.env.META_PAGE_ACCESS_TOKEN_DL"
            elif token.startswith("AIzaSy"):
                # Gemini Key
                replacement = "os.environ.get('GEMINI_API_KEY_MOTOR')" if rel_path.endswith(".py") else "process.env.GEMINI_API_KEY_MOTOR"
            else:
                replacement = "os.environ.get('API_KEY_PLACEHOLDER')"
                
            # Substituir no arquivo, tratando as aspas
            for quote in ["'", '"']:
                quoted_token = f"{quote}{token}{quote}"
                if quoted_token in content:
                    content = content.replace(quoted_token, replacement)
                    modified = True
                    
            if token in content:
                content = content.replace(token, replacement)
                modified = True
                
        # 2. Casos especiais adicionais de palavras-chave
        if "D89g9#@B3aN3x7s" in content:
            content = content.replace("D89g9#@B3aN3x7s", "process.env.SUPABASE_DB_PASSWORD || 'your_db_password'")
            modified = True

        if modified:
            if rel_path.endswith(".py") and "os.environ.get" in content and "import os" not in content:
                content = "import os\n" + content
                
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[REPLACED] Sanitizado: {rel_path}")
        else:
            print(f"[OK] Sem alterações: {rel_path}")
            
    except Exception as e:
        print(f"Erro ao processar {rel_path}: {e}")

def main():
    print("Iniciando sanitização avançada por Regex...")
    workspace = r"d:\AntiGravity\projeto_01"
    for rel_path in FILES_TO_CLEAN:
        filepath = os.path.join(workspace, rel_path)
        if os.path.exists(filepath):
            clean_file(filepath, rel_path)

if __name__ == "__main__":
    main()
