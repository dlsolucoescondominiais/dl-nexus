import json
import os

workflow = {
  "name": "150_SOCIAL_LISTENER_ROUTER_DL",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "social-webhook",
        "options": {}
      },
      "id": "webhook_entry",
      "name": "Meta / Evolution Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [ 100, 300 ],
      "webhookId": "social-listener-uuid"
    },
    {
      "parameters": {
        "jsCode": """
const payload = $input.item.json;
let canal = 'unknown';
let origem = 'unknown';
let usuario_nome = 'Desconhecido';
let usuario_id = '0';
let mensagem = '';
let keyword = null;

// Mock logic for Meta Graph API / Evolution Webhook Extraction
if (payload.entry && payload.entry[0].messaging) {
    canal = 'facebook_instagram';
    origem = 'direct';
    usuario_id = payload.entry[0].messaging[0].sender.id;
    mensagem = payload.entry[0].messaging[0].message.text;
} else if (payload.data && payload.data.message) {
    canal = 'whatsapp';
    origem = 'whatsapp_api';
    usuario_id = payload.data.sender;
    usuario_nome = payload.data.pushName || 'Desconhecido';
    mensagem = payload.data.message;
}

if (mensagem.toLowerCase().includes('avaliacao') || mensagem.toLowerCase().includes('avaliação')) {
    keyword = 'AVALIAÇÃO';
}

return [{
  json: {
    canal,
    origem,
    usuario_id,
    usuario_nome,
    mensagem,
    palavra_chave_detectada: keyword,
    tipo_evento: keyword ? 'orcamento' : 'duvida'
  }
}];
"""
      },
      "id": "extract_data",
      "name": "Extrair Dados e Normalizar",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 300, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO dl_social_events (canal, origem, usuario_nome, usuario_id, mensagem, palavra_chave_detectada, tipo_evento) VALUES ('{{ $json.canal }}', '{{ $json.origem }}', '{{ $json.usuario_nome }}', '{{ $json.usuario_id }}', '{{ $json.mensagem }}', '{{ $json.palavra_chave_detectada }}', '{{ $json.tipo_evento }}') ON CONFLICT (canal, usuario_id, mensagem, criado_em) DO NOTHING RETURNING id;"
      },
      "id": "save_event",
      "name": "Salvar Evento Supabase",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 500, 300 ],
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
          "string": [
            { "value1": "={{ $json.id }}", "operation": "isNotEmpty" }
          ]
        }
      },
      "id": "check_saved",
      "name": "Foi salvo?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 700, 300 ]
    },
    {
      "parameters": {
        "workflowId": "151_ANINHA_ATENDIMENTO_CRM_DL",
        "mode": "each"
      },
      "id": "call_aninha",
      "name": "Acionar Aninha Atendimento",
      "type": "n8n-nodes-base.executeWorkflow",
      "typeVersion": 1,
      "position": [ 900, 200 ]
    }
  ],
  "connections": {
    "Meta / Evolution Webhook": {
      "main": [ [ { "node": "Extrair Dados e Normalizar", "type": "main", "index": 0 } ] ]
    },
    "Extrair Dados e Normalizar": {
      "main": [ [ { "node": "Salvar Evento Supabase", "type": "main", "index": 0 } ] ]
    },
    "Salvar Evento Supabase": {
      "main": [ [ { "node": "Foi salvo?", "type": "main", "index": 0 } ] ]
    },
    "Foi salvo?": {
      "main": [
        [ { "node": "Acionar Aninha Atendimento", "type": "main", "index": 0 } ]
      ]
    }
  },
  "active": False,
  "settings": {
    "executionOrder": "v1"
  }
}

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\150_SOCIAL_LISTENER_ROUTER_DL.json'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Workflow Listener atualizado em {path}")
