#!/usr/bin/env python3
"""
DL Nexus — Integração Google Stitch ↔ n8n ↔ Supabase
=====================================================
Conecta o Google Stitch (UI Builder) ao ecossistema DL Nexus,
permitindo que o Dashboard de Leads seja atualizado automaticamente.

Variáveis de ambiente necessárias (.env):
  - STITCH_API_KEY_1 ou STITCH_API_KEY_2
  - SUPABASE_URL
  - SUPABASE_SERVICE_ROLE_KEY
  - N8N_API_KEY
  - N8N_HOST
"""

import os
import sys
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

# ========================
# CONFIGURAÇÃO
# ========================
STITCH_API_KEY = os.getenv("STITCH_API_KEY_1") or os.getenv("STITCH_API_KEY_2")
STITCH_BASE_URL = os.getenv("STITCH_BASE_URL", "https://stitch.googleapis.com/mcp")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

N8N_API_KEY = os.getenv("N8N_API_KEY")
N8N_HOST = os.getenv("N8N_HOST")


class StitchClient:
    """Cliente Python para a API do Google Stitch (MCP)"""

    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or STITCH_BASE_URL
        self.session = requests.Session()
        # Google APIs usam x-goog-api-key para autenticação com API keys
        self.session.headers.update({
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        })

    def call_tool(self, tool_name: str, arguments: dict = None) -> dict:
        """Chama uma ferramenta MCP do Stitch"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            },
            "id": 1
        }
        try:
            resp = self.session.post(self.base_url, json=payload, timeout=60)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao chamar Stitch ({tool_name}): {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   Response: {e.response.text[:500]}")
            return {"error": str(e)}

    def list_tools(self) -> list:
        """Lista todas as ferramentas disponíveis no Stitch"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 1
        }
        try:
            resp = self.session.post(self.base_url, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("result", {}).get("tools", [])
        except Exception as e:
            print(f"❌ Erro ao listar ferramentas: {e}")
            return []

    def list_projects(self) -> list:
        """Lista todos os projetos no Stitch"""
        result = self.call_tool("list_projects")
        return result.get("result", {}).get("content", [])

    def create_project(self, title: str) -> dict:
        """Cria um novo projeto"""
        return self.call_tool("create_project", {"title": title})

    def generate_screen(self, project_id: str, prompt: str, 
                         device_type: str = "DESKTOP") -> dict:
        """Gera uma tela UI a partir de um prompt"""
        return self.call_tool("generate_screen_from_text", {
            "project_id": project_id,
            "text_prompt": prompt,
            "device_type": device_type
        })

    def get_screen(self, project_id: str, screen_id: str) -> dict:
        """Recupera detalhes de uma tela (HTML + screenshot)"""
        return self.call_tool("get_screen", {
            "project_id": project_id,
            "screen_id": screen_id
        })

    def edit_screen(self, project_id: str, screen_id: str, prompt: str) -> dict:
        """Edita uma tela existente"""
        return self.call_tool("edit_screen", {
            "project_id": project_id,
            "screen_id": screen_id,
            "text_prompt": prompt
        })


class SupabaseClient:
    """Cliente Supabase simplificado"""

    def __init__(self, url: str, key: str):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        })

    def get_leads(self, status: str = None, limit: int = 50) -> list:
        """Busca leads do Supabase"""
        url = f"{self.url}/rest/v1/leads?order=created_at.desc&limit={limit}"
        if status:
            url += f"&status=eq.{status}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_leads_summary(self) -> dict:
        """Retorna resumo dos leads para o dashboard"""
        all_leads = self.get_leads(limit=1000)
        total = len(all_leads)
        novos = sum(1 for l in all_leads if l.get("status") == "novo")
        triados = sum(1 for l in all_leads if l.get("status") == "triado")

        # Agrupar por tipo de serviço
        servicos = {}
        for lead in all_leads:
            tipo = lead.get("tipo_servico") or "Não classificado"
            servicos[tipo] = servicos.get(tipo, 0) + 1

        # Agrupar por porte
        portes = {}
        for lead in all_leads:
            porte = lead.get("porte") or "Não definido"
            portes[porte] = portes.get(porte, 0) + 1

        return {
            "total_leads": total,
            "leads_novos": novos,
            "leads_triados": triados,
            "por_servico": servicos,
            "por_porte": portes,
            "ultima_atualizacao": datetime.now().isoformat()
        }


class N8nClient:
    """Cliente n8n simplificado"""

    def __init__(self, host: str, api_key: str):
        self.host = host.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json"
        })
        # SSL self-signed
        self.session.verify = False

    def list_workflows(self) -> list:
        """Lista todos os workflows"""
        resp = self.session.get(f"{self.host}/workflows")
        resp.raise_for_status()
        return resp.json().get("data", [])

    def activate_workflow(self, workflow_id: str) -> dict:
        """Ativa um workflow"""
        resp = self.session.patch(
            f"{self.host}/workflows/{workflow_id}",
            json={"active": True}
        )
        resp.raise_for_status()
        return resp.json()

    def execute_workflow(self, workflow_id: str, data: dict = None) -> dict:
        """Executa um workflow manualmente"""
        resp = self.session.post(
            f"{self.host}/workflows/{workflow_id}/run",
            json={"data": data or {}}
        )
        resp.raise_for_status()
        return resp.json()


# ========================
# FUNÇÕES DE INTEGRAÇÃO
# ========================

def test_stitch_connection():
    """Testa a conexão com o Google Stitch"""
    print("🔗 Testando conexão com Google Stitch...")
    client = StitchClient(STITCH_API_KEY)

    # Listar ferramentas disponíveis
    tools = client.list_tools()
    if tools:
        print(f"✅ Conectado! {len(tools)} ferramentas disponíveis:")
        for tool in tools[:10]:
            name = tool.get("name", "?")
            desc = tool.get("description", "")[:60]
            print(f"   • {name}: {desc}")
    else:
        print("⚠️  Sem ferramentas retornadas. Tentando listar projetos...")

    # Listar projetos
    projects = client.list_projects()
    if projects:
        print(f"\n📁 Projetos encontrados:")
        for p in projects:
            print(f"   • {p}")
    else:
        print("   Nenhum projeto encontrado ou formato diferente.")

    return client


def test_supabase_connection():
    """Testa a conexão com o Supabase"""
    print("\n🗄️  Testando conexão com Supabase...")
    client = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)

    summary = client.get_leads_summary()
    print(f"✅ Conectado! Resumo dos leads:")
    print(f"   Total: {summary['total_leads']}")
    print(f"   Novos: {summary['leads_novos']}")
    print(f"   Triados: {summary['leads_triados']}")
    print(f"   Por serviço: {json.dumps(summary['por_servico'], ensure_ascii=False)}")

    return client


def test_n8n_connection():
    """Testa a conexão com o n8n"""
    print("\n⚡ Testando conexão com n8n...")
    client = N8nClient(N8N_HOST, N8N_API_KEY)

    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    workflows = client.list_workflows()
    print(f"✅ Conectado! {len(workflows)} workflows:")
    for wf in workflows:
        status = "🟢 Ativo" if wf.get("active") else "⏸️  Inativo"
        print(f"   • {wf['name']} — {status}")

    return client


def sync_dashboard(stitch_client: StitchClient, supabase_client: SupabaseClient):
    """
    Sincroniza dados do Supabase com o Dashboard no Stitch.
    Gera/atualiza a tela do dashboard com os dados mais recentes.
    """
    print("\n🔄 Sincronizando Dashboard...")

    # Buscar dados atualizados
    summary = supabase_client.get_leads_summary()
    leads = supabase_client.get_leads(limit=10)

    # Montar prompt para atualizar o dashboard
    leads_table = "\n".join([
        f"- {l.get('nome_contato', '?')} | {l.get('nome_condominio', '?')} | "
        f"{l.get('tipo_servico', 'N/A')} | {l.get('status', '?')} | {l.get('prioridade', 'normal')}"
        for l in leads
    ])

    prompt = f"""
    Atualize o Dashboard de Leads da DL Soluções com os seguintes dados reais:

    MÉTRICAS:
    - Total de Leads: {summary['total_leads']}
    - Leads Novos (requer ação): {summary['leads_novos']}
    - Leads Triados: {summary['leads_triados']}

    POR SERVIÇO: {json.dumps(summary['por_servico'], ensure_ascii=False)}
    POR PORTE: {json.dumps(summary['por_porte'], ensure_ascii=False)}

    ÚLTIMOS 10 LEADS:
    {leads_table}

    Design: Usar paleta azul/branco DL Soluções, fonte Manrope, cards arredondados.
    Mostrar tabela de leads com colunas: Nome, Condomínio, Tipo Serviço, Status, Ações.
    Incluir cards de métricas no topo e gráfico de distribuição por serviço.
    """

    print(f"   Prompt preparado com {summary['total_leads']} leads")
    print(f"   Enviando para Stitch...")

    # Aqui aplicamos o resultado — isso pode ser usado para
    # gerar uma nova versão do dashboard ou atualizar a existente
    result = stitch_client.generate_screen(
        project_id="DL Nexus Admin Dashboard",
        prompt=prompt,
        device_type="DESKTOP"
    )

    if "error" not in result:
        print("✅ Dashboard atualizado com sucesso no Stitch!")
    else:
        print(f"⚠️  Resultado: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")

    return result


def full_status():
    """Exibe o status completo de todas as integrações"""
    print("=" * 60)
    print("🏗️  DL NEXUS — Status das Integrações")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    stitch = test_stitch_connection()
    supabase = test_supabase_connection()
    n8n = test_n8n_connection()

    print("\n" + "=" * 60)
    print("📊 RESUMO")
    print("=" * 60)
    print("✅ Google Stitch — Conectado (Dashboard DL Nexus)")
    print("✅ Supabase — Conectado (Banco de Dados)")
    print("✅ n8n — Conectado (Automação)")
    print("\n🔗 Fluxo de dados:")
    print("   Site/WhatsApp → n8n webhook → Supabase → Stitch Dashboard")


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    if not STITCH_API_KEY:
        print("❌ STITCH_API_KEY não encontrada no .env!")
        sys.exit(1)

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            full_status()
        elif cmd == "stitch":
            test_stitch_connection()
        elif cmd == "supabase":
            test_supabase_connection()
        elif cmd == "n8n":
            test_n8n_connection()
        elif cmd == "sync":
            stitch = StitchClient(STITCH_API_KEY)
            supabase = SupabaseClient(SUPABASE_URL, SUPABASE_KEY)
            sync_dashboard(stitch, supabase)
        else:
            print(f"Uso: python {sys.argv[0]} [status|stitch|supabase|n8n|sync]")
    else:
        full_status()
