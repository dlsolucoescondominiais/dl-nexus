from pathlib import Path
import json
from datetime import datetime

BASE = Path("DL_NEXUS_V3_LOCAL") / "11_N8N_AGENTES_V3"
BASE.mkdir(parents=True, exist_ok=True)

def salvar_json(nome, conteudo):
    path = BASE / nome
    path.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK JSON: {path}")

def salvar_txt(nome, conteudo):
    path = BASE / nome
    path.write_text(conteudo, encoding="utf-8")
    print(f"OK TXT: {path}")

PROMPT_ANINHA = """Você é Aninha, agente oficial de atendimento da DL Soluções Condominiais.

Função:
Atender leads vindos de WhatsApp, Instagram Direct, Facebook Messenger, Telegram, site, Google Meu Negócio e e-mail.

Objetivo:
Classificar o atendimento, identificar oportunidade comercial e encaminhar para Diego, Orçamento, Suporte ou Humano.

Público principal:
Condomínios pequenos e médios, colégios/escolas, síndicos, administradoras, gestores escolares e responsáveis por infraestrutura.

Serviços e produtos principais:
1. Fortress:
Sistema de gestão e integração com portaria autônoma, baseado em Condfy. Não chamar de portaria remota. Usar: portaria autônoma, gestão de acesso, controle de moradores, convidados, prestadores e serviços. Receita recorrente mínima: R$ 450,00 mensais para condomínio. Custo interno da licença: R$ 140,00. Separar mensalidade de setup, instalação física, equipamentos, peças e chamados avulsos.

2. DL Acqua:
Solução de controle, automação e monitoramento de cisternas e caixas dágua, baseada em Metabo. Permite acompanhamento em tempo real do nível, funcionamento, alertas e prevenção de falhas. A DL atua na parte elétrica, comando, automação, proteção e monitoramento. Não vender como hidráulica pura.

3. Gatekeeper:
Solução de automação de portões e acessos via Bluetooth/wireless, baseada em Mobgate. Controle e compartilhamento de abertura de portões de veículos, pedestres, lojas, portas de rolagem e acessos restritos.

Outros serviços:
DL Guardião: CFTV, câmeras, controle de acesso, facial, biometria, QR Code, senha, cerca elétrica e automação de portões.
DL Volt: elétrica, quadros, painéis, bombas, iluminação e comandos.
DL Alerta: sistemas de incêndio, central, detectores, sirenes, acionadores e iluminação de emergência.
DL EcoVolt: energia solar on-grid, off-grid, híbrida, manutenção solar e carport solar.
DL VoltCharge: infraestrutura para carregador veicular.
DL Partner: contratos recorrentes, manutenção preventiva, corretiva, relatórios, SLA e garantia estendida enquanto durar o contrato.

Regras obrigatórias:
- Nunca usar visita técnica.
- Sempre usar Avaliação Técnica.
- Nunca sugerir canaleta plástica como padrão.
- Priorizar infraestrutura profissional: eletrodutos adequados, tubulação industrial, conduletes, sealtubo e aço galvanizado quando aplicável.
- Nunca fechar preço final sem Avaliação Técnica ou validação humana.
- Sempre puxar oportunidades para contrato recorrente quando fizer sentido.
- Separar setup, mensalidade, SLA, peças, equipamentos e chamados avulsos.
- WhatsApp não deve ser usado para prospecção fria.
- A DL não atua como manutenção hidráulica pura.

Se o cliente pedir hidráulica pura:
Responder que a DL atua na parte elétrica, comando, automação, proteção, monitoramento e inteligência preventiva. Para vazamento, encanamento ou hidráulica pura, o ideal é profissional hidráulico. Se envolver bomba, cisterna, boia, nível, painel ou comando, oferecer Avaliação Técnica.

Formato de saída:
Responder sempre em JSON válido com:
{
  "agente": "Aninha",
  "lead_real": true,
  "classificacao": "",
  "produto_relacionado": "",
  "area_dl": "",
  "prioridade": "baixa|media|alta|critica",
  "nome": "",
  "telefone": "",
  "email": "",
  "condominio_escola_empresa": "",
  "bairro": "",
  "mensagem_cliente": "",
  "resposta_cliente": "",
  "proxima_acao": "",
  "encaminhar_para": "Diego|Orcamento|Suporte|Humano|SocialPilot|Nenhum"
}
"""

PROMPT_DIEGO = """Você é Diego, agente técnico e roteador operacional da DL Soluções Condominiais.

Função:
Receber leads qualificados pela Aninha, analisar tecnicamente, definir prioridade, sugerir Avaliação Técnica, identificar riscos e encaminhar para orçamento, suporte, contrato recorrente ou humano.

Foco:
Condomínios e colégios/escolas pequenos e médios no Rio de Janeiro.

Produtos estratégicos:
- Fortress: portaria autônoma e gestão de acesso.
- DL Acqua: monitoramento e automação de cisternas e caixas dágua.
- Gatekeeper: automação de portões e acessos.
- DL Commander Nexus: automação, comando, proteção e monitoramento de sistemas críticos.

Regras técnicas:
- Nunca usar visita técnica.
- Sempre usar Avaliação Técnica.
- Nunca sugerir canaleta plástica como padrão.
- Nunca assumir hidráulica pura como escopo da DL.
- Para bombas, cisternas, recalque, boias e painéis, atuar no escopo elétrico, comando, proteção, automação e monitoramento.
- Separar defeito físico, peça queimada, motor, fechadura, placa, fonte, impacto, raio, vandalismo e mau uso de mensalidade recorrente.
- Sempre separar setup, MRR, SLA, peças e chamados avulsos.

Formato de saída:
{
  "agente": "Diego",
  "diagnostico_preliminar": "",
  "risco_tecnico": "",
  "produto_indicado": "",
  "precisa_avaliacao_tecnica": true,
  "prioridade": "baixa|media|alta|critica",
  "dados_necessarios": [],
  "resposta_cliente": "",
  "proxima_acao": "",
  "encaminhar_para": "Orcamento|Suporte|Humano|Contrato|Nenhum"
}
"""

PROMPT_SOCIALPILOT = """Você é o SocialPilot, agente de marketing do DL Nexus.

Função:
Gerar conteúdo para Instagram, Facebook, TikTok, Google Meu Negócio e site da DL Soluções Condominiais.

Objetivo:
Divulgar a marca, gerar autoridade técnica, captar leads e vender contratos recorrentes para condomínios e colégios/escolas.

Produtos principais:
1. Fortress:
Portaria autônoma e gestão de acesso baseada em Condfy. Foco em síndicos, administradoras, escolas, moradores, convidados, prestadores e controle de entrada. Não chamar de portaria remota.

2. DL Acqua:
Monitoramento e automação de cisternas e caixas dágua baseado em Metabo. Foco em nível em tempo real, alertas, prevenção de falta dágua, transbordamento, falha de boia, recalque e bomba.

3. Gatekeeper:
Automação de portões e acessos via Bluetooth/wireless baseada em Mobgate. Foco em controle, compartilhamento seguro, rastreabilidade, praticidade e redução de controle físico.

Canais:
- Instagram
- Facebook
- TikTok
- Google Meu Negócio
- Site

Regras:
- Não publicar automaticamente sem aprovação humana.
- Gerar conteúdo pronto para aprovação do Diogo.
- Sempre puxar para Avaliação Técnica.
- Nunca usar visita técnica.
- Nunca sugerir canaleta plástica.
- Sempre puxar para contrato recorrente quando fizer sentido.
- Linguagem profissional, comercial, técnica e clara.

Formato de saída:
{
  "agente": "SocialPilot",
  "produto": "",
  "titulo": "",
  "legenda_instagram_facebook": "",
  "texto_google_meu_negocio": "",
  "ideia_video_tiktok_reels": "",
  "texto_site": "",
  "cta": "",
  "hashtags": [],
  "proxima_acao_comercial": "",
  "status": "aguardando_aprovacao_humana"
}
"""

README = """# DL Nexus V3  n8n com Agentes

Este pacote cria a base lógica dos workflows do n8n para coordenar:

- Aninha: atendimento e triagem.
- Diego: técnico e roteador.
- SocialPilot: postagens e marketing.
- Canais: WhatsApp, Telegram, Instagram Direct, Facebook, Google Meu Negócio, site e e-mail.
- Receita principal: contratos recorrentes para condomínios e colégios/escolas.

## Arquivos

000_DL_NEXUS_ORQUESTRADOR.json
Workflow central que recebe mensagens por webhook e decide se a demanda é atendimento, técnica ou postagem.

030_AGENT_ANINHA_ATENDIMENTO.json
Workflow de triagem de atendimento.

031_AGENT_DIEGO_TECNICO.json
Workflow técnico.

080_AGENT_SOCIALPILOT_POSTAGENS.json
Workflow para gerar conteúdo de marketing para aprovação humana.

## Regra de implantação

1. Importar primeiro o 000_DL_NEXUS_ORQUESTRADOR no n8n.
2. Testar via webhook manual.
3. Importar Aninha, Diego e SocialPilot.
4. Não conectar Meta, TikTok ou Google Meu Negócio antes dos testes manuais.
5. Toda publicação deve iniciar com aprovação humana.

## KILLCRITIC

Termos proibidos:
- visita técnica
- visita
- agendar visita
- canaleta plástica
- manutenção hidráulica pura

Termos obrigatórios:
- Avaliação Técnica
- infraestrutura profissional
- contrato recorrente
- setup separado da mensalidade
"""

def workflow_orquestrador():
    code = r'''
const body = $json.body || $json;

const texto = String(body.mensagem || body.message || body.text || body.caption || "").toLowerCase();
const canal = body.canal || body.channel || body.origem || "desconhecido";

const proibidos = [
  "visita técnica",
  "visita tecnica",
  "agendar visita",
  "marcar visita",
  "canaleta plástica",
  "canaleta plastica",
  "manutenção hidráulica pura",
  "manutencao hidraulica pura"
];

const termosEncontrados = proibidos.filter(t => texto.includes(t));

let tipo_fluxo = "atendimento";
let agente_destino = "Aninha";
let produto = "nao_classificado";
let prioridade = "media";

const palavrasPostagem = ["post", "postagem", "conteúdo", "conteudo", "legenda", "instagram", "facebook", "tiktok", "google meu negócio", "google meu negocio"];
const palavrasTecnicas = ["falha", "parou", "queimou", "disjuntor", "bomba", "cisterna", "painel", "central", "detector", "portão", "portao", "câmera offline", "camera offline"];
const palavrasUrgentes = ["urgente", "emergência", "emergencia", "sem água", "sem agua", "alarme disparando", "bomba parada"];

if (palavrasPostagem.some(p => texto.includes(p))) {
  tipo_fluxo = "postagem";
  agente_destino = "SocialPilot";
}

if (palavrasTecnicas.some(p => texto.includes(p))) {
  tipo_fluxo = "tecnico";
  agente_destino = "Diego";
}

if (palavrasUrgentes.some(p => texto.includes(p))) {
  prioridade = "alta";
}

if (texto.includes("portaria") || texto.includes("controle de acesso") || texto.includes("condfy")) {
  produto = "Fortress";
}

if (texto.includes("cisterna") || texto.includes("caixa d") || texto.includes("bomba") || texto.includes("recalque") || texto.includes("metabo")) {
  produto = "DL Acqua";
}

if (texto.includes("gatekeeper") || texto.includes("mobgate") || texto.includes("bluetooth") || texto.includes("wireless") || texto.includes("portão") || texto.includes("portao")) {
  produto = "Gatekeeper";
}

return [{
  json: {
    status: "DL_NEXUS_ROTEADO",
    canal,
    tipo_fluxo,
    agente_destino,
    produto,
    prioridade,
    killcritic_termos_encontrados: termosEncontrados,
    entrada_original: body,
    mensagem_normalizada: texto,
    regra_linguagem: "Usar sempre Avaliação Técnica. Nunca usar visita técnica."
  }
}];
'''
    return {
        "name": "000_DL_NEXUS_ORQUESTRADOR",
        "nodes": [
            {
                "parameters": {
                    "path": "dl-nexus-orquestrador",
                    "httpMethod": "POST",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "id": "webhook_orquestrador",
                "name": "Webhook DL Nexus Orquestrador",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {"jsCode": code},
                "id": "code_rotear",
                "name": "Roteador Central DL Nexus",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "respond",
                "name": "Responder Roteamento",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [800, 300]
            }
        ],
        "connections": {
            "Webhook DL Nexus Orquestrador": {
                "main": [[{"node": "Roteador Central DL Nexus", "type": "main", "index": 0}]]
            },
            "Roteador Central DL Nexus": {
                "main": [[{"node": "Responder Roteamento", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "ORQUESTRADOR"}]
    }

def workflow_aninha():
    code = r'''
const body = $json.body || $json;

const msg = String(body.mensagem || body.message || body.text || "").toLowerCase();

let produto = "nao_classificado";
let area = "atendimento_geral";
let prioridade = "media";

if (msg.includes("portaria") || msg.includes("controle de acesso") || msg.includes("condfy") || msg.includes("facial")) {
  produto = "Fortress";
  area = "seguranca_controle_acesso";
}

if (msg.includes("cisterna") || msg.includes("caixa d") || msg.includes("bomba") || msg.includes("boia") || msg.includes("recalque")) {
  produto = "DL Acqua";
  area = "automacao_bombas_cisternas";
}

if (msg.includes("portão") || msg.includes("portao") || msg.includes("bluetooth") || msg.includes("wireless") || msg.includes("mobgate")) {
  produto = "Gatekeeper";
  area = "automacao_portoes_acessos";
}

if (msg.includes("urgente") || msg.includes("parou") || msg.includes("sem água") || msg.includes("sem agua")) {
  prioridade = "alta";
}

const resposta = `Olá. Recebemos sua solicitação pela DL Soluções Condominiais. A demanda foi relacionada a ${produto}. Para avançarmos com segurança, o próximo passo recomendado é uma Avaliação Técnica, onde analisamos o cenário, a infraestrutura existente, os riscos e a melhor solução para o condomínio ou escola. Por gentileza, envie nome do condomínio/escola, bairro, telefone para contato e fotos ou vídeos se houver.`;

return [{
  json: {
    agente: "Aninha",
    lead_real: true,
    classificacao: "lead_comercial",
    produto_relacionado: produto,
    area_dl: area,
    prioridade,
    nome: body.nome || "",
    telefone: body.telefone || body.phone || "",
    email: body.email || "",
    condominio_escola_empresa: body.condominio || body.empresa || "",
    bairro: body.bairro || "",
    mensagem_cliente: body.mensagem || body.message || body.text || "",
    resposta_cliente: resposta,
    proxima_acao: "coletar_dados_e_encaminhar_para_diego_ou_orcamento",
    encaminhar_para: prioridade === "alta" ? "Diego" : "Orcamento"
  }
}];
'''
    return {
        "name": "030_AGENT_ANINHA_ATENDIMENTO",
        "nodes": [
            {
                "parameters": {
                    "path": "agent-aninha-atendimento",
                    "httpMethod": "POST",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "id": "webhook",
                "name": "Webhook Aninha Atendimento",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {"jsCode": code},
                "id": "code",
                "name": "Aninha Classificar e Responder",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "respond",
                "name": "Responder Aninha",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [800, 300]
            }
        ],
        "connections": {
            "Webhook Aninha Atendimento": {
                "main": [[{"node": "Aninha Classificar e Responder", "type": "main", "index": 0}]]
            },
            "Aninha Classificar e Responder": {
                "main": [[{"node": "Responder Aninha", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "ANINHA"}]
    }

def workflow_diego():
    code = r'''
const body = $json.body || $json;
const msg = String(body.mensagem || body.message || body.text || body.mensagem_cliente || "").toLowerCase();

let produto_indicado = body.produto_relacionado || "nao_classificado";
let prioridade = body.prioridade || "media";
let risco = "risco_nao_identificado";
let dados = [];

if (msg.includes("bomba") || msg.includes("cisterna") || msg.includes("boia") || msg.includes("recalque") || msg.includes("nivel") || msg.includes("nível")) {
  produto_indicado = "DL Acqua / DL Commander Nexus";
  risco = "risco_de_falta_dagua_transbordamento_ou_falha_de_comando";
  prioridade = "alta";
  dados = ["fotos do painel", "foto da bomba", "foto da boia/sensor", "descrição da falha", "bairro", "nome do condomínio"];
}

if (msg.includes("portaria") || msg.includes("controle de acesso") || msg.includes("facial")) {
  produto_indicado = "Fortress";
  risco = "risco_de_controle_de_acesso_desorganizado";
  dados = ["quantidade de acessos", "quantidade de moradores ou alunos", "pontos de entrada", "sistema atual", "bairro"];
}

if (msg.includes("portão") || msg.includes("portao") || msg.includes("bluetooth") || msg.includes("wireless")) {
  produto_indicado = "Gatekeeper";
  risco = "risco_de_acesso_sem_rastreabilidade";
  dados = ["tipo de portão", "quantidade de usuários", "local de instalação", "tipo de acionamento atual"];
}

const resposta = `Análise preliminar: a demanda indica oportunidade para ${produto_indicado}. Para definir escopo, infraestrutura e responsabilidades, recomendamos uma Avaliação Técnica da DL Soluções. Essa etapa permite separar setup, mensalidade, SLA, peças, equipamentos e chamados avulsos, evitando orçamento incorreto.`;

return [{
  json: {
    agente: "Diego",
    diagnostico_preliminar: resposta,
    risco_tecnico: risco,
    produto_indicado,
    precisa_avaliacao_tecnica: true,
    prioridade,
    dados_necessarios: dados,
    resposta_cliente: resposta,
    proxima_acao: "solicitar_dados_e_preparar_avaliacao_tecnica",
    encaminhar_para: "Orcamento"
  }
}];
'''
    return {
        "name": "031_AGENT_DIEGO_TECNICO",
        "nodes": [
            {
                "parameters": {
                    "path": "agent-diego-tecnico",
                    "httpMethod": "POST",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "id": "webhook",
                "name": "Webhook Diego Tecnico",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {"jsCode": code},
                "id": "code",
                "name": "Diego Diagnostico e Roteamento",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "respond",
                "name": "Responder Diego",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [800, 300]
            }
        ],
        "connections": {
            "Webhook Diego Tecnico": {
                "main": [[{"node": "Diego Diagnostico e Roteamento", "type": "main", "index": 0}]]
            },
            "Diego Diagnostico e Roteamento": {
                "main": [[{"node": "Responder Diego", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "DIEGO"}]
    }

def workflow_social():
    code = r'''
const body = $json.body || $json;
const produto = body.produto || body.produto_relacionado || "Fortress";
const tema = body.tema || body.mensagem || "contrato recorrente para condomínios e escolas";

let foco = "";
let hashtags = [];

if (produto.toLowerCase().includes("fortress")) {
  foco = "portaria autônoma, gestão de acesso, moradores, convidados, prestadores e controle para condomínios e escolas";
  hashtags = ["#PortariaAutonoma", "#ControleDeAcesso", "#CondominiosRJ", "#DLSolucoes", "#Fortress"];
}

if (produto.toLowerCase().includes("acqua")) {
  foco = "monitoramento de cisternas e caixas dágua, nível em tempo real, prevenção de falhas e proteção de bombas";
  hashtags = ["#DLAcqua", "#AutomacaoPredial", "#Cisterna", "#CondominiosRJ", "#DLSolucoes"];
}

if (produto.toLowerCase().includes("gatekeeper")) {
  foco = "automação de portões e acessos via Bluetooth ou wireless, controle compartilhado e rastreabilidade";
  hashtags = ["#Gatekeeper", "#AutomacaoDePortao", "#ControleDeAcesso", "#CondominiosRJ", "#DLSolucoes"];
}

const titulo = `${produto}: mais controle e segurança para condomínios e escolas`;

const legenda = `Síndicos e gestores escolares precisam de soluções que tragam controle, organização e recorrência operacional. Com ${produto}, a DL Soluções entrega ${foco}. Antes de qualquer implantação, realizamos uma Avaliação Técnica para entender o cenário, a infraestrutura e o melhor caminho para o condomínio ou escola.`;

const gmb = `${produto} da DL Soluções: solução para ${foco}. Atendimento para condomínios e escolas no Rio de Janeiro. Solicite uma Avaliação Técnica.`;

const video = `Vídeo curto mostrando o problema: falta de controle, risco ou desorganização. Depois apresentar ${produto} como solução da DL. Encerrar com CTA para Avaliação Técnica.`;

return [{
  json: {
    agente: "SocialPilot",
    produto,
    tema,
    titulo,
    legenda_instagram_facebook: legenda,
    texto_google_meu_negocio: gmb,
    ideia_video_tiktok_reels: video,
    texto_site: `${titulo}\n\n${legenda}`,
    cta: "Solicite uma Avaliação Técnica com a DL Soluções Condominiais.",
    hashtags,
    proxima_acao_comercial: "aprovar_post_e_publicar_manualmente",
    status: "aguardando_aprovacao_humana"
  }
}];
'''
    return {
        "name": "080_AGENT_SOCIALPILOT_POSTAGENS",
        "nodes": [
            {
                "parameters": {
                    "path": "agent-socialpilot-postagens",
                    "httpMethod": "POST",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "id": "webhook",
                "name": "Webhook SocialPilot Postagens",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 300]
            },
            {
                "parameters": {"jsCode": code},
                "id": "code",
                "name": "Gerar Conteudo SocialPilot",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [520, 300]
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{$json}}",
                    "options": {}
                },
                "id": "respond",
                "name": "Responder Conteudo",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [800, 300]
            }
        ],
        "connections": {
            "Webhook SocialPilot Postagens": {
                "main": [[{"node": "Gerar Conteudo SocialPilot", "type": "main", "index": 0}]]
            },
            "Gerar Conteudo SocialPilot": {
                "main": [[{"node": "Responder Conteudo", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "SOCIALPILOT"}]
    }

salvar_json("000_DL_NEXUS_ORQUESTRADOR.json", workflow_orquestrador())
salvar_json("030_AGENT_ANINHA_ATENDIMENTO.json", workflow_aninha())
salvar_json("031_AGENT_DIEGO_TECNICO.json", workflow_diego())
salvar_json("080_AGENT_SOCIALPILOT_POSTAGENS.json", workflow_social())

salvar_txt("PROMPT_ANINHA.txt", PROMPT_ANINHA)
salvar_txt("PROMPT_DIEGO.txt", PROMPT_DIEGO)
salvar_txt("PROMPT_SOCIALPILOT.txt", PROMPT_SOCIALPILOT)
salvar_txt("README_IMPLANTACAO.md", README)

print("")
print("PACOTE DL NEXUS V3 COM AGENTES CRIADO COM SUCESSO.")
print(f"Pasta: {BASE}")
print("")
print("Próximo passo:")
print("1. Rodar validar_killcritic.py")
print("2. Importar primeiro 000_DL_NEXUS_ORQUESTRADOR.json no n8n")
print("3. Testar via webhook manual")
