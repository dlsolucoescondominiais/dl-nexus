"""
[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.
Este script foi desativado.
"""
import sys
sys.exit("Script obsoleto. Manus.IA foi removido.")

import json
import os

# ──────────────────────────────────────────────────────────────────────
# 070_CRON_MANUS_DIARIO — Reconstruído sobre api.manus.ai/v2
# PRESERVA: x-manus-api-key, task.create, task.detail, task.listMessages
# PRESERVA: structured_output_schema, agent_profile manus-1.6-lite
# NÃO ALTERA: chave Manus, credenciais, Aninha, Supabase, CRM, outros wf
# ──────────────────────────────────────────────────────────────────────

structured_output_schema = {
    "type": "object",
    "properties": {
        "estrategia_texto": {"type": "string", "description": "Descreva o gancho, a dor do público e o tom que o MarkSolar deve usar no post."},
        "produto": {"type": "string", "description": "Nome do produto foco"},
        "publico_alvo": {"type": "string", "description": "Ex: Síndicos de pequenos condomínios"},
        "bairro": {"type": "string", "description": "Ex: Zona Sul, Barra ou Tijuca"},
        "canal_destino": {"type": "string", "description": "Instagram, Facebook e TikTok"},
        "objetivo": {"type": "string", "description": "Agendar Avaliação Técnica"}
    },
    "required": ["estrategia_texto", "produto", "publico_alvo", "bairro", "canal_destino", "objetivo"]
}

# ──────────────────────────────────────────────────────────────────────
# PROMPT DIÁRIO (Code Node)
# ──────────────────────────────────────────────────────────────────────
prompt_js = r"""const d = new Date().toLocaleDateString("pt-BR");

const prompt = `Você é Manus AI, o Diretor de Marketing B2B da DL Soluções Condominiais.
Hoje é dia ${d}. Pense em condomínios pequenos/médios, colégios e restaurantes no Rio de Janeiro.

Produtos da DL:
- DL Guardião: segurança eletrônica, CFTV, câmeras, proteção patrimonial
- Fortress: portaria autônoma, gestão de acesso
- Gatekeeper: automação de portões
- DL Acqua: cisternas, caixas d'água, bombas, automação hídrica
- DL Volt: elétrica condominial, quadros, painéis, infraestrutura elétrica
- DL EcoVolt: energia solar on-grid, híbrida, off-grid
- DL Alerta: prevenção de incêndio, centrais, detectores
- DL Partner: manutenção continuada Basic/Master/Premium
- Mult•Grill Express: chapas, fritadeiras, gastronomia comercial

REGRAS ABSOLUTAS:
- Nunca usar "visita técnica". Usar "Avaliação Técnica".
- Nunca citar Condfy.
- Nunca chamar Diogo de engenheiro. Usar "Tecnólogo Responsável".
- CTA principal: https://dlsolucoescondominiais.com
- CTA WhatsApp: https://wa.me/5521964742458

Gere a estratégia do dia de postagem para o Agente MarkSolar (Copywriter).
Retorne JSON com: estrategia_texto, produto, publico_alvo, bairro, canal_destino, objetivo.`;

return { json: { prompt: prompt } };"""

# ──────────────────────────────────────────────────────────────────────
# EXTRACT TASK ID (Code Node)
# ──────────────────────────────────────────────────────────────────────
extract_task_id_js = r"""const task = $json.task || $json.data || $json;
const task_id = task.task_id || task.id || $json.task_id || $json.id;

if (!task_id) {
  throw new Error("Manus não retornou task_id. Verificar payload ou endpoint task.create.");
}

return {
  json: {
    task_id: task_id,
    attempt: 0,
    max_attempts: 30
  }
};"""

# ──────────────────────────────────────────────────────────────────────
# NORMALIZE STATUS (Code Node)
# ──────────────────────────────────────────────────────────────────────
normalize_status_js = r"""const task = $json.task || $json.data || $json;
const status = String(task.status || $json.status || '').toLowerCase();

const doneStatuses = ['stopped', 'completed', 'succeeded', 'success', 'finished', 'waiting'];
const errorStatuses = ['failed', 'error', 'cancelled', 'timeout'];
const runningStatuses = ['running', 'pending', 'queued', 'processing', 'created'];

return {
  json: {
    task_id: task.id || task.task_id || $json.task_id,
    status,
    is_done: doneStatuses.includes(status),
    is_error: errorStatuses.includes(status),
    is_running: runningStatuses.includes(status),
    attempt: $json.attempt || 0,
    max_attempts: $json.max_attempts || 30
  }
};"""

# ──────────────────────────────────────────────────────────────────────
# INCREMENT ATTEMPT (Code Node — false branch of IF)
# ──────────────────────────────────────────────────────────────────────
increment_attempt_js = r"""const attempt = ($json.attempt || 0) + 1;
const max_attempts = $json.max_attempts || 30;

if (attempt >= max_attempts) {
  throw new Error("Timeout Manus: tarefa não concluiu em 15 minutos (" + max_attempts + " tentativas x 30s).");
}

return {
  json: {
    task_id: $json.task_id,
    attempt: attempt,
    max_attempts: max_attempts
  }
};"""

# ──────────────────────────────────────────────────────────────────────
# LIMPAR JSON DO MANUS (Code Node — from task.listMessages)
# ──────────────────────────────────────────────────────────────────────
limpar_json_js = r"""const events = $input.all()[0].json.data || [];

// 1. Buscar structured_output_result
const resultEvent = events.find(e => e.type === 'structured_output_result');

if (
  resultEvent &&
  resultEvent.structured_output_result &&
  resultEvent.structured_output_result.success
) {
  const value = resultEvent.structured_output_result.value;

  if (typeof value === 'string') {
    return { json: JSON.parse(value) };
  }

  return { json: value };
}

// 2. Fallback: buscar assistant_message com JSON
const assistantEvent = events.find(e =>
  e.type === 'assistant_message' &&
  e.assistant_message &&
  e.assistant_message.content
);

if (assistantEvent) {
  const content = assistantEvent.assistant_message.content;
  const match = content.match(/\{[\s\S]*\}/);

  if (match) {
    const parsed = JSON.parse(match[0]);

    if (!parsed.estrategia_texto || !parsed.produto) {
      throw new Error('JSON do Manus incompleto.');
    }

    return { json: parsed };
  }
}

throw new Error('Resultado estruturado do Manus não encontrado em task.listMessages.');"""

# ──────────────────────────────────────────────────────────────────────
# BUILD THE WORKFLOW JSON
# ──────────────────────────────────────────────────────────────────────
wf = {
    "name": "070_CRON_MANUS_DIARIO",
    "active": False,
    "nodes": [
        # 1. Schedule Trigger
        {
            "parameters": {
                "rule": {
                    "interval": [{"field": "cronExpression", "expression": "35 0 * * *"}]
                }
            },
            "id": "trigger_cron",
            "name": "Schedule Trigger (00:35)",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1,
            "position": [0, 0]
        },
        # 2. Preparar Prompt Diário
        {
            "parameters": {"jsCode": prompt_js},
            "id": "prepare_prompt",
            "name": "Preparar Prompt Diário",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [220, 0]
        },
        # 3. HTTP Request Manus API — task.create
        {
            "parameters": {
                "method": "POST",
                "url": "https://api.manus.ai/v2/task.create",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "x-manus-api-key", "value": "={{$env.MANUS_API_KEY}}"},
                        {"name": "Content-Type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "specifyBody": "json",
                "jsonBody": json.dumps({
                    "prompt": "={{$json.prompt}}",
                    "agent_profile": "manus-1.6-lite",
                    "interactive_mode": False,
                    "structured_output_schema": structured_output_schema
                }, ensure_ascii=False),
                "options": {
                    "response": {"response": {"responseFormat": "json"}}
                }
            },
            "id": "api_manus_create",
            "name": "HTTP Request Manus API",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [440, 0]
        },
        # 4. Extract Task ID
        {
            "parameters": {"jsCode": extract_task_id_js},
            "id": "extract_task_id",
            "name": "Extrair Task ID",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [660, 0]
        },
        # 5. Wait 30s (first wait before first status check)
        {
            "parameters": {"amount": 30, "unit": "seconds"},
            "id": "wait_initial",
            "name": "Wait 30s Inicial",
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [880, 0]
        },
        # 6. Check Task Status — task.detail
        {
            "parameters": {
                "method": "GET",
                "url": "=https://api.manus.ai/v2/task.detail?task_id={{$json.task_id}}",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "x-manus-api-key", "value": "={{$env.MANUS_API_KEY}}"}
                    ]
                },
                "options": {
                    "response": {"response": {"responseFormat": "json"}}
                }
            },
            "id": "check_task_status",
            "name": "Check Task Status",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [1100, 0]
        },
        # 7. Normalize Status
        {
            "parameters": {"jsCode": normalize_status_js},
            "id": "normalize_status",
            "name": "Normalizar Status",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1320, 0]
        },
        # 8. IF Manus concluído?
        {
            "parameters": {
                "conditions": {
                    "boolean": [{"value1": "={{$json.is_done}}", "value2": True}]
                }
            },
            "id": "if_done",
            "name": "IF Manus concluído?",
            "type": "n8n-nodes-base.if",
            "typeVersion": 1,
            "position": [1540, 0]
        },
        # 9. Incrementar Tentativa (false branch — not done yet)
        {
            "parameters": {"jsCode": increment_attempt_js},
            "id": "increment_attempt",
            "name": "Incrementar Tentativa",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1540, 250]
        },
        # 10. Wait 30s (loop wait)
        {
            "parameters": {"amount": 30, "unit": "seconds"},
            "id": "wait_loop",
            "name": "Wait 30s",
            "type": "n8n-nodes-base.wait",
            "typeVersion": 1,
            "position": [1320, 250]
        },
        # 11. Get Final Messages — task.listMessages (true branch — done)
        {
            "parameters": {
                "method": "GET",
                "url": "=https://api.manus.ai/v2/task.listMessages?task_id={{$json.task_id}}",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "x-manus-api-key", "value": "={{$env.MANUS_API_KEY}}"}
                    ]
                },
                "options": {
                    "response": {"response": {"responseFormat": "json"}}
                }
            },
            "id": "get_messages",
            "name": "Get Final Messages",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.1,
            "position": [1760, 0]
        },
        # 12. Limpar JSON do Manus
        {
            "parameters": {"jsCode": limpar_json_js},
            "id": "clean_json",
            "name": "Limpar JSON do Manus",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1980, 0]
        },
        # 13. Chamar MarkSolar (020)
        {
            "parameters": {
                "workflowId": "publicadorSocialDlNexusV320260518"
            },
            "id": "call_marksolar",
            "name": "Chamar MarkSolar (020)",
            "type": "n8n-nodes-base.executeWorkflow",
            "typeVersion": 1,
            "position": [2200, 0]
        },
        # 14. Telegram Entrega (notificação apenas, continueOnFail)
        {
            "parameters": {
                "chatId": "-1002012015091",
                "text": "={{ \"🎯 DIRETRIZ MANUS B2B\\n\\nPúblico: \" + $json.publico_alvo + \"\\nProduto: \" + $json.produto + \"\\nRegião: \" + $json.bairro + \"\\nEstratégia: \" + $json.estrategia_texto }}",
                "additionalFields": {"parse_mode": "Markdown"}
            },
            "id": "telegram_entrega",
            "name": "Telegram Entrega",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [2420, 0],
            "continueOnFail": True
        }
    ],
    "connections": {
        "Schedule Trigger (00:35)": {
            "main": [[{"node": "Preparar Prompt Diário", "type": "main", "index": 0}]]
        },
        "Preparar Prompt Diário": {
            "main": [[{"node": "HTTP Request Manus API", "type": "main", "index": 0}]]
        },
        "HTTP Request Manus API": {
            "main": [[{"node": "Extrair Task ID", "type": "main", "index": 0}]]
        },
        "Extrair Task ID": {
            "main": [[{"node": "Wait 30s Inicial", "type": "main", "index": 0}]]
        },
        "Wait 30s Inicial": {
            "main": [[{"node": "Check Task Status", "type": "main", "index": 0}]]
        },
        "Check Task Status": {
            "main": [[{"node": "Normalizar Status", "type": "main", "index": 0}]]
        },
        "Normalizar Status": {
            "main": [[{"node": "IF Manus concluído?", "type": "main", "index": 0}]]
        },
        "IF Manus concluído?": {
            "main": [
                [{"node": "Get Final Messages", "type": "main", "index": 0}],
                [{"node": "Incrementar Tentativa", "type": "main", "index": 0}]
            ]
        },
        "Incrementar Tentativa": {
            "main": [[{"node": "Wait 30s", "type": "main", "index": 0}]]
        },
        "Wait 30s": {
            "main": [[{"node": "Check Task Status", "type": "main", "index": 0}]]
        },
        "Get Final Messages": {
            "main": [[{"node": "Limpar JSON do Manus", "type": "main", "index": 0}]]
        },
        "Limpar JSON do Manus": {
            "main": [
                [
                    {"node": "Chamar MarkSolar (020)", "type": "main", "index": 0},
                    {"node": "Telegram Entrega", "type": "main", "index": 0}
                ]
            ]
        }
    },
    "settings": {
        "callerPolicy": "workflowsFromSameOwner",
        "availableInMCP": False
    }
}

# Save to all 3 locations
paths = [
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\070_CRON_MANUS_DIARIO.json',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\09_PRONTOS_PARA_PRODUCAO\070_CRON_MANUS_DIARIO.json'
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    print(f"Salvo: {p}")

# Validate
with open(paths[0], 'r', encoding='utf-8') as f:
    check = json.load(f)
    node_names = [n['name'] for n in check['nodes']]
    print(f"\nNodes ({len(node_names)}):")
    for name in node_names:
        print(f"  - {name}")
    
    # Verify API domain
    for n in check['nodes']:
        if n['type'] == 'n8n-nodes-base.httpRequest':
            url = n['parameters'].get('url', '')
            print(f"\n  HTTP Node: {n['name']}")
            print(f"  URL: {url}")
            hps = n['parameters'].get('headerParameters', {}).get('parameters', [])
            for h in hps:
                hname = h.get('name', '')
                hval = h.get('value', '')
                if 'key' in hname.lower():
                    hval = '***MASKED***'
                print(f"  Header: {hname} = {hval}")

    # Verify no hardcoded secrets
    raw = json.dumps(check)
    if 'sk-' in raw or 'sk_' in raw:
        print("\n⚠️ ALERTA: Possível segredo hardcoded detectado!")
    else:
        print("\n✅ Nenhum segredo hardcoded detectado.")
    
    if 'api.manus.gg' in raw:
        print("⚠️ ALERTA: Referência a api.manus.gg encontrada!")
    else:
        print("✅ Nenhuma referência a api.manus.gg.")
    
    if 'openai.com' in raw:
        print("⚠️ ALERTA: Referência a openai.com encontrada!")
    else:
        print("✅ Nenhuma referência a openai.com.")
    
    if 'x-manus-api-key' in raw:
        print("✅ Header x-manus-api-key presente.")
    else:
        print("⚠️ ALERTA: Header x-manus-api-key NÃO encontrado!")
    
    if 'api.manus.ai/v2' in raw:
        print("✅ Domínio api.manus.ai/v2 presente.")
    else:
        print("⚠️ ALERTA: Domínio api.manus.ai/v2 NÃO encontrado!")

print("\n✅ Workflow 070 reconstruído com sucesso.")
