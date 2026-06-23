import json
import os

workflow = {
  "name": "140B_AGENTE_ZELADOR_EXECUTOR_MOVIMENTACAO_APROVADA",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            {
              "field": "cron",
              "expression": "0 2 * * *"
            }
          ]
        }
      },
      "id": "trigger_executor_diario",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [ 100, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "select * from dl_zelador_arquivos where status = 'aprovado_para_mover' and acao_aprovada = 'mover' and coalesce(precisa_revisao_humana, false) = false and file_id is not null and pasta_origem_id is not null and pasta_destino_id is not null limit 20;"
      },
      "id": "fetch_approved_supabase",
      "name": "Supabase Fetch Approved",
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
        "batchSize": 5,
        "options": {}
      },
      "id": "loop_batches",
      "name": "Split In Batches",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 2,
      "position": [ 500, 300 ]
    },
    {
      "parameters": {
        "jsCode": """
const item = $input.item.json;
const isDryRun = (process.env.GOOGLE_DRIVE_EXECUTOR_DRY_RUN === 'true' || process.env.GOOGLE_DRIVE_EXECUTOR_DRY_RUN === true || process.env.GOOGLE_DRIVE_EXECUTOR_DRY_RUN === undefined);

let bloqueado = false;
let motivo_bloqueio = '';

if (item.pasta_origem_id === item.pasta_destino_id) { bloqueado = true; motivo_bloqueio = 'Origem igual destino'; }
else if (!item.file_id || !item.pasta_origem_id || !item.pasta_destino_id) { bloqueado = true; motivo_bloqueio = 'IDs ausentes'; }
else if (item.acao_aprovada !== 'mover') { bloqueado = true; motivo_bloqueio = 'Acao nao e mover'; }
else if (item.status !== 'aprovado_para_mover') { bloqueado = true; motivo_bloqueio = 'Status nao e aprovado'; }
else if (item.precisa_revisao_humana === true) { bloqueado = true; motivo_bloqueio = 'Revisao humana pendente'; }

return [{
  json: {
    ...item,
    dry_run: isDryRun,
    bloqueado: bloqueado,
    motivo_bloqueio: motivo_bloqueio
  }
}];
"""
      },
      "id": "validacao_seguranca",
      "name": "Validacao de Seguranca e DRY RUN",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 700, 300 ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            { "value1": "={{ $json.bloqueado }}", "value2": True }
          ]
        }
      },
      "id": "if_bloqueado",
      "name": "Esta Bloqueado?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 900, 300 ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            { "value1": "={{ $json.dry_run }}", "value2": True }
          ]
        }
      },
      "id": "if_dry_run",
      "name": "Se DRY RUN?",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 1100, 400 ]
    },
    {
      "parameters": {
        "url": "={{ 'https://www.googleapis.com/drive/v3/files/' + $json.file_id + '?addParents=' + $json.pasta_destino_id + '&removeParents=' + $json.pasta_origem_id + '&fields=id,name,parents,webViewLink' }}",
        "method": "PATCH",
        "authentication": "predefinedCredentialType",
        "nodeCredentialType": "googleApi",
        "sendHeaders": True,
        "headerParameters": {
          "parameters": [
            { "name": "Content-Type", "value": "application/json" }
          ]
        }
      },
      "id": "http_patch_google_drive",
      "name": "Google Drive API v3 (PATCH)",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.1,
      "position": [ 1300, 500 ],
      "credentials": {
        "googleApi": {
          "id": "google_api_cred",
          "name": "Google OAuth2 API"
        }
      },
      "onError": "continueErrorOutput"
    },
    {
      "parameters": {
        "jsCode": """
const item = $input.item.json;
const isError = !!item.error;
const isDryRun = item.dry_run;

let status_update = '';
let erro = null;

if (isDryRun) {
  status_update = 'dry_run_movimento_validado';
} else if (isError) {
  status_update = 'erro_movimentacao';
  erro = item.error.message || 'Erro desconhecido na Google Drive API';
} else {
  status_update = 'movido';
}

return [{
  json: {
    ...item,
    status_update: status_update,
    erro_update: erro,
    movido_em: isError || isDryRun ? null : new Date().toISOString()
  }
}];
"""
      },
      "id": "prepare_supabase_update",
      "name": "Preparar Atualizacao Supabase",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 1500, 400 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "=UPDATE dl_zelador_arquivos SET status = '{{ $json.status_update }}', erro = '{{ $json.erro_update }}', movido_em = {{ $json.movido_em ? \"'\" + $json.movido_em + \"'\" : 'null' }}, tentativas_movimento = tentativas_movimento + {{ $json.status_update === 'erro_movimentacao' ? 1 : 0 }}, pasta_final_id = {{ $json.status_update === 'movido' ? \"'\" + $json.pasta_destino_id + \"'\" : 'null' }} WHERE id = '{{ $json.id }}';"
      },
      "id": "update_supabase",
      "name": "Supabase Update Status",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 1700, 400 ],
      "credentials": {
        "database": {
          "id": "supabase_postgres_cred_id",
          "name": "Supabase Connection"
        }
      }
    },
    {
      "parameters": {
        "jsCode": "return [{ json: { loop: true } }];"
      },
      "id": "loop_end",
      "name": "Continuar Lote",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 1900, 400 ]
    },
    {
      "parameters": {
        "chatId": "YOUR_TELEGRAM_CHAT_ID",
        "text": "=🤖 *Agente Zelador Executor - Fim de Lote*\n\nProcessamento Finalizado."
      },
      "id": "telegram_resumo",
      "name": "Telegram Resumo",
      "type": "n8n-nodes-base.telegram",
      "typeVersion": 1.1,
      "position": [ 1000, 100 ],
      "credentials": {
        "telegramApi": {
          "id": "telegram_cred_id",
          "name": "Telegram Bot Account"
        }
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [ [ { "node": "Supabase Fetch Approved", "type": "main", "index": 0 } ] ]
    },
    "Supabase Fetch Approved": {
      "main": [ [ { "node": "Split In Batches", "type": "main", "index": 0 } ] ]
    },
    "Split In Batches": {
      "main": [ 
        [ { "node": "Validacao de Seguranca e DRY RUN", "type": "main", "index": 0 } ],
        [ { "node": "Telegram Resumo", "type": "main", "index": 0 } ]
      ]
    },
    "Validacao de Seguranca e DRY RUN": {
      "main": [ [ { "node": "Esta Bloqueado?", "type": "main", "index": 0 } ] ]
    },
    "Esta Bloqueado?": {
      "main": [
        [ { "node": "Preparar Atualizacao Supabase", "type": "main", "index": 0 } ],
        [ { "node": "Se DRY RUN?", "type": "main", "index": 0 } ]
      ]
    },
    "Se DRY RUN?": {
      "main": [
        [ { "node": "Preparar Atualizacao Supabase", "type": "main", "index": 0 } ],
        [ { "node": "Google Drive API v3 (PATCH)", "type": "main", "index": 0 } ]
      ]
    },
    "Google Drive API v3 (PATCH)": {
      "main": [ [ { "node": "Preparar Atualizacao Supabase", "type": "main", "index": 0 } ] ]
    },
    "Preparar Atualizacao Supabase": {
      "main": [ [ { "node": "Supabase Update Status", "type": "main", "index": 0 } ] ]
    },
    "Supabase Update Status": {
      "main": [ [ { "node": "Continuar Lote", "type": "main", "index": 0 } ] ]
    },
    "Continuar Lote": {
      "main": [ [ { "node": "Split In Batches", "type": "main", "index": 0 } ] ]
    }
  },
  "active": False,
  "settings": {
    "executionOrder": "v1"
  }
}

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\140B_AGENTE_ZELADOR_EXECUTOR_MOVIMENTACAO_APROVADA.json'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2)

print(f"Workflow 140B criado em {path}")
