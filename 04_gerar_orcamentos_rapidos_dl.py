#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
04_gerar_orcamentos_rapidos_dl.py
DL Soluções Condominiais — Gerador de Workflow n8n para Propostas

Fluxo:
  Manual Trigger → Set (Dados da proposta) → Code (Montar texto) → Output

KILLCRITIC aplicado. Nunca usa "visita técnica". Sempre "Avaliação Técnica".
"""

from pathlib import Path
import json
from datetime import datetime

BASE = Path("DL_NEXUS_V3_LOCAL") / "12_N8N_WORKFLOWS_PROXIMOS"
BASE.mkdir(parents=True, exist_ok=True)

HOJE = datetime.now().strftime("%Y-%m-%d")


def workflow_orcamento_rapido():
    """Gera workflow n8n: Manual Trigger → Set → Code → Output."""

    code_montar_proposta = r'''
const d = $json;

// ── KILLCRITIC inline ──
const proibidos = [
  "visita técnica","visita tecnica","agendar visita","marcar visita",
  "canaleta plástica","canaleta plastica","portaria remota",
  "manutenção hidráulica pura","manutencao hidraulica pura"
];
const texto_lower = JSON.stringify(d).toLowerCase();
const violacoes = proibidos.filter(t => texto_lower.includes(t));

// ── Catálogo de produtos ──
const catalogo = {
  "Fortress": {
    nome_completo: "Fortress — Portaria Autônoma e Gestão de Acesso",
    base: "Condfy",
    descricao: "Sistema de portaria autônoma com controle de moradores, visitantes, convidados, prestadores e integração com gestão condominial.",
    mrr_minimo: "R$ 450,00/mês",
    custo_interno: "R$ 140,00/mês",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "Equipamentos", "SLA", "Peças", "Chamados avulsos"],
    regra: "Nunca chamar de portaria remota. Usar: portaria autônoma."
  },
  "DL Acqua": {
    nome_completo: "DL Acqua — Monitoramento e Automação de Cisternas",
    base: "Metabo",
    descricao: "Controle, automação e monitoramento de cisternas e caixas d'água. Nível em tempo real, alertas, proteção de bomba, prevenção de falta d'água e transbordamento.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "Sensores", "SLA", "Peças", "Chamados avulsos"],
    regra: "A DL atua em elétrica, comando, automação, proteção e monitoramento. Não vender hidráulica pura."
  },
  "Gatekeeper": {
    nome_completo: "Gatekeeper — Automação de Portões e Acessos",
    base: "Mobgate",
    descricao: "Automação de portões e acessos via Bluetooth/wireless. Controle compartilhado, rastreabilidade e abertura de veículos, pedestres, lojas e acessos restritos.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "Módulos", "SLA", "Peças", "Chamados avulsos"],
    regra: "Foco em rastreabilidade e controle. Sem controle remoto clonável."
  },
  "DL Partner": {
    nome_completo: "DL Partner — Contrato Recorrente de Manutenção",
    base: "DL Soluções",
    descricao: "Contrato recorrente com manutenção preventiva, corretiva, relatórios, SLA prioritário e garantia estendida enquanto durar o contrato.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "SLA", "Peças (fora da mensalidade)", "Chamados avulsos"],
    regra: "Defeito físico, peça queimada, raio, vandalismo e mau uso são separados da mensalidade."
  },
  "DL Guardião": {
    nome_completo: "DL Guardião — CFTV e Segurança Eletrônica",
    base: "DL Soluções",
    descricao: "CFTV, câmeras, controle de acesso facial, biometria, QR Code, cerca elétrica e automação de portões.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "Equipamentos", "SLA", "Peças", "Chamados avulsos"],
    regra: "Priorizar infraestrutura profissional: eletrodutos, conduletes, sealtubo."
  },
  "DL Volt": {
    nome_completo: "DL Volt — Elétrica e Comandos",
    base: "DL Soluções",
    descricao: "Elétrica predial, quadros, painéis, bombas, iluminação e comandos.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Serviço", "Material", "Peças", "Chamados avulsos"],
    regra: "Nunca sugerir canaleta plástica como padrão."
  },
  "DL EcoVolt": {
    nome_completo: "DL EcoVolt — Energia Solar",
    base: "DL Soluções",
    descricao: "Energia solar on-grid, off-grid, híbrida, manutenção solar e carport solar.",
    mrr_minimo: "Sob Avaliação Técnica",
    custo_interno: "Variável",
    itens_separados: ["Setup/implantação", "Mensalidade (MRR)", "Equipamentos", "Manutenção"],
    regra: "Usar Lei 14.300 como argumento. Não prometer conta zerada."
  }
};

// ── Dados da proposta ──
const produto_key = d.produto || "Fortress";
const produto = catalogo[produto_key] || catalogo["Fortress"];

const cliente = d.nome_cliente || "Cliente";
const local = d.condominio_escola || "Condomínio/Escola";
const bairro = d.bairro || "Rio de Janeiro";
const demanda = d.demanda || "Solução de controle e automação";
const observacoes = d.observacoes || "";

// ── Montar proposta ──
const agora = new Date().toISOString().slice(0, 10);

let proposta = `# PROPOSTA COMERCIAL — DL SOLUÇÕES CONDOMINIAIS\n`;
proposta += `**Data:** ${agora}\n`;
proposta += `**Cliente:** ${cliente}\n`;
proposta += `**Local:** ${local} — ${bairro}\n`;
proposta += `**Produto:** ${produto.nome_completo}\n`;
proposta += `**Base tecnológica:** ${produto.base}\n\n`;
proposta += `---\n\n`;
proposta += `## Descrição da Solução\n\n`;
proposta += `${produto.descricao}\n\n`;
proposta += `## Demanda Identificada\n\n`;
proposta += `${demanda}\n\n`;

if (observacoes) {
  proposta += `## Observações\n\n${observacoes}\n\n`;
}

proposta += `## Estrutura de Custos\n\n`;
proposta += `| Componente | Valor |\n`;
proposta += `|-----------|-------|\n`;
produto.itens_separados.forEach(item => {
  proposta += `| ${item} | Sob Avaliação Técnica |\n`;
});
proposta += `\n**Valor mínimo recorrente:** ${produto.mrr_minimo}\n\n`;
proposta += `> **Nota:** Os valores finais serão definidos após Avaliação Técnica, `;
proposta += `onde analisamos o cenário, a infraestrutura existente, os riscos e a melhor solução.\n\n`;

proposta += `## Regras Aplicáveis\n\n`;
proposta += `- ${produto.regra}\n`;
proposta += `- Setup, mensalidade, SLA, peças, equipamentos e chamados avulsos são separados.\n`;
proposta += `- Defeito físico, peça queimada, raio, vandalismo e mau uso são separados da mensalidade.\n`;
proposta += `- Nenhum preço final é definido sem Avaliação Técnica.\n\n`;

proposta += `## Próximo Passo\n\n`;
proposta += `Recomendamos uma **Avaliação Técnica** para mapear cenário, infraestrutura e definir escopo com precisão.\n\n`;

proposta += `---\n`;
proposta += `*DL Soluções Condominiais LTDA — CREA-RJ*\n`;
proposta += `*contato@dlsolucoescondominiais.com.br*\n`;

return [{
  json: {
    status: "proposta_gerada",
    killcritic_violacoes: violacoes,
    killcritic_status: violacoes.length === 0 ? "APROVADO" : "VIOLACAO_DETECTADA",
    produto: produto_key,
    cliente,
    local,
    bairro,
    demanda,
    proposta_markdown: proposta,
    proxima_acao: "enviar_para_aprovacao_humana",
    data_geracao: agora
  }
}];
'''

    return {
        "name": "019_GERADOR_ORCAMENTO_RAPIDO",
        "nodes": [
            {
                "parameters": {},
                "id": "manual_trigger",
                "name": "Manual Trigger",
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [200, 300]
            },
            {
                "parameters": {
                    "mode": "raw",
                    "jsonOutput": json.dumps({
                        "produto": "Fortress",
                        "nome_cliente": "Síndico João",
                        "condominio_escola": "Residencial Solar do Bosque",
                        "bairro": "Barra da Tijuca",
                        "demanda": "Controle de acesso desorganizado, portaria sem rastreabilidade de visitantes e prestadores.",
                        "observacoes": "Condomínio com 3 blocos, 120 unidades, 2 portões de veículos e 1 de pedestres."
                    }, ensure_ascii=False),
                    "options": {}
                },
                "id": "set_dados",
                "name": "Set: Dados da Proposta",
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [440, 300]
            },
            {
                "parameters": {"jsCode": code_montar_proposta},
                "id": "code_proposta",
                "name": "Code: Montar Texto da Proposta",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [700, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "output",
                "name": "Output: Resultado Final",
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [960, 300]
            }
        ],
        "connections": {
            "Manual Trigger": {
                "main": [[{"node": "Set: Dados da Proposta", "type": "main", "index": 0}]]
            },
            "Set: Dados da Proposta": {
                "main": [[{"node": "Code: Montar Texto da Proposta", "type": "main", "index": 0}]]
            },
            "Code: Montar Texto da Proposta": {
                "main": [[{"node": "Output: Resultado Final", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "ORCAMENTO"}, {"name": "PROPOSTA"}]
    }


def salvar_json(nome, conteudo):
    path = BASE / nome
    path.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✅ {path}")


def main():
    print(f"\n{'='*60}")
    print("  DL SOLUÇÕES — GERADOR DE WORKFLOW: ORÇAMENTO RÁPIDO")
    print(f"  Data: {HOJE}")
    print(f"{'='*60}\n")

    wf = workflow_orcamento_rapido()
    salvar_json("019_GERADOR_ORCAMENTO_RAPIDO.json", wf)

    print(f"\n{'─'*60}")
    print("  Fluxo n8n gerado:")
    print("    Manual Trigger")
    print("      → Set: Dados da Proposta")
    print("      → Code: Montar Texto da Proposta (KILLCRITIC inline)")
    print("      → Output: Resultado Final")
    print(f"{'─'*60}")
    print("\n  Catálogo embutido: Fortress, DL Acqua, Gatekeeper,")
    print("  DL Partner, DL Guardião, DL Volt, DL EcoVolt")
    print("\n  Próximo passo:")
    print("    1. Importar 019_GERADOR_ORCAMENTO_RAPIDO.json no n8n")
    print("    2. Editar Set com dados reais do lead")
    print("    3. Executar manualmente")
    print("    4. Copiar proposta gerada e enviar para aprovação\n")


if __name__ == "__main__":
    main()
