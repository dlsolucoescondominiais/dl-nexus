import json
import sys
import os
import re

# TERMOS PROIBIDOS E PERMITIDOS SEGUNDO O PROTOCOLO KILLCRITIC DA DL
TERMOS_PROIBIDOS = [
    "visita técnica",
    "visita",
    "vistoria",
    "canaleta plástica",
    "manutenção hidráulica pura",
    "garantia vitalícia",
    "engenheiro"
]

TERMOS_PERMITIDOS = [
    "avaliação técnica",
    "auto de vistoria",
    "tecnólogo responsável",
    "responsável técnico",
    "nunca diga visita técnica"
]

SEGREDO_KEYS = ["password", "token", "api_key", "secret", "credentials"]

def check_termos(texto):
    if not isinstance(texto, str):
        return []
    texto_lower = texto.lower()
    erros = []

    # Bypass para termos permitidos (se o termo permitido estiver no texto, não alerta para a palavra proibida associada)
    # Ex: "auto de vistoria" tem "vistoria", mas não deve dar erro.
    for tp in TERMOS_PROIBIDOS:
        if tp in texto_lower:
            # check se faz parte de uma excecao
            is_exception = False
            if tp == "vistoria" and "auto de vistoria" in texto_lower:
                is_exception = True
            elif tp == "visita" or tp == "visita técnica":
                if "nunca diga visita técnica" in texto_lower:
                    is_exception = True

            if not is_exception:
                erros.append(f"Termo proibido encontrado: '{tp}'")

    return erros

def check_segredos(dict_obj):
    erros = []
    for k, v in dict_obj.items():
        if isinstance(k, str):
            for sk in SEGREDO_KEYS:
                if sk in k.lower():
                    erros.append(f"Possível segredo exposto na chave: {k}")
        if isinstance(v, str):
            for sk in SEGREDO_KEYS:
                if sk in v.lower() and len(v) > 5 and ' ' not in v: # simple heuristic for hardcoded tokens
                    erros.append(f"Possível segredo hardcoded no valor de chave {k}: {v[:5]}...")
        elif isinstance(v, dict):
            erros.extend(check_segredos(v))
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    erros.extend(check_segredos(item))
    return erros

def validate_workflow(file_path):
    print(f"Validando: {file_path}")
    erros = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return [f"JSON inválido: {e}"]
    except Exception as e:
        return [f"Erro ao ler arquivo: {e}"]

    # Estrutura obrigatoria
    for key in ["id", "name", "nodes", "connections"]:
        if key not in data:
            erros.append(f"Chave obrigatória ausente no root: {key}")

    # Active false (segurança)
    if data.get("active", True) is not False:
        erros.append("Workflow não está com active=false.")

    # Busca em todo o json text
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texto_completo = f.read()
            erros_termos = check_termos(texto_completo)
            erros.extend(erros_termos)
    except Exception as e:
        erros.append(f"Erro ao analisar termos no texto completo: {e}")

    # Verifica segredos hardcoded
    erros.extend(check_segredos(data))

    return erros

def main():
    if len(sys.argv) < 2:
        print("Uso: python validar_killcritic_v2.py <caminho_para_workflow.json>")
        sys.exit(1)

    target = sys.argv[1]

    arquivos = []
    if os.path.isfile(target):
        arquivos.append(target)
    elif os.path.isdir(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith('.json'):
                    arquivos.append(os.path.join(root, file))

    tem_erro_geral = False

    for arq in arquivos:
        erros = validate_workflow(arq)
        if erros:
            print(f"❌ Falhas no arquivo {arq}:")
            for e in erros:
                print(f"  - {e}")
            tem_erro_geral = True
        else:
            print(f"✅ Arquivo {arq} validado com sucesso (KILLCRITIC v2).")

    if tem_erro_geral:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
