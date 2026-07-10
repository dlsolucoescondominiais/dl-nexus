import json
from pathlib import Path

# WORKFLOW 1/7: DL_BIZ_LEAD_SCORING
# Conforms to Protocol V8.1 - Implementing Feature Flags, Logs, Idempotency

SCORE_WEIGHTS = {
  "DOR": 0.25,
  "POTENCIAL_RECORRENCIA": 0.25,
  "FACILIDADE_OPERACIONAL": 0.20,
  "POTENCIAL_EXPANSAO": 0.15,
  "LOCALIZACAO": 0.10,
  "TICKET": 0.05
}

SEGMENTOS_DL = {
  "CONDOMINIO_POPULAR":    { "peso": 15, "descricao": "MCMV, habitacional popular" },
  "CONDOMINIO_ECONOMICO":  { "peso": 20, "descricao": "Compactos, antigos, <R$1200" },
  "CONDOMINIO_COMPACTO":   { "peso": 18, "descricao": "8-20 unidades" },
  "CONDOMINIO_TRADICIONAL":{ "peso": 25, "descricao": "20-80 unidades, R$800-2000" },
  "CONDOMINIO_PEQUENO_PORTE": { "peso": 17, "descricao": "<30 unidades" }
}

workflow = {
  "name": "DL_BIZ_LEAD_SCORING_v8.1",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "dl-biz-lead-scoring",
        "responseMode": "lastNode",
        "options": {}
      },
      "name": "Webhook Lead Input",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [ 100, 300 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "SELECT enabled FROM dl_feature_flags WHERE flag_name = 'ENABLE_LEAD_SCORING';"
      },
      "name": "Check Feature Flag",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 300, 300 ]
    },
    {
      "parameters": {
        "conditions": {
          "boolean": [
            {
              "value1": "={{$json.enabled}}",
              "value2": True
            }
          ]
        }
      },
      "name": "If Enabled",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [ 500, 300 ]
    },
    {
      "parameters": {
        "jsCode": """
const input = $('Webhook Lead Input').first().json.body || {};
const weights = """ + json.dumps(SCORE_WEIGHTS) + """;
const segments = """ + json.dumps(SEGMENTOS_DL) + """;

let dor = input.dor_score || 0;
let rec = input.recorrencia_score || 0;
let op = input.operacional_score || 0;
let exp = input.expansao_score || 0;
let loc = input.localizacao_score || 0;
let tkt = input.ticket_score || 0;

let final_score = (dor * weights.DOR) +
                  (rec * weights.POTENCIAL_RECORRENCIA) +
                  (op * weights.FACILIDADE_OPERACIONAL) +
                  (exp * weights.POTENCIAL_EXPANSAO) +
                  (loc * weights.LOCALIZACAO) +
                  (tkt * weights.TICKET);

let segment = input.segmento || 'CONDOMINIO_TRADICIONAL';
if (segments[segment]) {
   final_score += segments[segment].peso;
}

final_score = Math.min(100, final_score);

return { final_score, segment, calculated_at: new Date().toISOString(), id: input.lead_id };
"""
      },
      "name": "Calculate Score Engine",
      "type": "n8n-nodes-base.code",
      "typeVersion": 1,
      "position": [ 700, 200 ]
    },
    {
      "parameters": {
        "operation": "update",
        "schema": "public",
        "table": "dl_crm_leads",
        "updateKey": "id",
        "columns": "score_comercial",
        "mappingMode": "defineBelow",
        "assignments": {
           "score_comercial": "={{$json.final_score}}"
        }
      },
      "name": "Update Supabase dl_crm_leads",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 900, 200 ]
    },
    {
      "parameters": {
        "operation": "insert",
        "schema": "public",
        "table": "dl_nexus_logs",
        "mappingMode": "defineBelow",
        "assignments": {
           "workflow_name": "DL_BIZ_LEAD_SCORING",
           "message": "Lead score updated successfully",
           "details": "={{JSON.stringify($json)}}"
        }
      },
      "name": "Log Success",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 1100, 200 ]
    },
    {
      "parameters": {
        "operation": "insert",
        "schema": "public",
        "table": "dl_nexus_logs",
        "mappingMode": "defineBelow",
        "assignments": {
           "workflow_name": "DL_BIZ_LEAD_SCORING",
           "message": "Execution skipped - Feature Flag Disabled"
        }
      },
      "name": "Log Skipped",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 700, 400 ]
    }
  ],
  "connections": {
    "Webhook Lead Input": {
      "main": [ [ { "node": "Check Feature Flag", "type": "main", "index": 0 } ] ]
    },
    "Check Feature Flag": {
      "main": [ [ { "node": "If Enabled", "type": "main", "index": 0 } ] ]
    },
    "If Enabled": {
      "main": [
        [ { "node": "Calculate Score Engine", "type": "main", "index": 0 } ],
        [ { "node": "Log Skipped", "type": "main", "index": 0 } ]
      ]
    },
    "Calculate Score Engine": {
      "main": [ [ { "node": "Update Supabase dl_crm_leads", "type": "main", "index": 0 } ] ]
    },
    "Update Supabase dl_crm_leads": {
      "main": [ [ { "node": "Log Success", "type": "main", "index": 0 } ] ]
    }
  },
  "settings": {
    "saveExecutionProgress": True,
    "saveManualExecutions": False,
    "callerPolicy": "workflowsFromSameOwner",
    "errorWorkflow": "dl_nexus_error_handler"
  }
}

out_path = Path("DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/DL_BIZ_LEAD_SCORING.json")
out_path.write_text(json.dumps(workflow, indent=2))
print(f"Generated {out_path.name}")
