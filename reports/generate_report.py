import json
import os
import glob

def parse_workflows():
    results = []

    # Paths to search
    paths = [
        "backend/n8n/workflows/**/*.json",
        "DL_NEXUS_V3_LOCAL/**/*.json"
    ]

    files = []
    for path in paths:
        files.extend(glob.glob(path, recursive=True))

    for file in files:
        if "node_modules" in file or ".git" in file or "LEADS_" in file or "leads_brutos" in file:
            continue

        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if isinstance(data, dict):
                # Basic n8n info
                name = data.get('name', 'N/A')
                is_active = data.get('active', False)
                nodes = data.get('nodes', [])
                node_count = len(nodes) if isinstance(nodes, list) else 0

                # Check for dependencies/integrations
                has_supabase = False
                has_ai = False
                has_webhooks = False
                has_http = False
                has_telegram = False
                has_meta = False

                if isinstance(nodes, list):
                    for node in nodes:
                        node_type = node.get('type', '')
                        if 'supabase' in node_type.lower(): has_supabase = True
                        if 'llm' in node_type.lower() or 'openai' in node_type.lower() or 'anthropic' in node_type.lower() or 'gemini' in node_type.lower() or 'ai' in node_type.lower(): has_ai = True
                        if 'webhook' in node_type.lower(): has_webhooks = True
                        if 'httpRequest' in node_type.lower(): has_http = True
                        if 'telegram' in node_type.lower(): has_telegram = True
                        if 'facebook' in node_type.lower() or 'instagram' in node_type.lower() or 'whatsapp' in node_type.lower(): has_meta = True

                results.append({
                    'file': file,
                    'name': name,
                    'active': is_active,
                    'node_count': node_count,
                    'deps': {
                        'supabase': has_supabase,
                        'ai': has_ai,
                        'webhooks': has_webhooks,
                        'http': has_http,
                        'telegram': has_telegram,
                        'meta': has_meta
                    },
                    'status': 'Valid'
                })
        except json.JSONDecodeError:
            results.append({
                'file': file,
                'name': 'N/A',
                'active': 'N/A',
                'node_count': 'N/A',
                'deps': {},
                'status': 'Invalid JSON'
            })
        except Exception as e:
            results.append({
                'file': file,
                'name': 'N/A',
                'active': 'N/A',
                'node_count': 'N/A',
                'deps': {},
                'status': f'Error: {str(e)}'
            })

    return results

def generate_markdown(results):
    md = "# Relatório de Status dos Workflows N8N - DL Nexus V3\n\n"

    md += "Este relatório detalha o status de todos os workflows JSON e suas dependências no ecosistema DL Nexus.\n\n"

    md += "## Resumo Executivo\n\n"
    total = len(results)
    valid = sum(1 for r in results if r['status'] == 'Valid')
    invalid = total - valid
    active = sum(1 for r in results if r['status'] == 'Valid' and r['active'] is True)

    md += f"- **Total de Arquivos Analisados:** {total}\n"
    md += f"- **Workflows Válidos:** {valid}\n"
    md += f"- **Workflows Inválidos/Com Erro:** {invalid}\n"
    md += f"- **Workflows Ativos:** {active}\n\n"

    md += "## Arquivos Inválidos\n\n"
    if invalid > 0:
        for r in results:
            if r['status'] != 'Valid':
                md += f"- `{r['file']}`: {r['status']}\n"
    else:
        md += "Nenhum arquivo JSON inválido encontrado.\n"
    md += "\n"

    md += "## Detalhamento dos Workflows\n\n"

    md += "| Arquivo | Nome do Workflow | Status Ativo | Qtd. Nodes | Dependências Principais |\n"
    md += "|---------|------------------|--------------|------------|-------------------------|\n"

    for r in sorted(results, key=lambda x: x['file']):
        if r['status'] == 'Valid':
            deps = []
            if r['deps'].get('supabase'): deps.append('Supabase')
            if r['deps'].get('ai'): deps.append('AI/LLM')
            if r['deps'].get('webhooks'): deps.append('Webhooks')
            if r['deps'].get('http'): deps.append('HTTP API')
            if r['deps'].get('telegram'): deps.append('Telegram')
            if r['deps'].get('meta'): deps.append('Meta (FB/IG/WA)')

            deps_str = ", ".join(deps) if deps else "Nenhuma detectada"
            active_str = "✅ Sim" if r['active'] else "❌ Não"

            md += f"| `{r['file']}` | {r['name']} | {active_str} | {r['node_count']} | {deps_str} |\n"

    with open('reports/n8n_status_report.md', 'w', encoding='utf-8') as f:
        f.write(md)

    print("Report generated at reports/n8n_status_report.md")

if __name__ == "__main__":
    results = parse_workflows()
    generate_markdown(results)
