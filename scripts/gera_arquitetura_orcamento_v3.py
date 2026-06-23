import json
import os

# Caminhos das pastas
PASTAS = [
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\09_PRONTOS_PARA_PRODUCAO'
]

def salvar_workflow(nome_arquivo, wf_data):
    for p in PASTAS:
        os.makedirs(p, exist_ok=True)
        caminho = os.path.join(p, nome_arquivo)
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(wf_data, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {nome_arquivo}")

def cria_workflow_agente(id_agente, nome, url_api, modelo, prompt_system):
    """Cria um workflow padrão de agente que recebe e responde usando o contrato"""
    nome_wf = f"{id_agente}_{nome}"
    is_gemini = 'googleapis' in url_api
    
    auth_header = [{"name": "Authorization", "value": "Bearer {{$env.DEEPSEEK_API_KEY}}"}]
    if is_gemini:
        auth_header = [] # Gemini usa query param key
        body = {
            "contents": [{"parts": [{"text": "SISTEMA:\n" + prompt_system + "\n\nPAYLOAD DO AGENTE:\n" + "={{JSON.stringify($json)}}"}]}],
            "generationConfig": {"response_mime_type": "application/json"}
        }
    else:
        body = {
            "model": modelo,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": "PAYLOAD DO AGENTE:\n={{JSON.stringify($json)}}"}
            ]
        }

    query_params = []
    if is_gemini:
        query_params = [{"name": "key", "value": "={{$env.GEMINI_API_KEY}}"}]

    parse_js = """
// Tenta extrair dados do body
let inputData = $json.body || $json;
return { json: inputData };
"""

    format_js = """
let orc_id = $('Parse Input').item.json.orcamento_id || "ID_NAO_INFORMADO";
let api_response = {};

try {
""" + (
    """  api_response = JSON.parse($('API LLM').item.json.candidates[0].content.parts[0].text);""" if is_gemini else 
    """  api_response = JSON.parse($('API LLM').item.json.choices[0].message.content);"""
) + """
} catch(e) {
  api_response = { erro: "Falha ao parsear JSON da LLM" };
}

return {
  json: {
    orcamento_id: orc_id,
    agente: \"""" + nome_wf + """\",
    status: api_response.erro ? "erro" : "ok",
    score_confianca: api_response.score_confianca || 85,
    dados: api_response,
    pendencias: []
  }
};
"""

    return {
        "name": nome_wf,
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": nome.lower().replace("_", "-"),
                    "responseMode": "lastNode",
                    "options": {}
                },
                "id": "webhook",
                "name": "Webhook Call",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [0, 0]
            },
            {
                "parameters": {"jsCode": parse_js},
                "id": "parse_input",
                "name": "Parse Input",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [200, 0]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": url_api,
                    "sendHeaders": True,
                    "headerParameters": {"parameters": auth_header + [{"name": "Content-Type", "value": "application/json"}]},
                    "sendQuery": is_gemini,
                    "queryParameters": {"parameters": query_params},
                    "sendBody": True,
                    "specifyBody": "json",
                    "jsonBody": json.dumps(body, ensure_ascii=False),
                    "options": {}
                },
                "id": "api_llm",
                "name": "API LLM",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [400, 0]
            },
            {
                "parameters": {"jsCode": format_js},
                "id": "format_output",
                "name": "Format Output",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 0]
            }
        ],
        "connections": {
            "Webhook Call": {"main": [[{"node": "Parse Input", "type": "main", "index": 0}]]},
            "Parse Input": {"main": [[{"node": "API LLM", "type": "main", "index": 0}]]},
            "API LLM": {"main": [[{"node": "Format Output", "type": "main", "index": 0}]]}
        },
        "active": False,
        "settings": {}
    }

# 189 NORMALIZADOR
wf_189 = {
    "name": "189_NORMALIZADOR_PAYLOAD_ORCAMENTO",
    "nodes": [
        {
            "parameters": {
                "httpMethod": "POST",
                "path": "orcamento-interno-dl",
                "responseMode": "lastNode",
                "options": {}
            },
            "id": "webhook",
            "name": "Webhook Recebe FormData",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [0, 0]
        },
        {
            "parameters": {
                "jsCode": """
const body = $input.item.json.body;
let payload_json = {};

if (body && body.payload_json) {
    try {
        payload_json = JSON.parse(body.payload_json);
    } catch(e) {}
}

const id = payload_json.meta?.orcamento_id || "ID_GERADO_" + Date.now();

const output = {
  orcamento_id: id,
  origem: "LP_ORCAMENTO_INTERNO",
  cliente: {
    nome: payload_json.cliente?.nome || "",
    tipo: payload_json.segmentacao_cliente?.tipo_cliente || "",
    documento: payload_json.cliente?.cl_cpf || payload_json.cliente?.cl_cnpj || "",
    telefone: payload_json.cliente?.telefone || "",
    email: payload_json.cliente?.email || ""
  },
  local: {
    endereco: payload_json.cliente?.cl_endereco || payload_json.cliente?.endereco || "",
    descricao: payload_json.segmentacao_cliente?.padrao_socioeconomico || "",
    estacionamento: "",
    escada: payload_json.diagnostico_base?.acesso_dificil_escada ? "Sim" : "Não"
  },
  servico: {
    linha_dl: payload_json.portfolio?.linha || "",
    categoria: payload_json.portfolio?.categoria || "",
    subcategoria: payload_json.portfolio?.servico_especifico || "",
    descricao_servico: payload_json.diagnostico_base?.resumo_visual || "",
    servicos_lista: [],
    chapa_lista: [],
    modalidade_lista: [payload_json.portfolio?.modalidade_comercial || ""]
  },
  tecnico: {
    voltagem: payload_json.parametros_tecnicos?.v_tensao || payload_json.parametros_tecnicos?.gr_tensao || payload_json.parametros_tecnicos?.cl_tensao_local || "",
    frequencia_hz: "60Hz",
    amperagem: payload_json.parametros_tecnicos?.v_corrente || "",
    rede_eletrica: "",
    concessionaria: ""
  },
  logistica: {
    urgencia: payload_json.parametros_comerciais_internos?.urgencia || "",
    tempo_execucao: "",
    tempo_deslocamento: "",
    qtd_profissionais: "",
    tempo_entrega: ""
  },
  interno: {
    material_interno: payload_json.parametros_comerciais_internos?.hardware_focado || "",
    custo_interno: "",
    notas_internas: "Necessita rasgo no gesso: " + (payload_json.diagnostico_base?.rasgo_gesso_alvenaria ? "Sim" : "Não")
  }
};

// Aqui chamaria o 190_MAESTRO
return { json: { payload_normalizado: output } };
"""
            },
            "id": "normaliza",
            "name": "Transforma em Contrato JSON",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [200, 0]
        },
        {
            "parameters": {
                "workflowId": "ID_MAESTRO_190"
            },
            "id": "chama_maestro",
            "name": "Execute Maestro 190",
            "type": "n8n-nodes-base.executeWorkflow",
            "typeVersion": 1,
            "position": [400, 0]
        }
    ],
    "connections": {
        "Webhook Recebe FormData": {"main": [[{"node": "Transforma em Contrato JSON", "type": "main", "index": 0}]]},
        "Transforma em Contrato JSON": {"main": [[{"node": "Execute Maestro 190", "type": "main", "index": 0}]]}
    },
    "active": False,
    "settings": {}
}

# 190 MAESTRO (Draft ilustrando a orquestração via JSON contrato)
wf_190 = {
    "name": "190_MAESTRO_ORQUESTRADOR_ORCAMENTO",
    "nodes": [
        {
            "parameters": {"httpMethod": "POST", "path": "maestro-orcamento"},
            "id": "trigger",
            "name": "Webhook Maestro",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [0, 0]
        },
        {
            "parameters": {"jsCode": "return {json: { orcamento_id: $json.payload_normalizado.orcamento_id, payload_normalizado: $json.payload_normalizado, contexto_dl: {}, resultado_anterior: {} }};"},
            "id": "init_contract",
            "name": "Inicializa Contrato",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [200, 0]
        },
        {
            "parameters": {"workflowId": "ID_201"},
            "id": "exec_201",
            "name": "Executa 201_CLASSIFICADOR",
            "type": "n8n-nodes-base.executeWorkflow",
            "typeVersion": 1,
            "position": [400, 0]
        }
    ],
    "connections": {
        "Webhook Maestro": {"main": [[{"node": "Inicializa Contrato", "type": "main", "index": 0}]]},
        "Inicializa Contrato": {"main": [[{"node": "Executa 201_CLASSIFICADOR", "type": "main", "index": 0}]]}
    },
    "active": False,
    "settings": {}
}

deepseek = "https://api.deepseek.com/chat/completions"
gemini = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"

# Agentes
wf_201 = cria_workflow_agente("201", "CLASSIFICADOR_ORCAMENTO", deepseek, "deepseek-chat", "Você é o Agente Classificador. Leia o payload_normalizado. Defina a linha_confirmada, categoria_confirmada e a complexidade do orçamento. Retorne JSON estruturado.")
wf_202 = cria_workflow_agente("202", "AGENTE_TECNICO_RESPONSAVEL", deepseek, "deepseek-chat", "Você é o Agente Técnico Responsável. Analise o payload e as informações técnicas. Forneça análise técnica, riscos operacionais, recomendação técnica e aponte NBRs aplicáveis.")
wf_203 = cria_workflow_agente("203", "AGENTE_MATERIAIS_CUSTOS", gemini, "", "Você é o Agente de Materiais e Custos. Liste materiais, quantidades e pesquise estimativas de custo.")
wf_204 = cria_workflow_agente("204", "AGENTE_INTELIGENCIA_COMERCIAL", gemini, "", "Você é o Agente de Inteligência Comercial. Com base no serviço, pesquise no mercado do Rio de Janeiro a faixa de preço praticada. Posicione o orçamento da DL com base nos diferenciais (garantia, contrato DL Partner).")
wf_205 = cria_workflow_agente("205", "AGENTE_RISCO_CONTRATUAL", deepseek, "deepseek-chat", "Você é o Agente de Risco Contratual. Analise os riscos operacionais da execução. Sugira cláusulas comerciais de proteção (ex: exclusão de danos pré-existentes) e condições de pagamento seguras.")
wf_206 = cria_workflow_agente("206", "AGENTE_REDATOR_PROPOSTA_LAUDO", deepseek, "deepseek-chat", "Você é o Agente Redator. Receba todos os resultados anteriores. Escreva dois textos em Markdown: 1. Proposta Cliente (sem custos internos, com logomarcas DL/ABESE/CREA-RJ). 2. Laudo Interno (com todos os custos e riscos).")
wf_207 = cria_workflow_agente("207", "AGENTE_CONFERISTA_KILLCRITIC", deepseek, "deepseek-chat", "Você é o Agente Conferista (KillCritic). Audite a coerência de todos os dados do orçamento. Calcule o score_confianca (0 a 100). Aprove ou rejeite a proposta caso tenha margem negativa, riscos não mitigados ou erros técnicos.")

# 208 ENTREGA
wf_208 = {
    "name": "208_ENTREGA_TELEGRAM_EMAIL_SUPABASE",
    "nodes": [
        {
            "parameters": {"httpMethod": "POST", "path": "entrega-orcamento"},
            "id": "trigger",
            "name": "Webhook Entrega",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [0, 0]
        },
        {
            "parameters": {
                "chatId": "-1002012015091",
                "text": "={{ \"🟢 *ORÇAMENTO APROVADO PELO KILLCRITIC*\\n\\nID: \" + $json.orcamento_id + \"\\nScore: \" + $json.score_confianca }}",
                "additionalFields": {"parse_mode": "Markdown"}
            },
            "id": "telegram",
            "name": "Telegram Notificacao",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [200, 0]
        }
    ],
    "connections": {
        "Webhook Entrega": {"main": [[{"node": "Telegram Notificacao", "type": "main", "index": 0}]]}
    },
    "active": False,
    "settings": {}
}

# Salvar todos
salvar_workflow("189_NORMALIZADOR_PAYLOAD_ORCAMENTO.json", wf_189)
salvar_workflow("190_MAESTRO_ORQUESTRADOR_ORCAMENTO.json", wf_190)
salvar_workflow("201_CLASSIFICADOR_ORCAMENTO.json", wf_201)
salvar_workflow("202_AGENTE_TECNICO_RESPONSAVEL.json", wf_202)
salvar_workflow("203_AGENTE_MATERIAIS_CUSTOS.json", wf_203)
salvar_workflow("204_AGENTE_INTELIGENCIA_COMERCIAL.json", wf_204)
salvar_workflow("205_AGENTE_RISCO_CONTRATUAL.json", wf_205)
salvar_workflow("206_AGENTE_REDATOR_PROPOSTA_LAUDO.json", wf_206)
salvar_workflow("207_AGENTE_CONFERISTA_KILLCRITIC.json", wf_207)
salvar_workflow("208_ENTREGA_TELEGRAM_EMAIL_SUPABASE.json", wf_208)
