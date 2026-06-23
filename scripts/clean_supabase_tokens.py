import os
import re

# Token do Supabase a higienizar
SUPABASE_TOKEN = process.env.SUPABASE_ANON_KEY

def clean_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        modified = False
        
        # 1. Substituir "Bearer eyJ..." por "=Bearer {{$env.SUPABASE_ANON_KEY}}"
        # Mas atenção, se a string de valor no JSON já tem as aspas, precisamos garantir que a substituição fique correta.
        # Ex: "value": "Bearer eyJ..." -> "value": "=Bearer {{$env.SUPABASE_ANON_KEY}}"
        bearer_pattern = r'Bearer\s+' + re.escape(SUPABASE_TOKEN)
        if re.search(bearer_pattern, content):
            content = re.sub(bearer_pattern, "=Bearer {{$env.SUPABASE_ANON_KEY}}", content)
            modified = True
            
        # 2. Substituir a chave pura se ainda restar
        if SUPABASE_TOKEN in content:
            # Substitui a chave pura. Mas se o "value": "eyJ..." for puro, no n8n a expressão precisa do prefixo '=' para ser avaliada.
            # Então se a chave pura for encontrada, vamos substituir por ={{$env.SUPABASE_ANON_KEY}}
            content = content.replace(SUPABASE_TOKEN, "={{$env.SUPABASE_ANON_KEY}}")
            # Caso tenhamos duplicado o sinal de igual (ex: "=={{$env...}}"), limpamos
            content = content.replace("=={{$env", "={{$env")
            modified = True
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[CLEANED] Higienizado tokens Supabase em: {filepath}")
            
    except Exception as e:
        print(f"Erro ao higienizar {filepath}: {e}")

def main():
    print("Iniciando limpeza em massa de tokens Supabase nos workflows JSON...")
    base_dir = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL"
    
    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                clean_file(filepath)
                
if __name__ == "__main__":
    main()
