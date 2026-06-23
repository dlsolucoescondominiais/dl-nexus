import os
import re

# Definição dos segredos e seus substitutos
REPLACEMENTS = {
    # 1. Token do Meta Graph API (long-lived)
    "EAF4obsfkqY4BRZBhoON47HF15BHX9m7Dajh4ZCmzVnd7UpZCScMdO7efyZCMZB07KWTk1iHahUZAFP9ZCITfSe1TfkomU0wiMUn9xUXI0KxDE0s2NbM8VQViEkQxym4H1pMM1j9m102uP295u0MdKFa2oiInZC6OfEGgGS1mRxdfK9VY5ohKr4MDl2ZBCZCKXxqybHai40fzFmvtIP": "os.environ.get('META_PAGE_ACCESS_TOKEN_DL')",
    "EAF4obsfkqY4BR4umA4fZBx7VvwX1rZBxK1XixvVY2ARjGbMx4ZB2o2k9jKWdRMKo4jta2zhzRzZCO6jzAyb1pBnzF3xJ4SZBqFwu43ZBu5dx0ZAZB5Fy5n3kOifFhknZCMcnGx3ZBAkZAc6tiUfDADTaXYGx9ZAQwaU9jZB7wulGmNqtOGtAx06tZBFcWWvOTAZCyKZAHsPYWHZAZCUjlAg7DZASDktns84mGy5MRg4gBWvdKrnpY6aCeqga8CHqlkZA7ZCEZD": "os.environ.get('META_PAGE_ACCESS_TOKEN_DL')",
    
    # 2. Token do n8n Cloud
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJuOG4iLCJpYXQiOjE3NzM4NjY3OTgsImV4cCI6MTc4OTQyNjc5OH0.wXk7z_Xp6kI5dZ68yM8VjF4T0jZ6a89694M4S4a-sWXw": "os.environ.get('N8N_API_KEY')",
    
    # 3. Senha do banco de dados Supabase
    "D89g9#@B3aN3x7s": "process.env.SUPABASE_DB_PASSWORD || 'your_db_password'",
    
    # 4. Token Anon do Supabase
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lamR0dmtwaWNsYWdzbmZsanN6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzM4NjY3OTEsImV4cCI6MjA4OTQ0MzI2MX0.j-qXVUaStEbtglVsw5kKNUEdqB5Z-NxXs7QIaRflttc": "process.env.SUPABASE_ANON_KEY || 'your_supabase_anon_key'",
}

# Lista de arquivos para higienizar (com base nas falhas de auditoria)
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

def main():
    print("Iniciando sanitização de segredos em arquivos específicos...")
    workspace = r"d:\AntiGravity\projeto_01"
    
    for relative_path in FILES_TO_CLEAN:
        filepath = os.path.join(workspace, relative_path)
        if not os.path.exists(filepath):
            print(f"[Aviso] Arquivo não encontrado, pulando: {relative_path}")
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            modified = False
            for secret, replacement in REPLACEMENTS.items():
                if secret in content:
                    # Ajustar substituição dependendo do tipo do arquivo
                    actual_replacement = replacement
                    if relative_path.endswith(".js"):
                        # Se for JS, usar sintaxe process.env
                        if "os.environ.get" in replacement:
                            var_name = re.search(r"'(.*?)'", replacement).group(1)
                            actual_replacement = f"process.env.{var_name}"
                    elif relative_path.endswith(".bat"):
                        # Se for .bat, usar valor padrão explicativo
                        actual_replacement = "N8N_API_KEY_PLACEHOLDER"
                    elif relative_path.endswith(".md"):
                        # Se for Markdown, usar placeholder explicativo
                        actual_replacement = "META_PAGE_ACCESS_TOKEN_PLACEHOLDER"
                    elif relative_path.endswith(".py"):
                        # Se for .py, usar import os + os.environ.get se necessário
                        if "os.environ.get" in replacement:
                            if "import os" not in content:
                                content = "import os\n" + content
                                
                    # Tratar as aspas do literal para não quebrar a sintaxe do script
                    # Ex: access_token = 'EAF4...' -> access_token = os.environ.get(...)
                    # Notar que o literal estava envolto em aspas simples ou duplas.
                    # Nós vamos substituir a chave literal crua.
                    # Se o replacement for código como os.environ.get, a linha original era:
                    # token = 'EAF4...' -> se substituirmos cru fica token = 'os.environ.get(...)'
                    # que é uma string literal! Para evitar isso, se a chave estava envolta em aspas,
                    # podemos substituir incluindo as aspas na busca.
                    for quote in ["'", '"']:
                        quoted_secret = f"{quote}{secret}{quote}"
                        if quoted_secret in content:
                            if "os.environ.get" in replacement or "process.env" in replacement:
                                # Substituir sem as aspas, pois o substituto é código executável
                                content = content.replace(quoted_secret, replacement)
                            else:
                                # Substituir com as aspas se o substituto for string literal
                                content = content.replace(quoted_secret, f"{quote}{replacement}{quote}")
                            modified = True
                            
                    # Substituição genérica caso não estivesse entre aspas (fallback)
                    if secret in content:
                        content = content.replace(secret, replacement)
                        modified = True
                        
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"[SUCESSO] Sanitizado: {relative_path}")
            else:
                print(f"[OK] Nenhum segredo encontrado em: {relative_path}")
                
        except Exception as e:
            print(f"Erro ao processar {relative_path}: {e}")

if __name__ == "__main__":
    main()
