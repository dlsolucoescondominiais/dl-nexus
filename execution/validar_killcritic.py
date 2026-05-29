import os
import json
import sys
import re

BASE_DIR = "backend/n8n/workflows"

FORBIDDEN_TERMS = [
    "visita técnica",
    "visita tecnica",
    "vistoria",
    "canaleta plástica",
    "canaleta plastica",
    "manutenção hidráulica pura",
    "manutencao hidraulica pura"
]

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            content_lower = content.lower()

            # Removemos strings de instrução negativa ("nunca diga x", "não usamos x") para não acusar falso positivo
            content_lower = re.sub(r'nunca diga (visita t[eé]cnica)', '', content_lower)
            content_lower = re.sub(r'n[aã]o usamos (canaleta pl[aá]stica)', '', content_lower)
            content_lower = re.sub(r'auto de vistoria', '', content_lower)

            # Check forbidden again
            for term in FORBIDDEN_TERMS:
                if term.lower() in content_lower:
                    print(f"ERRO: Termo proibido '{term}' encontrado em {filepath}")
                    return False

            # Check for generic secrets (basic heuristic)
            try:
                data = json.loads(content)
                str_data = json.dumps(data)
                if "password=" in str_data.lower() or "secret=" in str_data.lower():
                    print(f"ERRO: Possível secret hardcoded em {filepath}")
                    return False
            except json.JSONDecodeError:
                print(f"ERRO: Arquivo JSON inválido: {filepath}")
                return False

            return True
    except Exception as e:
        print(f"Erro ao ler {filepath}: {e}")
        return False

def main():
    has_errors = False
    checked = 0

    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                if not check_file(filepath):
                    has_errors = True
                checked += 1

    print(f"\nVerificação concluída. {checked} arquivos analisados.")
    if has_errors:
        print("FALHA: Arquivos violam o Protocolo KILLCRITIC.")
        sys.exit(1)
    else:
        print("SUCESSO: Todos os arquivos seguem o Protocolo KILLCRITIC.")
        sys.exit(0)

if __name__ == "__main__":
    main()
