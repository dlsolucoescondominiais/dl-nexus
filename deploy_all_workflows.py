import os
import json
import urllib.request
import urllib.error
import ssl
import sys
import argparse

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Carregar credenciais do .env local
ENV_FILE = ".env"
n8n_api_key = ""
n8n_host = ""

if os.path.exists(ENV_FILE):
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("N8N_API_KEY="):
                n8n_api_key = line.split("=", 1)[1].strip()
            elif line.startswith("N8N_HOST="):
                n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith('/'):
    n8n_host += '/'

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def parse_args():
    parser = argparse.ArgumentParser(description="Deploy controlado de workflows para o n8n Cloud.")
    parser.add_argument("--dry-run", action="store_true", help="Simula o deploy sem efetuar alterações reais na nuvem.")
    parser.add_argument("--allowlist", type=str, default="", help="Lista de nomes de workflows separados por vírgula para processar (ex: 081_PUBLICADOR_INSTAGRAM_META_API,082_PUBLICADOR_FACEBOOK_META_API,151_MAQUINA_CONTEUDO_META_DL_4X_DIA).")
    parser.add_argument("--import-inactive", action="store_true", default=True, help="Força a importação do workflow como inativo (default: True).")
    parser.add_argument("--no-activate", action="store_true", help="Força explicitamente a não ativação do workflow.")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Determinar se ativa ou não
    # Se --no-activate estiver presente, ou se --import-inactive for verdadeiro (que é o default), nós NÃO ativaremos.
    should_activate = not (args.import_inactive or args.no_activate)
    
    # Processar allowlist se fornecida
    allowlist = []
    if args.allowlist:
        allowlist = [item.strip() for item in args.allowlist.split(",") if item.strip()]
        print(f"[*] Modo Allowlist Ativo. Apenas os seguintes workflows serão processados: {allowlist}")
    else:
        print("[!] ATENÇÃO: Nenhuma allowlist fornecida. Rodando em modo completo (cuidado!).")

    base_dir = "DL_NEXUS_V3_LOCAL"
    
    if args.dry_run:
        print("[DRY-RUN] Simulação de deploy iniciada...")
    else:
        print("[*] Iniciando deploy seguro para o n8n Cloud...")

    # Obter os workflows existentes no servidor
    existing_workflows = {}
    if not args.dry_run:
        try:
            req = urllib.request.Request(n8n_host + "workflows", headers=headers, method="GET")
            resp = urllib.request.urlopen(req, context=ctx)
            data = json.loads(resp.read().decode('utf-8'))
            for wf in data.get('data', []):
                existing_workflows[wf.get('name')] = wf.get('id')
            print(f"[+] Obtidos {len(existing_workflows)} workflows do n8n Cloud para conferência.")
        except Exception as e:
            print(f"[-] Erro ao obter workflows do servidor: {e}")
            print("[*] Prosseguindo em modo cego de criação...")

    processed_count = 0
    success_count = 0
    
    for root, _, files in os.walk(base_dir):
        # Ignorar pastas que não sejam 12_N8N_WORKFLOWS_PROXIMOS ou 11_N8N_AGENTES_V3
        rel_path = os.path.relpath(root, base_dir)
        if not (rel_path.startswith("12_N8N_WORKFLOWS_PROXIMOS") or rel_path.startswith("11_N8N_AGENTES_V3")):
            continue
        for filename in files:
            if not filename.endswith('.json'):
                continue
            
            # Checar allowlist
            wf_name_base = filename.replace('.json', '')
            if allowlist:
                # Checa correspondência exata ou por prefixo
                matched = False
                for item in allowlist:
                    if item in wf_name_base or wf_name_base.startswith(item):
                        matched = True
                        break
                if not matched:
                    continue

            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            try:
                workflow_data = json.loads(content)
            except json.JSONDecodeError:
                continue

            if not isinstance(workflow_data, dict) or 'nodes' not in workflow_data or 'connections' not in workflow_data:
                continue

            wf_name = workflow_data.get('name')
            if not wf_name:
                wf_name = wf_name_base
                workflow_data['name'] = wf_name

            # Bloqueio rígido extra de segurança para workflows Manus
            if "manus" in wf_name.lower():
                print(f"[BLOQUEADO] Ignorando workflow legado Manus: {filename}")
                continue

            # Limpar metadados locais mantendo apenas chaves permitidas pela API n8n
            whitelist = ['name', 'nodes', 'connections', 'settings', 'staticData']
            clean_workflow_data = {k: v for k, v in workflow_data.items() if k in whitelist}

            processed_count += 1
            print(f"\n[*] Processando [{filename}] (Nome: {wf_name})...")
            
            if args.dry_run:
                action = "Atualizaria" if wf_name in existing_workflows else "Criaria"
                print(f"  [DRY-RUN] {action} workflow no servidor.")
                print(f"  [DRY-RUN] Manteria status: INATIVO.")
                success_count += 1
                continue

            data_bytes = json.dumps(clean_workflow_data).encode('utf-8')
            server_id = existing_workflows.get(wf_name)
            
            try:
                if server_id:
                    req_put = urllib.request.Request(n8n_host + f"workflows/{server_id}", data=data_bytes, headers=headers, method="PUT")
                    resp = urllib.request.urlopen(req_put, context=ctx)
                    print(f"  [+] Atualizado com sucesso (ID: {server_id}).")
                else:
                    req_post = urllib.request.Request(n8n_host + "workflows", data=data_bytes, headers=headers, method="POST")
                    resp = urllib.request.urlopen(req_post, context=ctx)
                    resp_data = json.loads(resp.read().decode('utf-8'))
                    server_id = resp_data.get('id')
                    existing_workflows[wf_name] = server_id
                    print(f"  [+] Criado com sucesso (Novo ID: {server_id}).")
                
                # Ativação controlada
                if should_activate:
                    if server_id:
                        req_activate = urllib.request.Request(n8n_host + f"workflows/{server_id}/activate", data=b'{}', headers=headers, method="POST")
                        urllib.request.urlopen(req_activate, context=ctx)
                        print(f"  [+] Workflow ATIVADO na nuvem.")
                else:
                    # Se estivesse ativo anteriormente, devemos desativar para garantir
                    if server_id:
                        try:
                            req_deactivate = urllib.request.Request(n8n_host + f"workflows/{server_id}/deactivate", data=b'{}', headers=headers, method="POST")
                            urllib.request.urlopen(req_deactivate, context=ctx)
                            print(f"  [-] Forçado status: INATIVO.")
                        except Exception:
                            # Se falhar porque já estava inativo, tudo bem
                            print(f"  [-] Mantido status: INATIVO.")
                
                success_count += 1
                
            except urllib.error.HTTPError as e:
                resp_text = e.read().decode('utf-8')
                print(f"  [-] Erro API n8n: {e.code} - {resp_text}")
            except Exception as e:
                print(f"  [-] Erro de conexão/processamento: {e}")

    print("\n--- RESUMO DO DEPLOY CONTROLADO ---")
    print(f"Total de candidatos encontrados na allowlist: {processed_count}")
    print(f"Sucesso: {success_count}")
    print(f"Status da simulação (Dry-Run): {'SIM' if args.dry_run else 'NÃO'}")
    print(f"Ativação automática após deploy: {'SIM' if should_activate else 'NÃO'}")

if __name__ == "__main__":
    main()
