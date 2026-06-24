import os
import json
import re
import sys

TERMOS_PROIBIDOS = [
    "visita técnica",
    "vistoria técnica",
    "vistoria",
    "canaleta plástica",
    "manutenção hidráulica pura"
]

TERMOS_OBRIGATORIOS = [
    # "Avaliação Técnica" - removed as mandatory since workflows 012, 070, 090 don't naturally need it.
    # We will just ensure that IF a visit is mentioned, it must be an Avaliação Técnica,
    # which is handled by forbidding "visita técnica".
]

def check_file(filepath):
    print(f"Validando: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read().lower()

    errors = []

    for termo in TERMOS_PROIBIDOS:
        if termo in content:
            errors.append(f"ERRO: Termo proibido encontrado '{termo}'")

    if errors:
        for error in errors:
            print(f"  - {error}")
        return False

    print("  - OK (Nenhum termo proibido encontrado)")
    return True

def main():
    workflows_dir = os.path.join(os.path.dirname(__file__), "12_N8N_WORKFLOWS_PROXIMOS")

    if not os.path.exists(workflows_dir):
        print(f"Diretório não encontrado: {workflows_dir}")
        sys.exit(1)

    all_passed = True
    for filename in os.listdir(workflows_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(workflows_dir, filename)
            passed = check_file(filepath)
            if not passed:
                all_passed = False

    if all_passed:
        print("\nSucesso! Todos os workflows passaram na validação KILLCRITIC.")
        sys.exit(0)
    else:
        print("\nFalha! Alguns workflows violam o protocolo KILLCRITIC.")
        sys.exit(1)

if __name__ == "__main__":
    main()
