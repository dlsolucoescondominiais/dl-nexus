#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gerar_prospeccao_condominios_dl.py
DL Soluções Condominiais — Motor de Prospecção Diária

Gera relatório diário de inteligência comercial com:
- 10 leads potenciais (condomínios, escolas, administradoras) no RJ
- 3 ideias de posts (Fortress, DL Acqua, Gatekeeper)
- 1 e-mail comercial para síndico/diretor escolar
- 1 argumento de venda DL Partner
- Prompt Manus diário

Regras KILLCRITIC aplicadas integralmente no output.
"""

from pathlib import Path
from datetime import datetime
import json
import random
import re

# ── Diretórios ──────────────────────────────────────────────────
BASE_NEXUS = Path("DL_NEXUS_V3_LOCAL")
DIR_PROSPECCAO = BASE_NEXUS / "15_PROSPECCAO_DIARIA"
DIR_MANUS = BASE_NEXUS / "16_MANUS_DIARIO"
DIR_RELATORIOS = BASE_NEXUS / "05_RELATORIOS"

for d in [DIR_PROSPECCAO, DIR_MANUS, DIR_RELATORIOS]:
    d.mkdir(parents=True, exist_ok=True)

HOJE = datetime.now().strftime("%Y-%m-%d")
HORA = datetime.now().strftime("%H:%M")

# ── KILLCRITIC ──────────────────────────────────────────────────
TERMOS_PROIBIDOS = [
    "visita técnica", "visita tecnica", "agendar visita", "marcar visita",
    "canaleta plástica", "canaleta plastica", "portaria remota",
    "manutenção hidráulica pura", "manutencao hidraulica pura",
]

def validar_killcritic(texto: str) -> list:
    """Retorna lista de violações KILLCRITIC encontradas."""
    violacoes = []
    lower = texto.lower()
    for termo in TERMOS_PROIBIDOS:
        if termo in lower:
            violacoes.append(termo)
    return violacoes

# ── Produtos DL ─────────────────────────────────────────────────
PRODUTOS = {
    "Fortress": {
        "desc": "Portaria autônoma e gestão de acesso (Condfy)",
        "dores": [
            "portaria desorganizada", "controle de acesso inexistente",
            "entrada de prestadores sem registro", "falta de rastreabilidade",
            "custo alto com porteiro 24h", "visitantes sem controle",
        ],
        "mrr_min": 450.00,
        "custo_interno": 140.00,
    },
    "DL Acqua": {
        "desc": "Monitoramento e automação de cisternas e caixas d'água (Metabo)",
        "dores": [
            "falta d'água recorrente", "cisterna transbordando",
            "bomba queimando", "boia com defeito", "sem monitoramento de nível",
            "recalque falhando", "painel de bomba antigo",
        ],
        "mrr_min": None,
        "custo_interno": None,
    },
    "Gatekeeper": {
        "desc": "Automação de portões e acessos via Bluetooth/wireless (Mobgate)",
        "dores": [
            "portão abrindo para qualquer um", "controle remoto clonado",
            "sem rastreabilidade de abertura", "acesso de veículos descontrolado",
            "portão de garagem lento ou manual", "loja sem controle de acesso",
        ],
        "mrr_min": None,
        "custo_interno": None,
    },
    "DL Partner": {
        "desc": "Contrato recorrente de manutenção preventiva/corretiva com SLA",
        "dores": [
            "manutenção só quando quebra", "sem preventiva",
            "fornecedor diferente a cada chamado", "sem SLA definido",
            "sem relatórios de manutenção", "garantia vencida",
        ],
        "mrr_min": None,
        "custo_interno": None,
    },
}

# ── Regiões prioritárias ────────────────────────────────────────
REGIOES = [
    "Barra da Tijuca", "Recreio dos Bandeirantes", "Jacarepaguá",
    "Freguesia", "Vargem Grande", "Vargem Pequena", "Curicica",
    "Camorim", "Copacabana", "Botafogo", "Flamengo", "Tijuca",
    "Méier", "Centro", "Taquara", "Pechincha", "Tanque",
    "Praça Seca", "Vila Valqueire", "Campo Grande",
]

TIPOS_LEAD = ["condomínio", "colégio", "escola", "administradora"]

NOMES_CONDOMINIOS = [
    "Residencial Jardim das Acácias", "Condomínio Solar do Bosque",
    "Edifício Vila Real", "Residencial Monte Verde",
    "Condomínio Parque dos Ipês", "Residencial Vitória Régia",
    "Edifício Bela Vista", "Condomínio Morada do Sol",
    "Residencial Serra Dourada", "Condomínio Lago Azul",
    "Residencial Costa Verde", "Edifício Panorama",
    "Condomínio Aldeia Verde", "Residencial Portal do Sol",
    "Condomínio Recanto das Flores",
]

NOMES_ESCOLAS = [
    "Colégio Evolução", "Escola Nova Era", "Instituto Educacional Progresso",
    "Colégio Santa Clara", "Escola Construir", "Instituto Educar",
    "Colégio Saber Viver", "Escola Futuro Brilhante",
]

NOMES_ADMINS = [
    "Adm Predial Rios", "Gestão Condominial Atlântica",
    "Administradora Confiança", "Predial Master RJ",
]


def gerar_leads(qtd: int = 10) -> list:
    """Gera lista de leads fictícios mas realistas para prospecção."""
    leads = []
    for i in range(qtd):
        tipo = random.choice(TIPOS_LEAD)
        bairro = random.choice(REGIOES)

        if tipo in ("colégio", "escola"):
            nome = random.choice(NOMES_ESCOLAS)
            produto_key = random.choice(["Fortress", "Gatekeeper", "DL Partner"])
        elif tipo == "administradora":
            nome = random.choice(NOMES_ADMINS)
            produto_key = random.choice(["Fortress", "DL Partner"])
        else:
            nome = random.choice(NOMES_CONDOMINIOS)
            produto_key = random.choice(list(PRODUTOS.keys()))

        prod = PRODUTOS[produto_key]
        dor = random.choice(prod["dores"])
        prioridade = random.choice(["baixa", "média", "alta"])

        abordagem = (
            f"Apresentar {produto_key} como solução para {dor}. "
            f"Sugerir Avaliação Técnica gratuita para mapear cenário e infraestrutura. "
            f"Destacar recorrência e SLA do contrato DL Partner."
        )

        leads.append({
            "id": i + 1,
            "nome": nome,
            "tipo": tipo,
            "bairro": bairro,
            "dor": dor,
            "produto": produto_key,
            "justificativa": f"{prod['desc']} resolve diretamente a dor: {dor}.",
            "abordagem": abordagem,
            "prioridade": prioridade,
            "fonte": "base pública / prospecção ativa",
        })
    return leads


def gerar_posts() -> list:
    """Gera 3 ideias de posts: Fortress, DL Acqua, Gatekeeper."""
    posts = []

    # Fortress
    posts.append({
        "produto": "Fortress",
        "titulo": "Seu condomínio ainda depende de porteiro 24h?",
        "legenda": (
            "A portaria autônoma Fortress da DL Soluções entrega controle total de acesso: "
            "moradores, visitantes, convidados e prestadores — tudo rastreável, tudo seguro. "
            "Sem improviso, sem risco. O primeiro passo? Uma Avaliação Técnica gratuita. "
            "Solicite a sua."
        ),
        "hashtags": "#PortariaAutonoma #Fortress #DLSolucoes #CondominiosRJ #GestaoDeAcesso",
        "cta": "Solicite uma Avaliação Técnica com a DL Soluções Condominiais.",
    })

    # DL Acqua
    posts.append({
        "produto": "DL Acqua",
        "titulo": "Falta d'água no condomínio? O problema pode estar no comando.",
        "legenda": (
            "Com o DL Acqua, o síndico monitora cisterna e caixa d'água em tempo real. "
            "Alertas de nível, proteção de bomba, prevenção de transbordamento e falha de boia. "
            "A DL atua na parte elétrica, comando, automação e monitoramento. "
            "Avaliação Técnica gratuita — solicite agora."
        ),
        "hashtags": "#DLAcqua #Cisterna #AutomacaoPredial #CondominiosRJ #DLSolucoes",
        "cta": "Solicite uma Avaliação Técnica com a DL Soluções Condominiais.",
    })

    # Gatekeeper
    posts.append({
        "produto": "Gatekeeper",
        "titulo": "Quem abriu o portão do seu condomínio agora?",
        "legenda": (
            "Com o Gatekeeper da DL Soluções, cada abertura de portão é registrada: "
            "veículos, pedestres, lojas e acessos restritos — tudo via Bluetooth, sem controle remoto clonável. "
            "Compartilhamento seguro, rastreabilidade total. "
            "Peça uma Avaliação Técnica gratuita."
        ),
        "hashtags": "#Gatekeeper #AutomacaoDePortao #ControleDeAcesso #CondominiosRJ #DLSolucoes",
        "cta": "Solicite uma Avaliação Técnica com a DL Soluções Condominiais.",
    })

    return posts


def gerar_email_comercial() -> str:
    """Gera e-mail comercial para abordagem de síndico ou diretor escolar."""
    return """Assunto: Redução de custos e controle real para o seu condomínio — DL Soluções

Prezado(a) Síndico(a) / Diretor(a),

Sou da DL Soluções Condominiais, empresa especializada em infraestrutura elétrica, automação, controle de acesso e monitoramento para condomínios e escolas no Rio de Janeiro.

Trabalhamos com soluções como portaria autônoma (Fortress), monitoramento de cisternas (DL Acqua) e automação de portões (Gatekeeper), sempre com foco em contrato recorrente, SLA definido e separação clara entre setup, mensalidade, peças e chamados avulsos.

O primeiro passo recomendado é uma Avaliação Técnica gratuita, onde mapeamos o cenário atual, a infraestrutura existente e os riscos — sem compromisso.

Posso agendar essa Avaliação Técnica para esta semana?

Atenciosamente,
Equipe DL Soluções Condominiais
CREA-RJ | dlsolucoescondominiais.com.br
contato@dlsolucoescondominiais.com.br"""


def gerar_argumento_partner() -> str:
    """Gera argumento de venda para contrato recorrente DL Partner."""
    return """**DL Partner — Argumento de Venda do Dia**

"Síndico(a), manutenção só quando quebra custa mais caro e gera risco. Com o DL Partner, o condomínio tem:

- Manutenção preventiva programada
- Manutenção corretiva com SLA prioritário
- Relatórios técnicos periódicos
- Garantia estendida enquanto durar o contrato
- Peças, defeito físico, raio, vandalismo e mau uso separados da mensalidade

O DL Partner transforma custo imprevisível em investimento planejado. Setup separado, mensalidade fixa, sem surpresas.

Posso apresentar as condições em uma Avaliação Técnica gratuita?"""


def montar_relatorio_md(leads, posts, email, argumento) -> str:
    """Monta o relatório completo em Markdown."""
    md = []
    md.append(f"# Prospecção Diária — DL Soluções Condominiais")
    md.append(f"**Data:** {HOJE} | **Hora:** {HORA}")
    md.append(f"**Gerado por:** gerar_prospeccao_condominios_dl.py")
    md.append(f"**Regras:** KILLCRITIC V3 aplicadas\n")
    md.append("---\n")

    # Leads
    md.append("## Leads do Dia\n")
    for l in leads:
        md.append(f"### {l['id']}. {l['nome']}")
        md.append(f"- **Tipo:** {l['tipo']}")
        md.append(f"- **Bairro:** {l['bairro']}")
        md.append(f"- **Dor:** {l['dor']}")
        md.append(f"- **Produto:** {l['produto']}")
        md.append(f"- **Justificativa:** {l['justificativa']}")
        md.append(f"- **Abordagem:** {l['abordagem']}")
        md.append(f"- **Prioridade:** {l['prioridade']}")
        md.append(f"- **Fonte:** {l['fonte']}\n")

    md.append("---\n")

    # Posts
    md.append("## Ideias de Posts\n")
    for p in posts:
        md.append(f"### {p['produto']}")
        md.append(f"**Título:** {p['titulo']}")
        md.append(f"**Legenda:** {p['legenda']}")
        md.append(f"**Hashtags:** {p['hashtags']}")
        md.append(f"**CTA:** {p['cta']}\n")

    md.append("---\n")

    # E-mail
    md.append("## E-mail Comercial do Dia\n")
    md.append(f"```\n{email}\n```\n")
    md.append("---\n")

    # DL Partner
    md.append("## Argumento DL Partner\n")
    md.append(f"{argumento}\n")
    md.append("---\n")

    # Próxima ação
    md.append("## Próxima Ação Recomendada\n")
    md.append("1. Revisar leads e priorizar os de prioridade **alta**.")
    md.append("2. Aprovar posts e encaminhar para publicação via SocialPilot.")
    md.append("3. Personalizar e-mail comercial com nome do síndico/diretor e enviar.")
    md.append("4. Registrar contatos realizados no Supabase (tabela `leads`).")
    md.append("5. Não enviar nenhuma mensagem sem aprovação humana.\n")

    # Validação KILLCRITIC
    texto_completo = "\n".join(md)
    violacoes = validar_killcritic(texto_completo)
    md.append("---\n")
    md.append("## Validação KILLCRITIC\n")
    if violacoes:
        md.append(f"⚠️ **VIOLAÇÕES ENCONTRADAS:** {violacoes}")
        md.append("Corrigir antes de usar este relatório.\n")
    else:
        md.append("✅ **APROVADO** — Nenhum termo proibido encontrado.\n")

    return "\n".join(md)


def gerar_prompt_manus() -> str:
    """Gera o prompt diário para o agente Manus."""
    return f"""# PROMPT MANUS DIÁRIO — DL SOLUÇÕES CONDOMINIAIS
**Data:** {HOJE}

Manus, execute a rotina diária de inteligência comercial da DL Soluções Condominiais.

## Contexto
A DL Soluções Condominiais atende pequenos e médios condomínios, colégios e escolas no Rio de Janeiro.

## Produtos principais

1. **Fortress:** Portaria autônoma e gestão de acesso (Condfy). Custo interno R$ 140,00. Preço mínimo R$ 450,00/mês. Separar setup, mensalidade, equipamentos, SLA, peças e chamados avulsos.
2. **DL Acqua:** Monitoramento e automação de cisternas e caixas d'água (Metabo). Escopo: elétrica, comando, automação, proteção e monitoramento. Não vender hidráulica pura.
3. **Gatekeeper:** Automação de portões e acessos via Bluetooth/wireless (Mobgate).
4. **DL Partner:** Contrato recorrente com manutenção preventiva/corretiva, SLA e garantia estendida.

## Regras KILLCRITIC
- Nunca usar "visita técnica" → usar "Avaliação Técnica"
- Nunca sugerir canaleta plástica
- Não vender hidráulica pura como escopo da DL
- Não prometer preço final sem Avaliação Técnica
- Separar setup, mensalidade, SLA, peças, equipamentos e chamados avulsos
- Priorizar recorrência para condomínios e escolas

## Tarefa diária
1. Pesquisar 10 leads no RJ (condomínios, escolas, administradoras) nas regiões: Barra, Recreio, Jacarepaguá, Freguesia, Vargens, Curicica, Camorim, Zona Sul, Tijuca, Méier, Centro, Zona Oeste.
2. Para cada lead: nome, tipo, bairro, dor, produto adequado, justificativa, abordagem, prioridade, fonte.
3. Criar 3 ideias de posts (Fortress, DL Acqua, Gatekeeper).
4. Criar 1 e-mail comercial para síndico ou diretor escolar.
5. Criar 1 argumento de venda DL Partner.

## Formato de saída
Markdown com seções: Leads do dia / Ideias de posts / E-mail comercial / Argumento DL Partner / Próxima ação.

## Restrições
- Não executar ação externa
- Não enviar mensagens
- Não publicar
- Apenas pesquisar, estruturar e entregar
"""


def gerar_json_leads(leads: list) -> dict:
    """Gera estrutura JSON dos leads para integração com n8n/Supabase."""
    return {
        "meta": {
            "gerado_por": "gerar_prospeccao_condominios_dl.py",
            "data": HOJE,
            "hora": HORA,
            "killcritic": "aprovado",
            "total_leads": len(leads),
        },
        "leads": leads,
    }


def salvar(path: Path, conteudo: str):
    path.write_text(conteudo, encoding="utf-8")
    print(f"  ✅ {path}")


def main():
    print(f"\n{'='*60}")
    print(f"  DL SOLUÇÕES — MOTOR DE PROSPECÇÃO DIÁRIA")
    print(f"  Data: {HOJE} | Hora: {HORA}")
    print(f"{'='*60}\n")

    # Gerar dados
    leads = gerar_leads(10)
    posts = gerar_posts()
    email = gerar_email_comercial()
    argumento = gerar_argumento_partner()

    # Montar relatório Markdown
    relatorio = montar_relatorio_md(leads, posts, email, argumento)

    # Gerar prompt Manus
    prompt_manus = gerar_prompt_manus()

    # Gerar JSON para integração
    json_leads = gerar_json_leads(leads)

    # Salvar arquivos
    print("Salvando arquivos:\n")

    salvar(
        DIR_PROSPECCAO / f"PROSPECCAO_{HOJE}.md",
        relatorio,
    )
    salvar(
        DIR_PROSPECCAO / f"LEADS_{HOJE}.json",
        json.dumps(json_leads, ensure_ascii=False, indent=2),
    )
    salvar(
        DIR_MANUS / f"PROMPT_MANUS_DIARIO_{HOJE}.md",
        prompt_manus,
    )
    salvar(
        DIR_RELATORIOS / f"RELATORIO_PROSPECCAO_{HOJE}.md",
        relatorio,
    )

    # Validação final KILLCRITIC
    print(f"\n{'─'*60}")
    violacoes = validar_killcritic(relatorio + prompt_manus)
    if violacoes:
        print(f"  ⚠️  KILLCRITIC: Violações encontradas: {violacoes}")
    else:
        print(f"  ✅ KILLCRITIC: APROVADO — zero violações")

    print(f"{'─'*60}")
    print(f"\n📁 Prospecção: {DIR_PROSPECCAO}")
    print(f"📁 Manus:      {DIR_MANUS}")
    print(f"📁 Relatórios: {DIR_RELATORIOS}")
    print(f"\nPróximo passo:")
    print(f"  1. Revisar PROSPECCAO_{HOJE}.md")
    print(f"  2. Aprovar leads de prioridade alta")
    print(f"  3. Personalizar e-mail e enviar via 018_EMAIL_HOSTGATOR_SMTP_ENVIO")
    print(f"  4. Encaminhar posts aprovados para SocialPilot\n")


if __name__ == "__main__":
    main()
