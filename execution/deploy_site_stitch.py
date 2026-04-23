#!/usr/bin/env python3
"""
DL Nexus — Deploy Site da DL Soluções no Google Stitch
======================================================
Envia todas as seções do site institucional da DL Soluções
para o projeto Stitch existente via API MCP.

Project ID: 1279935118882481507
URL: https://stitch.withgoogle.com/projects/1279935118882481507

Uso:
  python deploy_site_stitch.py              # Deploy completo (todas as telas)
  python deploy_site_stitch.py list         # Lista telas existentes
  python deploy_site_stitch.py hero         # Gera apenas a tela Hero
  python deploy_site_stitch.py servicos     # Gera apenas a tela Serviços
  python deploy_site_stitch.py status       # Status do projeto
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for emoji output
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Carrega variáveis do .env (com tratamento para caracteres nulos)
env_path = Path(__file__).resolve().parent.parent / ".env"
try:
    # Ler manualmente e filtrar linhas com null bytes
    with open(env_path, "r", encoding="utf-8", errors="replace") as f:
        clean_lines = []
        for line in f:
            if "\x00" not in line and "\ufffd" not in line:
                clean_lines.append(line)
    # Escrever .env limpo em temp e carregar
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False, encoding="utf-8") as tmp:
        tmp.writelines(clean_lines)
        tmp_path = tmp.name
    load_dotenv(tmp_path)
    os.unlink(tmp_path)
except Exception as e:
    print(f"⚠️ Erro ao carregar .env: {e}")
    load_dotenv(env_path)

# ========================
# CONFIGURAÇÃO
# ========================
STITCH_API_KEY = os.getenv("STITCH_API_KEY_1") or os.getenv("STITCH_API_KEY_2")
STITCH_BASE_URL = os.getenv("STITCH_BASE_URL", "https://stitch.googleapis.com/mcp")
PROJECT_ID = "1279935118882481507"

# ========================
# IDENTIDADE VISUAL DL
# ========================
DL_BRAND = """
IDENTIDADE VISUAL DA DL SOLUÇÕES CONDOMINIAIS:
- Paleta Principal: Background #060810 (escuro profundo), Cards #0D1117, Bordas #1E293B
- Cor Destaque: Âmbar/Dourado #F5A623 (cor principal da marca)
- Cor Elétrica: Ciano/Elétrico #00CFFF (cor secundária tech)
- Cor Sucesso: #10B981
- Tipografia Headlines: Manrope (Google Fonts), weight 800
- Tipografia Body: Inter (Google Fonts), weight 400-600
- Bordas: Arredondamento 16px (cards), 12px (inputs), 24px (botões pill)
- Efeito: Glassmorphism sutil, gradientes amber → escuro
- Shadow: 0 8px 32px rgba(245,166,35,0.15) para hover
- Tom: Premium, moderno, dark-mode, engenharia de alto padrão
- NUNCA usar cores chapadas (vermelho, azul puro). Sempre tons sofisticados.
- Animações: Hover com translateY(-6px) e border-color transition
"""

DL_CONTEXT = """
SOBRE A EMPRESA:
- Nome: DL Soluções Condominiais LTDA
- Setor: Engenharia elétrica, energia solar, CFTV, automação predial, prevenção de incêndio
- Público: Síndicos, administradoras de condomínios, escolas no Rio de Janeiro
- Diferencial: SLA de 8 horas, padrão ABNT, CREA-RJ: 2022106230 (Eng. Diogo Luiz de Oliveira)
- Avaliações: 5.0 estrelas no Google (49 avaliações)
- Telefones: (21) 96474-2458 e (21) 96878-2196
- Email: sac@dlsolucoescondominiais.com.br
- Site: www.dlsolucoescondominiais.com.br
- Região: Zona Sul, Norte, Oeste, Baixada Fluminense, Niterói

SUB-MARCAS DE SERVIÇO:
- DL Volt™ / DL Praxis™ — Engenharia Elétrica Predial
- DL EcoVolt Solar™ — Energia Solar Fotovoltaica
- DL Guardião™ — CFTV Forense e Segurança (parceiro Intelbras)
- DL Gatekeeper™ — Controle de Acesso (MobGate)
- DL Alerta™ — Prevenção e Combate a Incêndio
- DL VoltCharge™ — Carregadores de Veículos Elétricos

PARCEIROS: CREA-RJ, ABESE, Intelbras, Condfy, MobGate
"""


class StitchMCP:
    """Cliente Python para a API MCP do Google Stitch"""

    def __init__(self, api_key: str, base_url: str = None):
        self.api_key = api_key
        self.base_url = base_url or STITCH_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        })
        self._request_id = 0

    def _next_id(self):
        self._request_id += 1
        return self._request_id

    def call_tool(self, tool_name: str, arguments: dict = None) -> dict:
        """Chama uma ferramenta MCP do Stitch"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments or {}
            },
            "id": self._next_id()
        }
        print(f"   🔧 Chamando {tool_name}...")
        try:
            resp = self.session.post(self.base_url, json=payload, timeout=300)
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                print(f"   ❌ Erro MCP: {data['error']}")
            return data
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Erro HTTP: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"      Response: {e.response.text[:500]}")
            return {"error": str(e)}

    def list_tools(self) -> list:
        """Lista ferramentas disponíveis"""
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": self._next_id()
        }
        try:
            resp = self.session.post(self.base_url, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            return data.get("result", {}).get("tools", [])
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            return []

    def get_project(self, project_id: str) -> dict:
        """Detalhes do projeto"""
        return self.call_tool("get_project", {"projectId": project_id})

    def list_screens(self, project_id: str) -> dict:
        """Lista todas as telas do projeto"""
        return self.call_tool("list_screens", {"projectId": project_id})

    def get_screen(self, project_id: str, screen_id: str) -> dict:
        """Detalhes de uma tela"""
        return self.call_tool("get_screen", {
            "projectId": project_id,
            "screenId": screen_id
        })

    def generate_screen(self, project_id: str, prompt: str,
                        device_type: str = "DESKTOP") -> dict:
        """Gera uma nova tela UI a partir de prompt"""
        return self.call_tool("generate_screen_from_text", {
            "projectId": project_id,
            "prompt": prompt,
            "deviceType": device_type
        })

    def edit_screen(self, project_id: str, screen_id: str, prompt: str) -> dict:
        """Edita uma tela existente"""
        return self.call_tool("edit_screen", {
            "project_id": project_id,
            "screen_id": screen_id,
            "text_prompt": prompt
        })

    def extract_design_context(self, project_id: str, screen_id: str) -> dict:
        """Extrai DNA de design de uma tela"""
        return self.call_tool("extract_design_context", {
            "projectId": project_id,
            "screenId": screen_id
        })


# ========================
# PROMPTS DAS TELAS
# ========================

SCREEN_PROMPTS = {
    "01_hero": {
        "name": "Hero — Landing",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}
{DL_CONTEXT}

Crie uma HERO SECTION espetacular para o site da DL Soluções Condominiais.

LAYOUT:
- Navbar fixa no topo: logo DL à esquerda (quadrada com bordas arredondadas),
  links de navegação (Para Quem, Serviços, DL Nexus, Avaliações, Contato),
  botão "◈ Acessar Nexus" (cor ciano #00CFFF) e "Falar Agora" (outline âmbar).
- Hero fullscreen com background escuro (#060810) com glow gradiente âmbar no canto inferior esquerdo
  e ciano no canto superior direito.
- Badge no topo: "Rio de Janeiro · Zona Sul, Norte, Oeste e Baixada"
- Título principal em 3 linhas:
  Linha 1: "A" + "Infraestrutura Técnica" (cor âmbar #F5A623)
  Linha 2: "que o seu Condomínio"
  Linha 3: "Merece e Precisa." (segunda palavra em itálico sutil)
- Subtítulo: "Elétrica, Energia Solar, CFTV, Automação e Prevenção de Incêndio — tudo em um único parceiro técnico. SLA de 8 horas e padrão ABNT. Sem gambiarras, sem canaleta plástica."
- 2 botões CTA: "Solicitar Avaliação Técnica Gratuita" (botão primário âmbar),
  "Ver Portfólio de Serviços" (botão outline)
- 3 stats em row: "5 ★ / 49 Avaliações Google" | "8h / SLA de Atendimento" | "100% / Padrão ABNT"
- Font heading: Manrope 800, body: Inter 400-600
- Tudo em dark mode premium
"""
    },

    "02_para_quem": {
        "name": "Para Quem — Personas",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie uma seção "PARA QUEM É A DL" — perfis de clientes.

LAYOUT:
- Tag de seção: "Para Quem é a DL"
- Título: "Cada Cliente tem uma Dor Diferente. Nós Resolvemos a Sua."
- Subtítulo: "Entendemos as responsabilidades e pressões únicas de cada perfil. Por isso, nossa abordagem é personalizada desde o primeiro contato."
- Grid de 3 cards (persona-card) com fundo #0D1117, borda #1E293B, hover com sombra âmbar:

  Card 1 — SÍNDICO 🏢
  "Você precisa de agilidade, resolução sem drama para os moradores e laudos técnicos claros para apresentar na assembleia. Precisa confiar que a execução é segura, normatizada e sem retrabalho."
  Tag: "SLA de 8h · Laudos para Assembleia · Conformidade NR-10"

  Card 2 — ADMINISTRADORA 🏗️
  "Você gerencia múltiplos condomínios e precisa de um parceiro técnico que cumpra SLAs rigorosos, emita documentação técnica e entregue relatórios de compliance para o corpo diretivo."
  Tag: "Parceria B2B · Multi-condomínio · Documentação Técnica"

  Card 3 — ESCOLA 🏫
  "Segurança dos alunos é inegociável. Você precisa de CFTV forense, elétrica segura, energia eficiente e a certeza de que obras críticas serão executadas durante as férias escolares."
  Tag: "CFTV · Obras nas Férias · AVCB · Energia Solar"

- Dark mode, fontes Manrope/Inter, bordas 16px
"""
    },

    "03_diferenciais": {
        "name": "Diferenciais — Números",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie uma seção "DIFERENCIAIS" com métricas e banner de credenciamento.

LAYOUT:
- Tag: "Nossos Diferenciais"
- Título: "O Padrão DL que Fala por Si"
- Grid 4 cards de métricas (background #0D1117):
  ⭐ 5.0 — "Nota no Google (49 avaliações)"
  ⚡ 8h — "SLA de atendimento on-site"
  🛡️ 100% — "Projetos com padrão ABNT"
  🎓 CREA-RJ — "Reg. 2022106230 · Eng. Diogo Luiz de Oliveira"

- Banner CREA abaixo: imagem escura com overlay, dois lados:
  Esquerdo: Tag "Engenheiro Registrado · CREA-RJ", Nome "Diogo Luiz de Oliveira",
  "Reg. 2022106230 · Engenheiro responsável técnico. Laudos, projetos e ART emitidos por profissional habilitado."
  Direito: medalha 🏅 com "CREA-RJ" em âmbar e "Conselho Regional de Engenharia e Agronomia"

- Dark mode premium
"""
    },

    "04_servicos": {
        "name": "Serviços — Portfolio",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}
{DL_CONTEXT}

Crie a seção "SERVIÇOS" — grid de 6 cards de serviço.

LAYOUT:
- Tag: "Portfólio de Serviços"
- Título: "Um Ecossistema Técnico Completo para o Seu Patrimônio"
- Subtítulo: "Todas as verticais de engenharia que um condomínio moderno precisa, operadas por uma única empresa de confiança."

- Grid 3 colunas × 2 linhas, cards clicáveis com hover translateY(-6px):

  1. DL Volt™/DL Praxis™ — Engenharia Elétrica Predial
     Badge: "CREA-RJ · ART Inclusa" (pill âmbar)
     "Retrofit elétrico completo, quadros QDC, eletrodutos metálicos galvanizados. Sem gambiarras. Laudo CREA-RJ e ART incluso. ABNT NBR 5410."
     CTA: "Solicitar Retrofit Elétrico →"

  2. DL EcoVolt Solar™ — Energia Solar
     "Projetos solares para redução de até 95% na conta de energia das áreas comuns. Homologação CEMIG/ENEL. Lei 14.300."
     CTA: "Saiba mais →"

  3. DL Guardião™ — CFTV Forense (Intelbras)
     "Painel de monitoramento no tablet, Câmeras Full HD Intelbras, armazenamento cloud, acesso remoto. Qualidade jurídica de imagem para boletim de ocorrência."
     CTA: "Ver sistema CFTV →"

  4. DL Gatekeeper™ — Controle de Acesso
     Badge: "📱 App MobGate" (pill ciano)
     "Portão de garagem e porta pedestre pelo celular, sem internet. Biometria, RFID, reconhecimento facial. Portaria autônoma e remota."
     CTA: "Conhecer DL Gatekeeper →"

  5. DL Alerta™ — Prevenção de Incêndio
     "Sistemas de detecção e alarme eletrônico, sprinklers, sinalização de emergência. Adequação para AVCB/CBMERJ."
     CTA: "Saiba mais →"

  6. DL VoltCharge™ — Carregadores EV
     "Instalação de wallboxes e eletropostos em garagens de condomínios e estacionamentos. Compatível com todos os EVs."
     CTA: "Saiba mais →"

- Cada card: imagem placeholder no topo (16:9 ratio, escura), marca em pill, título h3, descrição, CTA em âmbar
- Cards: bg #0D1117, border #1E293B, border-radius 16px
"""
    },

    "05_nexus": {
        "name": "DL Nexus — Portal Tech",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie a seção "DL NEXUS" — portal tecnológico da empresa.

LAYOUT dividido em 2 colunas:

COLUNA ESQUERDA (conteúdo):
- Tag: "Portal Tecnológico"
- Título: "Conheça o DL Nexus" (Nexus em ciano #00CFFF)
- Descrição: "O DL Nexus é o nosso sistema inteligente de gestão de atendimento e orçamentos. Por ele, o seu pedido de avaliação técnica chega diretamente à nossa equipe de engenharia, é triado automaticamente e escalado para o Diretor Técnico sem burocracia."
- 4 features com ícone + texto:
  🤖 "Atendimento inteligente 24/7 com triagem automática por IA"
  📋 "Coleta técnica de dados precisos para orçamento real"
  🔔 "Notificação direta ao Diretor Técnico Diogo Luiz"
  🔒 "Seus dados são 100% seguros e privados — LGPD compliant"
- Botão grande: "◈ Acionar o DL Nexus →" (estilo ciano com glow)

COLUNA DIREITA (dashboard visual mockup):
- Card escuro simulando um painel:
  Header: "◈ DL Nexus" + "🟢 Sistema Ativo"
  Row: "Lead triado pela Aninha" — "✓ Classificado" (verde)
  Progress bar: "Progresso da Avaliação" — "Em andamento" (âmbar, 65%)
  Progress bar: "SLA de Resposta" — "7h 20min restantes" (ciano, 88%)
  Progress bar: "Satisfação do Cliente" — "5.0 / 5.0" (verde, 100%)
  Métricas: 49 Avaliações | 8h SLA | 100% ABNT

- Dark mode, bordas ciano sutis no dashboard
"""
    },

    "06_avaliacoes": {
        "name": "Avaliações + Mapa",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie a seção "AVALIAÇÕES" — prova social com reviews e mapa.

LAYOUT 2 colunas:

COLUNA ESQUERDA:
- Header: Logo "Google" + ★★★★★ + "5,0 · 49 avaliações no Google"
- 3 review cards empilhados:

  Review 1: ★★★★★
  "Empresa super profissional! Resolveram o problema elétrico do nosso condomínio rápido, com laudo técnico e tudo certinho. Recomendo muito!"
  Avatar "MF" — Marcia Freitas — Novembro 2025

  Review 2: ★★★★★
  "Instalaram o sistema de câmeras no nosso condomínio. Excelente qualidade de imagem, SLA cumprido à risca e a equipe foi extremamente profissional."
  Avatar "AN" — Antonio Neto — Junho 2025

  Review 3: ★★★★★
  "Fizeram o projeto de energia solar para as áreas comuns. Já vemos a economia na conta. Equipe super competente, vale muito a pena!"
  Avatar "CM" — Christian Marques — Junho 2025

- Link: "Ver todas as 49 avaliações no Google ↗"

COLUNA DIREITA:
- Google Maps embed (placeholder escuro com pin do RJ)
- Card info: "📍 Atendemos todo o Rio de Janeiro"
  "Zona Sul · Zona Norte · Zona Oeste · Baixada Fluminense · Niterói e Região Metropolitana"
  Telefones: (21) 96474-2458 | (21) 96878-2196

- Cards: bg #0D1117, avatares circulares com iniciais, estrelas em âmbar
"""
    },

    "07_contato": {
        "name": "Contato — Formulário CTA",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie a seção "CONTATO" — formulário de lead.

LAYOUT:
- Tag: "Avaliação Técnica Gratuita"
- Título: "Pronto para Resolver de Vez?"
- Subtítulo: "Preencha abaixo. Nossa equipe analisará o seu cenário e o Diretor Técnico Diogo Luiz entrará em contato em até 8 horas."

- Formulário centralizado (max-width 720px), background card:
  Row 1: Input "Nome Completo" | Input "WhatsApp (21) 9 0000-0000"
  Row 2: Select "Você é" (Síndico, Administradora, Escola, Outro) | Select "Serviço" (Elétrica, Solar, CFTV, Acesso, Incêndio, EV, Múltiplos)
  Textarea: "Descreva sua necessidade" (placeholder: "Ex: Temos 80 unidades, o quadro elétrico é de 2008...")
  Botão submit: "⚡ Acionar Avaliação Técnica Gratuita" (botão grande, dourado/âmbar)
  Texto legal: "Ao enviar, você concorda com nossa Política de Privacidade. Seus dados são protegidos pela LGPD."

- Inputs: bg escuro, border #1E293B → âmbar no focus, border-radius 12px
- Formulário com border sutil e fundo levemente mais claro que o bg
"""
    },

    "08_footer": {
        "name": "Footer — Rodapé",
        "device": "DESKTOP",
        "prompt": f"""
{DL_BRAND}

Crie o FOOTER do site da DL Soluções.

LAYOUT grid 4 colunas:

Coluna 1 — BRAND:
- Logo DL (quadrada, bordas arredondadas)
- Texto: "Engenharia elétrica, energia solar, CFTV, automação e prevenção de incêndio para condomínios e escolas no Rio de Janeiro. Padrão ABNT. SLA de 8 horas."
- Social icons: 📸 Instagram | 📘 Facebook | ▶️ YouTube

Coluna 2 — SERVIÇOS:
- DL Volt™ — Elétrica
- DL EcoVolt Solar™
- DL Guardião™ — CFTV
- DL Gatekeeper™ — Acesso
- DL Alerta™ — Incêndio
- DL VoltCharge™ — EV

Coluna 3 — EMPRESA:
- Quem Atendemos
- DL Nexus
- Avaliações Google
- Solicitar Avaliação
- Política de Privacidade
- LGPD

Coluna 4 — CONTATO:
- 📞 (21) 96474-2458
- 📞 (21) 96878-2196
- ✉️ sac@dlsolucoescondominiais.com.br
- 📍 Rio de Janeiro, RJ
- Link: "⭐ Nos avalie no Google →"

RODAPÉ BOTTOM:
- "© 2026 DL Soluções Condominiais LTDA · CNPJ registrado · Rio de Janeiro, RJ"
- Links: Privacidade | LGPD | Contato

- Background mais escuro que o body, border-top sutil
"""
    },

    "09_mobile_hero": {
        "name": "Mobile — Hero + Nav",
        "device": "MOBILE",
        "prompt": f"""
{DL_BRAND}
{DL_CONTEXT}

Crie a versão MOBILE do Hero da DL Soluções.

LAYOUT MOBILE (390px width):
- Navbar compacta: logo DL + hamburger ☰
- Menu mobile overlay: links empilhados + botão "Solicitar Avaliação"
- Hero vertical:
  Badge: "Rio de Janeiro · Zona Sul, Norte, Oeste e Baixada"
  Título: "A Infraestrutura Técnica que o seu Condomínio Merece e Precisa."
  Subtítulo curto
  Botão CTA empilhados (full-width)
  Stats em row (3 colunas compactas)
- WhatsApp floating button no canto inferior direito (verde, ícone WPP)

- Dark mode, mesma paleta, fontes menores, padding adaptado
"""
    },
}


# ========================
# FUNÇÕES DE DEPLOY
# ========================

def deploy_screen(client: StitchMCP, screen_key: str):
    """Deploy de uma tela específica"""
    if screen_key not in SCREEN_PROMPTS:
        print(f"❌ Tela '{screen_key}' não encontrada.")
        print(f"   Telas disponíveis: {', '.join(SCREEN_PROMPTS.keys())}")
        return None

    screen_def = SCREEN_PROMPTS[screen_key]
    print(f"\n🎨 Gerando tela: {screen_def['name']} ({screen_def['device']})...")
    print(f"   Projeto: {PROJECT_ID}")

    result = client.generate_screen(
        project_id=PROJECT_ID,
        prompt=screen_def["prompt"],
        device_type=screen_def["device"]
    )

    if "error" not in result:
        print(f"   ✅ Tela '{screen_def['name']}' gerada com sucesso!")
        # Tentar extrair screen_id do resultado
        content = result.get("result", {}).get("content", [])
        if content:
            for item in content:
                if isinstance(item, dict):
                    text = item.get("text", "")
                    if "screenId" in text or "screen_id" in text:
                        print(f"   📋 Detalhes: {text[:200]}")
    else:
        print(f"   ⚠️ Resultado: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")

    return result


def deploy_all(client: StitchMCP):
    """Deploy de todas as telas em sequência"""
    print("=" * 60)
    print("🚀 DL NEXUS — Deploy Completo no Google Stitch")
    print(f"📁 Projeto: {PROJECT_ID}")
    print(f"🎨 Total de telas: {len(SCREEN_PROMPTS)}")
    print("=" * 60)

    results = {}
    for i, (key, screen_def) in enumerate(SCREEN_PROMPTS.items(), 1):
        print(f"\n{'─' * 40}")
        print(f"[{i}/{len(SCREEN_PROMPTS)}] {screen_def['name']}")
        print(f"{'─' * 40}")

        result = deploy_screen(client, key)
        results[key] = result

        # Rate limiting — esperar entre chamadas
        if i < len(SCREEN_PROMPTS):
            wait_time = 10
            print(f"   ⏳ Aguardando {wait_time}s antes da próxima tela...")
            time.sleep(wait_time)

    print("\n" + "=" * 60)
    print("📊 RESUMO DO DEPLOY")
    print("=" * 60)
    success = sum(1 for r in results.values() if r and "error" not in r)
    print(f"   ✅ Sucesso: {success}/{len(SCREEN_PROMPTS)}")
    print(f"   🌐 Acesse: https://stitch.withgoogle.com/projects/{PROJECT_ID}")
    print("=" * 60)

    return results


def list_screens(client: StitchMCP):
    """Lista as telas existentes no projeto"""
    print(f"📋 Listando telas do projeto {PROJECT_ID}...")
    result = client.list_screens(PROJECT_ID)
    content = result.get("result", {}).get("content", [])
    if content:
        print(f"\n📱 Telas encontradas:")
        for item in content:
            if isinstance(item, dict):
                print(f"   {item.get('text', item)}")
            else:
                print(f"   {item}")
    else:
        print("   📭 Nenhuma tela encontrada ou formato inesperado.")
        print(f"   Raw: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
    return result


def project_status(client: StitchMCP):
    """Status do projeto"""
    print(f"🔍 Status do projeto {PROJECT_ID}...")
    result = client.get_project(PROJECT_ID)
    content = result.get("result", {}).get("content", [])
    if content:
        for item in content:
            if isinstance(item, dict):
                print(f"   {item.get('text', item)}")
            else:
                print(f"   {item}")
    else:
        print(f"   Raw: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")

    # Listar ferramentas disponíveis
    print(f"\n🔧 Ferramentas MCP disponíveis:")
    tools = client.list_tools()
    for tool in tools:
        name = tool.get("name", "?")
        desc = tool.get("description", "")[:80]
        print(f"   • {name}: {desc}")

    return result


# ========================
# MAIN
# ========================
if __name__ == "__main__":
    if not STITCH_API_KEY:
        print("❌ STITCH_API_KEY não encontrada no .env!")
        print("   Adicione STITCH_API_KEY_1 ou STITCH_API_KEY_2 ao arquivo .env")
        sys.exit(1)

    client = StitchMCP(STITCH_API_KEY)

    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "list":
            list_screens(client)
        elif cmd == "status":
            project_status(client)
        elif cmd == "all":
            deploy_all(client)
        elif cmd in SCREEN_PROMPTS:
            deploy_screen(client, cmd)
        else:
            # Tentar como prefixo (ex: "hero" → "01_hero")
            found = [k for k in SCREEN_PROMPTS if cmd in k]
            if found:
                deploy_screen(client, found[0])
            else:
                print(f"❌ Comando '{cmd}' não reconhecido.")
                print(f"\nUso: python {sys.argv[0]} [comando]")
                print(f"\nComandos:")
                print(f"  all      — Deploy de todas as telas")
                print(f"  list     — Listar telas existentes")
                print(f"  status   — Status do projeto + ferramentas")
                print(f"\nTelas individuais:")
                for k, v in SCREEN_PROMPTS.items():
                    print(f"  {k:20s} — {v['name']}")
    else:
        deploy_all(client)
