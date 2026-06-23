import json

workflow = {
  "name": "151_ANINHA_ATENDIMENTO_CRM_DL",
  "nodes": [
    {
      "parameters": {},
      "id": "execute_workflow_trigger",
      "name": "Execute Workflow Trigger",
      "type": "n8n-nodes-base.executeWorkflowTrigger",
      "typeVersion": 1,
      "position": [ 100, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT * FROM dl_aninha_sessions WHERE usuario_id = '{{ $json.usuario_id }}' AND canal = '{{ $json.canal }}';"
      },
      "id": "check_session",
      "name": "Verificar Sessao Aninha",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 300, 300 ],
      "credentials": {
        "database": {
          "id": "supabase_postgres_cred_id",
          "name": "Supabase Connection"
        }
      }
    },
    {
      "parameters": {
        "conditions": {
          "number": [
            { "value1": "={{ $json.id ? 1 : 0 }}", "operation": "equal", "value2": 0 }
          ]
        }
      },
      "id": "if_new_session",
      "name": "Nova Sessao?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 500, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO dl_aninha_sessions (usuario_id, canal, estado_conversa) VALUES ('{{ $('Execute Workflow Trigger').item.json.usuario_id }}', '{{ $('Execute Workflow Trigger').item.json.canal }}', 'coleta_inicial') RETURNING id;"
      },
      "id": "create_session",
      "name": "Criar Sessao Supabase",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 700, 200 ],
      "credentials": {
        "database": {
          "id": "supabase_postgres_cred_id",
          "name": "Supabase Connection"
        }
      }
    },
    {
      "parameters": {
        "model": "gemini-1.5-pro",
        "options": {
          "systemMessage": "Você é a Aninha, atendente B2B da DL Soluções Condominiais. Se apresente e peça de forma clara: Nome, Empresa/Condomínio, Bairro, Serviço Desejado e Urgência. Se o usuário já informou tudo, responda com JSON de qualificação do lead.",
          "temperature": 0.5
        }
      },
      "id": "aninha_agent",
      "name": "Agente Aninha (Gemini)",
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.4,
      "position": [ 900, 300 ],
      "credentials": {
        "googlePalmApi": {
          "id": "gemini_api_cred",
          "name": "Google Gemini API"
        }
      }
    },
    {
      "parameters": {
        "jsCode": """
const ai_reply = $input.item.json.text || $input.item.json.response || '';
let is_qualified = false;
let lead_data = null;

if (ai_reply.includes('{') && ai_reply.includes('}')) {
    try {
        const extracted = JSON.parse(ai_reply.substring(ai_reply.indexOf('{'), ai_reply.lastIndexOf('}') + 1));
        if (extracted.nome && extracted.bairro) {
            is_qualified = true;
            lead_data = extracted;
        }
    } catch(e) {}
}

return [{
  json: {
    reply: ai_reply,
    is_qualified,
    lead_data
  }
}];
"""
      },
      "id": "process_reply",
      "name": "Processar Resposta e Lead",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 1100, 300 ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            { "value1": "={{ $json.is_qualified }}", "value2": True }
          ]
        }
      },
      "id": "if_qualified",
      "name": "Lead Qualificado?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 1300, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO dl_leads (nome, telefone, empresa_condominio, bairro, servico, urgencia, status) VALUES ('{{ $json.lead_data.nome }}', '{{ $json.lead_data.telefone || '' }}', '{{ $json.lead_data.empresa_condominio || '' }}', '{{ $json.lead_data.bairro }}', '{{ $json.lead_data.servico || '' }}', '{{ $json.lead_data.urgencia || '' }}', 'qualificado') RETURNING id;"
      },
      "id": "create_lead",
      "name": "Cadastrar Lead (CRM)",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 1500, 200 ],
      "credentials": {
        "database": {
          "id": "supabase_postgres_cred_id",
          "name": "Supabase Connection"
        }
      }
    },
    {
      "parameters": {
        "chatId": "YOUR_TELEGRAM_CHAT_ID",
        "text": "=🚀 *NOVO LEAD QUALIFICADO (SOCIAL)*\n\nNome: {{$json.lead_data.nome}}\nEmpresa/Cond: {{$json.lead_data.empresa_condominio}}\nBairro: {{$json.lead_data.bairro}}\nServiço: {{$json.lead_data.servico}}\nUrgência: {{$json.lead_data.urgencia}}"
      },
      "id": "telegram_alert",
      "name": "Alerta Diogo Telegram",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.1,
      "position": [ 1700, 200 ],
      "credentials": {
        "telegramApi": {
          "id": "telegram_cred_id",
          "name": "Telegram Bot Account"
        }
      }
    }
  ],
  "connections": {
    "Execute Workflow Trigger": {
      "main": [ [ { "node": "Verificar Sessao Aninha", "type": "main", "index": 0 } ] ]
    },
    "Verificar Sessao Aninha": {
      "main": [ [ { "node": "Nova Sessao?", "type": "main", "index": 0 } ] ]
    },
    "Nova Sessao?": {
      "main": [
        [ { "node": "Criar Sessao Supabase", "type": "main", "index": 0 } ],
        [ { "node": "Agente Aninha (Gemini)", "type": "main", "index": 0 } ]
      ]
    },
    "Criar Sessao Supabase": {
      "main": [ [ { "node": "Agente Aninha (Gemini)", "type": "main", "index": 0 } ] ]
    },
    "Agente Aninha (Gemini)": {
      "main": [ [ { "node": "Processar Resposta e Lead", "type": "main", "index": 0 } ] ]
    },
    "Processar Resposta e Lead": {
      "main": [ [ { "node": "Lead Qualificado?", "type": "main", "index": 0 } ] ]
    },
    "Lead Qualificado?": {
      "main": [
        [ { "node": "Cadastrar Lead (CRM)", "type": "main", "index": 0 } ]
      ]
    },
    "Cadastrar Lead (CRM)": {
      "main": [ [ { "node": "Alerta Diogo Telegram", "type": "main", "index": 0 } ] ]
    }
  },
  "active": False,
  "settings": {
    "executionOrder": "v1"
  }
}

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\151_ANINHA_ATENDIMENTO_CRM_DL.json'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Workflow Aninha atualizado em {path}")
