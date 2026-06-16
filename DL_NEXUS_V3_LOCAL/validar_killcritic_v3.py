import json
import sys
import os
from validar_killcritic_v2 import validate_workflow as validate_v2

def validate_v3(file_path):
    erros = validate_v2(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        # Erros de leitura/parse já são reportados pelo v2
        return erros

    nodes = data.get("nodes", [])

    # Validações V3 Específicas
    for node in nodes:
        node_type = node.get("type", "")

        # 1. Webhooks ou requisições HTTP
        if "webhook" in node_type.lower() or "httprequest" in node_type.lower():
            # Recomendação/Verificação de headerAuth em Webhooks (Router Entry Points)
            if "webhook" in node_type.lower() and "roteador" in data.get("name", "").lower():
                # Apenas aviso ou erro dependendo da rigorosidade
                pass # Aqui podemos futuramente forçar headerAuth se os nodes expõem credenciais

            # ContinueErrorOutput para HTTP nodes
            if "httprequest" in node_type.lower():
                on_error = node.get("onError", "")
                if on_error != "continueErrorOutput":
                    # Depende se eh critico ou nao, vamos apenas relatar como aviso no log, ou forçar se desejado
                    pass

    return erros

def main():
    if len(sys.argv) < 2:
        print("Uso: python validar_killcritic_v3.py <caminho_para_workflow.json>")
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
        erros = validate_v3(arq)
        if erros:
            print(f"❌ Falhas no arquivo {arq} (v3):")
            for e in erros:
                print(f"  - {e}")
            tem_erro_geral = True
        else:
            print(f"✅ Arquivo {arq} validado com sucesso (KILLCRITIC v3).")

    if tem_erro_geral:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
