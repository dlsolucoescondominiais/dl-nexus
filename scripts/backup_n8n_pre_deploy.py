import urllib.request
import json
import ssl
import os
from datetime import datetime

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""

if os.path.exists(ENV_FILE):
    with open(ENV_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("N8N_API_KEY="):
                n8n_api_key = line.split("=", 1)[1].strip()
            elif line.startswith("N8N_HOST="):
                n8n_host = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Accept": "application/json"
}

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Gerar nome da pasta de backup com data e hora
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
backup_dir_name = f"BACKUP_PRE_DEPLOY_{timestamp}"
backup_dir = os.path.join(r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\13_N8N_PRODUCAO_SYNC", backup_dir_name)
os.makedirs(backup_dir, exist_ok=True)

print(f"Iniciando backup preventivo para {backup_dir}...")

active_workflows = []
inactive_workflows = []
backup_count = 0
failed_count = 0
failed_details = []

try:
    req = urllib.request.Request(n8n_host + "workflows", headers=headers)
    with urllib.request.urlopen(req, context=ctx) as response:
        res = json.loads(response.read().decode('utf-8'))
        workflows = res.get('data', [])
        
        for wf in workflows:
            wf_id = wf.get('id')
            wf_name = wf.get('name')
            is_active = wf.get('active', False)
            
            # Sanitizar nome de arquivo
            safe_name = "".join(c if c.isalnum() else "_" for c in wf_name)
            file_name = f"{wf_id}_{safe_name}.json"
            file_path = os.path.join(backup_dir, file_name)
            
            # Fetch workflow completo
            try:
                req_wf = urllib.request.Request(f"{n8n_host}workflows/{wf_id}", headers=headers)
                with urllib.request.urlopen(req_wf, context=ctx) as r_wf:
                    full_wf = json.loads(r_wf.read().decode('utf-8'))
                    with open(file_path, 'w', encoding='utf-8') as fw:
                        json.dump(full_wf, fw, indent=2, ensure_ascii=False)
                    backup_count += 1
            except Exception as e_wf:
                print(f"Erro ao baixar workflow {wf_name} (ID: {wf_id}): {e_wf}")
                failed_count += 1
                failed_details.append(f"- **{wf_name}** (ID: {wf_id}) - Erro: {e_wf}")
            
            status_symbol = "✅ ATIVO" if is_active else "⏸️ INATIVO"
            wf_info = f"- **{wf_name}** (ID: {wf_id}) - Status: {status_symbol}"
            if is_active:
                active_workflows.append(wf_info)
            else:
                inactive_workflows.append(wf_info)
                
except Exception as e:
    print(f"Erro geral durante listagem de workflows: {e}")
    failed_details.append(f"- Falha na conexão geral da API: {e}")

# Gerar o RELATORIO_BACKUP_N8N_PRE_DEPLOY.md
report_lines = []
report_lines.append("# RELATÓRIO DE BACKUP PRE-DEPLOY — N8N PRODUÇÃO")
report_lines.append(f"**Data e Hora do Backup:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"**Diretório do Backup:** `DL_NEXUS_V3_LOCAL/13_N8N_PRODUCAO_SYNC/{backup_dir_name}/` \n")

report_lines.append("## Resumo Estatístico")
report_lines.append(f"- **Total de Workflows Localizados:** {len(active_workflows) + len(inactive_workflows)}")
report_lines.append(f"- **Salvos com Sucesso:** {backup_count}")
report_lines.append(f"- **Falhas no Download:** {failed_count}")
report_lines.append("")

report_lines.append("## Workflows Ativos na Produção")
if active_workflows:
    report_lines.extend(active_workflows)
else:
    report_lines.append("- *Nenhum workflow ativo localizado.*")
report_lines.append("")

report_lines.append("## Workflows Inativos na Produção")
if inactive_workflows:
    report_lines.extend(inactive_workflows)
else:
    report_lines.append("- *Nenhum workflow inativo localizado.*")
report_lines.append("")

report_lines.append("## Detalhes de Falhas e Alertas")
if failed_details:
    report_lines.extend(failed_details)
else:
    report_lines.append("- *Nenhuma falha de download registrada.*")
report_lines.append("")

report_lines.append("## Observações sobre Credenciais")
report_lines.append("- O n8n não retorna dados literais de chaves privadas ou senhas dos nós de credenciais por meio da API de Workflows. Elas estão salvas de forma segura no banco de dados interno do n8n Cloud.")
report_lines.append("- Este backup assegura a estrutura visual, parâmetros e códigos lógicos dos workflows. Em caso de restore, as conexões de credenciais correspondentes no n8n Cloud devem ser reassociadas.")
report_lines.append("")

report_content = "\n".join(report_lines)

# Salvar relatório na raiz
with open("RELATORIO_BACKUP_N8N_PRE_DEPLOY.md", "w", encoding="utf-8") as rf:
    rf.write(report_content)

print(f"Backup concluído com sucesso! {backup_count} workflows salvos.")
