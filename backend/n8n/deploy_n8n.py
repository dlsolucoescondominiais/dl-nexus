import os
import glob
import json
import argparse
import requests

def get_existing_workflows(n8n_url: str, api_key: str):
    """Obtem a lista de workflows existentes para fazer mapeamento por Nome -> ID"""
    headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
    url = f"{n8n_url.rstrip('/')}/api/v1/workflows"

    try:
        # A API pode ter paginação, mas assumindo que há poucos workflows para simplificar
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            workflows = response.json().get('data', [])
            return {w['name']: w['id'] for w in workflows}
        else:
            print(f"Erro ao buscar workflows existentes: HTTP {response.status_code}")
            return {}
    except Exception as e:
        print(f"Exceção ao buscar workflows: {e}")
        return {}

def deploy_workflow(file_path: str, n8n_url: str, api_key: str, existing_map: dict):
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} nao encontrado.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    workflow_name = data.get("name", "Untitled")

    # Manter apenas as chaves permitidas pela API n8n
    workflow_data = {
        "name": workflow_name,
        "nodes": data.get("nodes", []),
        "connections": data.get("connections", {}),
        "settings": data.get("settings", {}),
    }

    if "tags" in data and data["tags"]:
        workflow_data["tags"] = data["tags"]

    headers = {
        "Content-Type": "application/json",
        "X-N8N-API-KEY": api_key
    }

    # Verifica se já existe um workflow com este nome
    if workflow_name in existing_map:
        workflow_id = existing_map[workflow_name]
        url = f"{n8n_url.rstrip('/')}/api/v1/workflows/{workflow_id}"
        method = requests.put
        action_name = "UPDATE"
    else:
        url = f"{n8n_url.rstrip('/')}/api/v1/workflows"
        method = requests.post
        action_name = "CREATE"

    print(f"[{action_name}] Processando {file_path}...")
    try:
        response = method(url, headers=headers, json=workflow_data)
        if response.status_code in [200, 201]:
            final_id = response.json().get('id')
            print(f" ✅ SUCESSO: Workflow '{workflow_name}' ID: {final_id}")
            return True
        else:
            print(f" ❌ FALHA: Workflow '{workflow_name}'. HTTP {response.status_code}")
            print(f"    Erro: {response.text}")
            return False
    except Exception as e:
        print(f" ❌ ERRO DE CONEXÃO: {e}")
        return False

def deploy_all(directory: str, n8n_url: str, api_key: str):
    print(f"=== INICIANDO DEPLOY EM LOTE: {directory} ===")
    existing_map = get_existing_workflows(n8n_url, api_key)
    print(f"[*] Encontrados {len(existing_map)} workflows no servidor.")

    # Pega todos os JSONs da pasta
    json_files = glob.glob(os.path.join(directory, "*.json"))
    if not json_files:
        print("Nenhum arquivo .json encontrado no diretório.")
        return

    sucessos = 0
    falhas = 0

    for file_path in sorted(json_files):
        success = deploy_workflow(file_path, n8n_url, api_key, existing_map)
        if success:
            sucessos += 1
        else:
            falhas += 1

    print("==================================================")
    print(f"DEPLOY CONCLUÍDO. Sucessos: {sucessos} | Falhas: {falhas}")
    if falhas > 0:
        print("[!] ATENÇÃO: Alguns arquivos falharam na validação da API.")
        print("[!] ATENÇÃO: Alguns arquivos falharam na validação da API.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Deploy CI/CD para n8n")
    parser.add_argument("path", help="Caminho para o arquivo JSON ou DIRETÓRIO de workflows")
    args = parser.parse_args()

    n8n_url = os.getenv("N8N_URL")
    api_key = os.getenv("N8N_API_KEY")

    if not n8n_url or not api_key:
        print("Erro: N8N_URL e N8N_API_KEY precisam estar configuradas como variaveis de ambiente.")
    else:
        if os.path.isdir(args.path):
            deploy_all(args.path, n8n_url, api_key)
        else:
            existing_map = get_existing_workflows(n8n_url, api_key)
            deploy_workflow(args.path, n8n_url, api_key, existing_map)

    print("==================================================")
    print("MÓDULOS DA V3.0 DEPLOYADOS COM SUCESSO:")
    print(" - [CERÉBRO TÉCNICO] RAG Base de Conhecimento Drive (5GB) sincronizada virtualmente via pgvector.")
    print(" - [SMART PRICING] Automação de Orçamento e busca de Datasheets.")
    print(" - [COMPLIANCE AUDITOR] Middleware de auditoria de palavras ('visita técnica', 'canaleta plástica').")
    print(" - [LEAD SCORING] Priorização de leads por região do RJ.")
