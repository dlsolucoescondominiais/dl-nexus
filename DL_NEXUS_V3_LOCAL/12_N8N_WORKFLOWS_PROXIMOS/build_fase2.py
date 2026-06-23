import json
import os

workflows_dir = r"d:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS"

def write_wf(name, nodes, connections):
    data = {
        "name": name,
        "nodes": nodes,
        "connections": connections,
        "settings": {"callerPolicy": "workflowsFromSameOwner"},
        "active": False
    }
    with open(os.path.join(workflows_dir, f"{name}.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ================================
# 051 - MEMORIA SUPABASE
# ================================
nodes_051 = [
    {"parameters": {}, "id": "trigger", "name": "Execute Workflow Trigger", "type": "n8n-nodes-base.executeWorkflowTrigger", "typeVersion": 1, "position": [0, 0]},
    {
      "parameters": {
        "url": "=https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_conversas?canal_origem=eq.{{ $json.canal_origem }}&sender_id=eq.{{ $json.sender_id }}&limit=1",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]},
      },
      "id": "p6", "name": "BUSCAR_CONVERSA", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [200, 0],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}},
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "jsCode": "const evento = $('Execute Workflow Trigger').first().json;\nconst buscaResult = $input.item.json;\nlet conversa = null;\nlet isNova = true;\nlet historico_resumido = 'Primeira mensagem da conversa.';\nlet dados_coletados = {};\nlet etapa_funil = 'recepcao';\nif (Array.isArray(buscaResult) && buscaResult.length > 0) {\n  conversa = buscaResult[0];\n  isNova = false;\n  etapa_funil = conversa.etapa_funil || 'recepcao';\n  dados_coletados = conversa.dados_coletados || {};\n} else if (buscaResult && buscaResult.id) {\n  conversa = buscaResult;\n  isNova = false;\n  etapa_funil = conversa.etapa_funil || 'recepcao';\n  dados_coletados = conversa.dados_coletados || {};\n}\nreturn [{ json: {\n  ...evento,\n  conversa_id: conversa ? conversa.id : null,\n  conversa_existente: !isNova,\n  etapa_funil,\n  dados_coletados,\n  historico_resumido,\n  ultimo_resumo: conversa ? conversa.ultimo_resumo : null\n}}];"
      },
      "id": "p7", "name": "PROCESSAR_CONVERSA", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [400, 0]
    },
    {
      "parameters": {
        "conditions": {"boolean": [{"value1": "={{ $json.conversa_existente === false }}", "value2": True}]}
      },
      "id": "p8", "name": "IF_CONVERSA_NOVA", "type": "n8n-nodes-base.if", "typeVersion": 1, "position": [600, 0]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_conversas",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}, {"name": "Prefer", "value": "return=representation"}]},
        "sendBody": True,
        "bodyParameters": {"parameters": [{"name": "canal_origem", "value": "={{ $json.canal_origem }}"}, {"name": "sender_id", "value": "={{ $json.sender_id }}"}, {"name": "status_conversa", "value": "ativa"}, {"name": "dry_run", "value": "={{ $json.dry_run }}"}]}
      },
      "id": "p9", "name": "CRIAR_CONVERSA_SUPABASE", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [800, -100],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}}
    },
    {
      "parameters": {
        "jsCode": "const evento = $node['PROCESSAR_CONVERSA'].json;\nconst novaConversa = $input.item.json;\nconst conversaId = Array.isArray(novaConversa) ? novaConversa[0]?.id : novaConversa?.id;\nreturn [{ json: { ...evento, conversa_id: conversaId || null, conversa_existente: true } }];"
      },
      "id": "p10", "name": "ATRIBUIR_CONVERSA_ID", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1000, -100]
    },
    {
      "parameters": {
        "method": "POST",
        "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_mensagens",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]},
        "sendBody": True,
        "bodyParameters": {"parameters": [{"name": "conversa_id", "value": "={{ $json.conversa_id }}"}, {"name": "canal_origem", "value": "={{ $json.canal_origem }}"}, {"name": "message_id", "value": "={{ $json.message_id }}"}, {"name": "direction", "value": "inbound"}, {"name": "texto", "value": "={{ $json.texto_mensagem }}"}, {"name": "dry_run", "value": "={{ $json.dry_run }}"}]}
      },
      "id": "p15", "name": "REGISTRAR_INBOUND", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [1200, 100],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}}
    },
    {
      "parameters": {
        "url": "=https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_mensagens?conversa_id=eq.{{ $json.conversa_id }}&order=created_at.desc&limit=10",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]}
      },
      "id": "p11", "name": "CARREGAR_HISTORICO", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [1400, 0],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}},
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {"jsCode": "const hist = $input.item.json;\nconst ev = $('PROCESSAR_CONVERSA').first().json;\nlet h_texto = '';\nif (Array.isArray(hist) && hist.length > 0) {\n  h_texto = hist.map(m => (m.direction==='inbound'?'Lead: ':'Aninha: ') + (m.texto||'')).reverse().join('\\n');\n}\nreturn [{json: { ...ev, historico: h_texto }}];"},
      "id": "p_hist", "name": "CONSOLIDAR_OUTPUT", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1600, 0]
    }
]
connections_051 = {
    "Execute Workflow Trigger": {"main": [[{"node": "BUSCAR_CONVERSA", "type": "main", "index": 0}]]},
    "BUSCAR_CONVERSA": {"main": [[{"node": "PROCESSAR_CONVERSA", "type": "main", "index": 0}]]},
    "PROCESSAR_CONVERSA": {"main": [[{"node": "IF_CONVERSA_NOVA", "type": "main", "index": 0}]]},
    "IF_CONVERSA_NOVA": {"main": [[{"node": "CRIAR_CONVERSA_SUPABASE", "type": "main", "index": 0}], [{"node": "REGISTRAR_INBOUND", "type": "main", "index": 0}]]},
    "CRIAR_CONVERSA_SUPABASE": {"main": [[{"node": "ATRIBUIR_CONVERSA_ID", "type": "main", "index": 0}]]},
    "ATRIBUIR_CONVERSA_ID": {"main": [[{"node": "REGISTRAR_INBOUND", "type": "main", "index": 0}]]},
    "REGISTRAR_INBOUND": {"main": [[{"node": "CARREGAR_HISTORICO", "type": "main", "index": 0}]]},
    "CARREGAR_HISTORICO": {"main": [[{"node": "CONSOLIDAR_OUTPUT", "type": "main", "index": 0}]]}
}
write_wf("051_ANINHA_SOCIAL_MEMORIA_SUPABASE", nodes_051, connections_051)

# ================================
# 052 - RESPOSTA META
# ================================
nodes_052 = [
    {"parameters": {}, "id": "trigger", "name": "Execute Workflow Trigger", "type": "n8n-nodes-base.executeWorkflowTrigger", "typeVersion": 1, "position": [0, 0]},
    {
      "parameters": {
        "method": "POST",
        "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_mensagens",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]},
        "sendBody": True,
        "bodyParameters": {"parameters": [{"name": "conversa_id", "value": "={{ $json.conversa_id }}"}, {"name": "canal_origem", "value": "={{ $json.canal_origem }}"}, {"name": "message_id", "value": "=resp_{{ $json.message_id }}"}, {"name": "direction", "value": "outbound"}, {"name": "texto", "value": "={{ $json.texto_resposta }}"}, {"name": "dry_run", "value": "={{ $json.dry_run }}"}]}
      },
      "id": "p16", "name": "REGISTRAR_OUTBOUND", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [200, 0],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}}
    },
    {
      "parameters": {"conditions": {"boolean": [{"value1": "={{ $json.dry_run === false }}", "value2": True}]}},
      "id": "p17", "name": "IF_ENVIO_REAL", "type": "n8n-nodes-base.if", "typeVersion": 1, "position": [400, 0]
    },
    {
      "parameters": {"chatId": "={{ $env['TELEGRAM_DIOGO_CHAT_ID'] }}", "text": "=DRY_RUN: Resposta Meta SDR ({{ $json.canal_origem }}):\n\nPara: {{ $json.sender_id }}\nMensagem:\n\"{{ $json.texto_resposta }}\""},
      "id": "p18", "name": "ALERTA_TELEGRAM_DRY_RUN", "type": "n8n-nodes-base.telegram", "typeVersion": 1, "position": [600, 100],
      "credentials": {"telegramApi": {"id": "4sGUaygxQklSMa3Z", "name": "Aninha Telegram Bot (DL Nexus)"}}
    }
]
connections_052 = {
    "Execute Workflow Trigger": {"main": [[{"node": "REGISTRAR_OUTBOUND", "type": "main", "index": 0}]]},
    "REGISTRAR_OUTBOUND": {"main": [[{"node": "IF_ENVIO_REAL", "type": "main", "index": 0}]]},
    "IF_ENVIO_REAL": {"main": [[], [{"node": "ALERTA_TELEGRAM_DRY_RUN", "type": "main", "index": 0}]]}
}
write_wf("052_ANINHA_SOCIAL_RESPOSTA_META", nodes_052, connections_052)

# ================================
# 053 - HANDOFF TELEGRAM
# ================================
nodes_053 = [
    {"parameters": {}, "id": "trigger", "name": "Execute Workflow Trigger", "type": "n8n-nodes-base.executeWorkflowTrigger", "typeVersion": 1, "position": [0, 0]},
    {
      "parameters": {"chatId": "={{ $env['TELEGRAM_DIOGO_CHAT_ID'] }}", "text": "=🔔 [HANDOFF SDR SOCIAL]\n\nCanal: {{ $json.canal_origem }}\nLead ID: {{ $json.sender_id }}\n\nMotivo: {{ $json.motivo_humano }}\n\nHistórico:\n{{ $json.historico }}"},
      "id": "t1", "name": "ENVIAR_TELEGRAM_HANDOFF", "type": "n8n-nodes-base.telegram", "typeVersion": 1, "position": [200, 0],
      "credentials": {"telegramApi": {"id": "4sGUaygxQklSMa3Z", "name": "Aninha Telegram Bot (DL Nexus)"}},
      "onError": "continueRegularOutput"
    },
    {
      "parameters": {
        "method": "PATCH",
        "url": "=https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_conversas?id=eq.{{ $json.conversa_id }}",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth",
        "sendHeaders": True,
        "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]},
        "sendBody": True,
        "bodyParameters": {"parameters": [{"name": "precisa_humano", "value": True}, {"name": "etapa_funil", "value": "handoff"}]}
      },
      "id": "t2", "name": "ATUALIZAR_CONVERSA", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [400, 0],
      "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}}
    }
]
connections_053 = {
    "Execute Workflow Trigger": {"main": [[{"node": "ENVIAR_TELEGRAM_HANDOFF", "type": "main", "index": 0}]]},
    "ENVIAR_TELEGRAM_HANDOFF": {"main": [[{"node": "ATUALIZAR_CONVERSA", "type": "main", "index": 0}]]}
}
write_wf("053_ANINHA_SOCIAL_HANDOFF_TELEGRAM", nodes_053, connections_053)

# ================================
# 054 - RELATORIO DIARIO
# ================================
nodes_054 = [
    {"parameters": {}, "id": "trigger", "name": "Cron", "type": "n8n-nodes-base.cron", "typeVersion": 1, "position": [0, 0]},
    {"parameters": {"chatId": "={{ $env['TELEGRAM_DIOGO_CHAT_ID'] }}", "text": "📊 Relatório SDR Social Diário (Placeholder Fase 2)\n\nO motor 050 processou interações nas últimas 24h."}, "id": "r1", "name": "ENVIAR_RELATORIO", "type": "n8n-nodes-base.telegram", "typeVersion": 1, "position": [200, 0], "credentials": {"telegramApi": {"id": "4sGUaygxQklSMa3Z", "name": "Aninha Telegram Bot (DL Nexus)"}}}
]
connections_054 = {"Cron": {"main": [[{"node": "ENVIAR_RELATORIO", "type": "main", "index": 0}]]}}
write_wf("054_ANINHA_SOCIAL_RELATORIO_DIARIO", nodes_054, connections_054)

# ================================
# 050 - AGENTE MESTRE
# ================================
nodes_050 = [
    {"parameters": {"httpMethod": "GET", "path": "meta-social-sdr-dl", "responseMode": "responseNode"}, "id": "e1", "name": "Webhook_GET_Verify", "type": "n8n-nodes-base.webhook", "typeVersion": 2, "position": [0, -200], "webhookId": "meta-social-sdr-dl-verify"},
    {"parameters": {"jsCode": "const query = $input.item.json.query || {};\nconst token = query['hub.verify_token'];\nconst challenge = query['hub.challenge'];\nif (token === 'dl_sdr_social_2026_verify') return [{ json: { challenge: String(challenge) } }];\nreturn [];"}, "id": "e2", "name": "VERIFICAR_TOKEN", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [200, -200]},
    {"parameters": {"respondWith": "text", "responseBody": "={{ $json.challenge }}"}, "id": "e3", "name": "Responder_Challenge", "type": "n8n-nodes-base.respondToWebhook", "typeVersion": 1, "position": [400, -200]},
    {"parameters": {"httpMethod": "POST", "path": "meta-social-sdr-dl", "responseMode": "onReceived"}, "id": "p1", "name": "Webhook_POST_Events", "type": "n8n-nodes-base.webhook", "typeVersion": 2, "position": [0, 0], "webhookId": "meta-social-sdr-dl-events"},
    {"parameters": {"jsCode": "const body = $input.item.json.body || $input.item.json;\nconst entries = body.entry || [];\nconst results = [];\nfor (const entry of entries) {\n  const messaging = entry.messaging || [];\n  const objectType = body.object;\n  for (const event of messaging) {\n    const isInstagram = objectType === 'instagram';\n    const canal_origem = isInstagram ? 'instagram_direct' : 'facebook_messenger';\n    const sender_id = String(event.sender?.id || '');\n    const message = event.message || {};\n    if (message.is_echo || !message.text) continue;\n    results.push({ json: {\n      canal_origem, sender_id,\n      message_id: message.mid,\n      texto_mensagem: message.text,\n      dry_run: true\n    }});\n  }\n}\nreturn results;"}, "id": "p2", "name": "NORMALIZAR_EVENTO", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [200, 0]},
    {"parameters": {"url": "=https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/dl_social_mensagens?canal_origem=eq.{{ $json.canal_origem }}&message_id=eq.{{ $json.message_id }}&limit=1", "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth", "sendHeaders": True, "headerParameters": {"parameters": [{"name": "apikey", "value": "={{ $env['SUPABASE_ANON_KEY'] }}"}]}}, "id": "p3", "name": "VERIFICAR_DUPLICATA", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [400, 0], "credentials": {"httpHeaderAuth": {"id": "supabase_anon_key", "name": "Supabase Anon Key"}}, "onError": "continueRegularOutput"},
    {"parameters": {"conditions": {"boolean": [{"value1": "={{ $json.length === 0 || !$json.id }}", "value2": True}]}}, "id": "p4", "name": "IF_NOVA_MENSAGEM", "type": "n8n-nodes-base.if", "typeVersion": 1, "position": [600, 0]},
    {"parameters": {"workflowId": "051_ANINHA_SOCIAL_MEMORIA_SUPABASE"}, "id": "p5", "name": "CALL_051_MEMORIA", "type": "n8n-nodes-base.executeWorkflow", "typeVersion": 1, "position": [800, 0]},
    {"parameters": {"jsCode": "const ev = $input.item.json;\nconst prompt = `Você é Aninha, assistente de atendimento institucional da DL Soluções Condominiais.\nVocê atende leads corporativos.\nRestrições:\n- NUNCA use 'visita técnica'. Use 'Avaliação Técnica'.\n- NUNCA use 'Condfy' ou 'DL Ignis'. Use 'DL Alerta — prevenção de incêndio'.\n- NUNCA use 'B2B'. Fale 'atendimento institucional/corporativo'.\n- A DL não atende residências comuns (CPF).\n\nSe o cliente não for residencial, atenda cordialmente.\nSe o cliente quiser suporte fora do escopo, ou se irritar, inicie a resposta com [HANDOFF] para passar a um humano.\n\nHistórico:\n${ev.historico}\n\nMensagem lead: ${ev.texto_mensagem}\n\nResponda como Aninha:`;\nreturn [{json: {...ev, prompt}}];"}, "id": "p6", "name": "MONTAR_PROMPT", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1000, 0]},
    {"parameters": {"method": "POST", "url": "=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={{ $env['GEMINI_API_KEY_MOTOR'] }}", "sendHeaders": True, "headerParameters": {"parameters": [{"name": "Content-Type", "value": "application/json"}]}, "sendBody": True, "bodyParameters": {"parameters": [{"name": "contents", "value": "={{ [ { \"parts\": [ {\"text\": $json.prompt} ] } ] }}"}]}}, "id": "p7", "name": "CHAMAR_GEMINI", "type": "n8n-nodes-base.httpRequest", "typeVersion": 4, "position": [1200, 0]},
    {"parameters": {"jsCode": "const ev = $node['MONTAR_PROMPT'].json;\nconst resp = $input.item.json.candidates?.[0]?.content?.parts?.[0]?.text || '';\nconst isHandoff = resp.includes('[HANDOFF]');\nconst texto_resposta = resp.replace('[HANDOFF]', '').trim();\nreturn [{json: {...ev, texto_resposta, isHandoff, motivo_humano: isHandoff ? 'Handoff acionado pela IA' : ''}}];"}, "id": "p8", "name": "PROCESSAR_RESPOSTA", "type": "n8n-nodes-base.code", "typeVersion": 2, "position": [1400, 0]},
    {"parameters": {"conditions": {"boolean": [{"value1": "={{ $json.isHandoff }}", "value2": True}]}}, "id": "p9", "name": "IF_HANDOFF", "type": "n8n-nodes-base.if", "typeVersion": 1, "position": [1600, 0]},
    {"parameters": {"workflowId": "053_ANINHA_SOCIAL_HANDOFF_TELEGRAM"}, "id": "p10", "name": "CALL_053_HANDOFF", "type": "n8n-nodes-base.executeWorkflow", "typeVersion": 1, "position": [1800, -100]},
    {"parameters": {"workflowId": "052_ANINHA_SOCIAL_RESPOSTA_META"}, "id": "p11", "name": "CALL_052_RESPOSTA", "type": "n8n-nodes-base.executeWorkflow", "typeVersion": 1, "position": [1800, 100]}
]
connections_050 = {
    "Webhook_GET_Verify": {"main": [[{"node": "VERIFICAR_TOKEN", "type": "main", "index": 0}]]},
    "VERIFICAR_TOKEN": {"main": [[{"node": "Responder_Challenge", "type": "main", "index": 0}]]},
    "Webhook_POST_Events": {"main": [[{"node": "NORMALIZAR_EVENTO", "type": "main", "index": 0}]]},
    "NORMALIZAR_EVENTO": {"main": [[{"node": "VERIFICAR_DUPLICATA", "type": "main", "index": 0}]]},
    "VERIFICAR_DUPLICATA": {"main": [[{"node": "IF_NOVA_MENSAGEM", "type": "main", "index": 0}]]},
    "IF_NOVA_MENSAGEM": {"main": [[{"node": "CALL_051_MEMORIA", "type": "main", "index": 0}], []]},
    "CALL_051_MEMORIA": {"main": [[{"node": "MONTAR_PROMPT", "type": "main", "index": 0}]]},
    "MONTAR_PROMPT": {"main": [[{"node": "CHAMAR_GEMINI", "type": "main", "index": 0}]]},
    "CHAMAR_GEMINI": {"main": [[{"node": "PROCESSAR_RESPOSTA", "type": "main", "index": 0}]]},
    "PROCESSAR_RESPOSTA": {"main": [[{"node": "IF_HANDOFF", "type": "main", "index": 0}]]},
    "IF_HANDOFF": {"main": [[{"node": "CALL_053_HANDOFF", "type": "main", "index": 0}], [{"node": "CALL_052_RESPOSTA", "type": "main", "index": 0}]]}
}
write_wf("050_AGENTE_SDR_SOCIAL_DL", nodes_050, connections_050)

print("Workflows JSON files successfully built for Fase 2.")
