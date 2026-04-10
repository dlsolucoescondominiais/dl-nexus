import os
import json
import argparse
import requests

def deploy_workflow(file_path: str, n8n_url: str, api_key: str):
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo {file_path} nao encontrado.")
        return False

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Manter apenas as chaves permitidas pela API n8n
    workflow_data = {
        "name": data.get("name", "Untitled Workflow"),
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

    url = f"{n8n_url.rstrip('/')}/api/v1/workflows"

    print(f"Fazendo deploy de {file_path} para {url}...")
    try:
        response = requests.post(url, headers=headers, json=workflow_data)
        if response.status_code == 200:
            print("Deploy concluido com sucesso! HTTP 200 OK")
            print(f"ID do Workflow: {response.json().get('id')}")
            return True
        else:
            print(f"Falha no deploy. HTTP {response.status_code}")
            print(f"Erro: {response.text}")
            return False
    except Exception as e:
        print(f"Erro ao conectar com a API do n8n: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de Deploy CI/CD para n8n")
    parser.add_argument("file_path", help="Caminho para o arquivo JSON do workflow")
    args = parser.parse_args()

    n8n_url = os.getenv("N8N_URL")
    api_key = os.getenv("N8N_API_KEY")

    if not n8n_url or not api_key:
        print("Erro: N8N_URL e N8N_API_KEY precisam estar configuradas como variaveis de ambiente.")
    else:
        deploy_workflow(args.file_path, n8n_url, api_key)
