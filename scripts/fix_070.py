import json
import os

wf_data = {
  'name': '070_CRON_MANUS_DIARIO',
  'active': False,
  'nodes': [
    {
      'parameters': {
        'rule': {'interval': [{'field': 'cronExpression', 'expression': '35 0 * * *'}]}
      },
      'id': 'trigger',
      'name': 'Schedule Trigger',
      'type': 'n8n-nodes-base.scheduleTrigger',
      'typeVersion': 1,
      'position': [0, 0]
    },
    {
      'parameters': {
        'jsCode': 'return {json: {attempt: 0, max_attempts: 20, wait_seconds: 30}};'
      },
      'id': 'init_vars',
      'name': 'Init Loop Variables',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [200, 0]
    },
    {
      'parameters': {
        'jsCode': 'const d = new Date().toLocaleDateString("pt-BR"); return {json: {prompt: `Você é Manus AI, o Diretor de Marketing B2B da DL Soluções Condominiais.\nHoje é dia ${d}. Pense em condomínios pequenos/médios, colégios e restaurantes no Rio de Janeiro.\nUse os seguintes produtos: DL Guardião (segurança eletrônica/CFTV), Fortress (portaria autônoma/gestão de acesso), Gatekeeper (automação de portões), DL Acqua (água/bombas/cisternas), DL Volt (elétrica condominial), DL EcoVolt (solar), DL Alerta (prevenção de incêndio), DL Partner (manutenção continuada), Mult•Grill Express (chapas/fritadeiras/gastronomia comercial).\nNão use "visita técnica", use "Avaliação Técnica". Não cite Condfy. Não chame o Diogo de engenheiro, use "Tecnólogo Responsável" se necessário.\nRetorne JSON:\n{\n  "estrategia_texto": "...",\n  "produto": "...",\n  "publico_alvo": "...",\n  "bairro": "...",\n  "canal_destino": "...",\n  "objetivo": "..."\n}`}};'
      },
      'id': 'prompt',
      'name': 'Prepare Prompt',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [400, 0]
    },
    {
      'parameters': {
        'method': 'POST',
        'url': 'https://api.manus.gg/v1/task.create',
        'sendHeaders': True,
        'headerParameters': {
          'parameters': [
            {'name': 'Authorization', 'value': 'Bearer {{$env.MANUS_API_KEY}}'},
            {'name': 'Content-Type', 'value': 'application/json'}
          ]
        },
        'sendBody': True,
        'bodyParameters': {
          'parameters': [{'name': 'prompt', 'value': '={{$json.prompt}}'}]
        }
      },
      'id': 'create_task',
      'name': 'HTTP Request Manus Task',
      'type': 'n8n-nodes-base.httpRequest',
      'typeVersion': 4.1,
      'position': [600, 0]
    },
    {
      'parameters': {
        'jsCode': 'const task_id = $json.task_id || $json.id || ($json.data && ($json.data.task_id || $json.data.id)); if (!task_id) { throw new Error("Manus não retornou task_id. Verificar payload ou endpoint task.create."); } return {json: {task_id: task_id, attempt: $node["Init Loop Variables"].json.attempt, max_attempts: $node["Init Loop Variables"].json.max_attempts}};'
      },
      'id': 'extract_id',
      'name': 'Extract Task ID',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [800, 0]
    },
    {
      'parameters': {
        'method': 'GET',
        'url': '="https://api.manus.gg/v1/task.status?task_id=" + $json.task_id',
        'sendHeaders': True,
        'headerParameters': {
          'parameters': [{'name': 'Authorization', 'value': 'Bearer {{$env.MANUS_API_KEY}}'}]
        }
      },
      'id': 'check_status',
      'name': 'Check Task Status',
      'type': 'n8n-nodes-base.httpRequest',
      'typeVersion': 4.1,
      'position': [1000, 0]
    },
    {
      'parameters': {
        'jsCode': 'let s = ($json.status || ($json.data && $json.data.status) || ($json.task && $json.task.status) || "").toLowerCase(); let is_done = ["stopped", "completed", "succeeded", "success", "finished"].includes(s); let is_error = ["failed", "error", "cancelled", "timeout"].includes(s); let is_running = ["running", "pending", "queued", "processing", "created"].includes(s); return {json: {status: s, is_done, is_error, is_running, attempt: $node["Check Loop/Wait"] ? $node["Check Loop/Wait"].json.attempt + 1 : 1, max_attempts: 20}};'
      },
      'id': 'normalize_status',
      'name': 'Normalize Status',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [1200, 0]
    },
    {
      'parameters': {
        'conditions': {
          'boolean': [{'value1': '={{$json.is_done}}', 'value2': True}]
        }
      },
      'id': 'if_done',
      'name': 'IF Manus concluído?',
      'type': 'n8n-nodes-base.if',
      'typeVersion': 1,
      'position': [1400, 0]
    },
    {
      'parameters': {
        'jsCode': 'if ($json.attempt >= $json.max_attempts) { throw new Error("Timeout Manus: tarefa não concluiu em 10 minutos"); } return {json: {attempt: $json.attempt, task_id: $node["Extract Task ID"].json.task_id}};'
      },
      'id': 'check_loop',
      'name': 'Check Loop/Wait',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [1400, 200]
    },
    {
      'parameters': {'amount': 30, 'unit': 'seconds'},
      'id': 'wait',
      'name': 'Wait 30s',
      'type': 'n8n-nodes-base.wait',
      'typeVersion': 1,
      'position': [1200, 200]
    },
    {
      'parameters': {
        'jsCode': 'let txt = JSON.stringify($json); let parsed = null; try{ if($json.structured_output_result && $json.structured_output_result.value) parsed = JSON.parse($json.structured_output_result.value); else if($json.message && $json.message.content) parsed = JSON.parse($json.message.content); else { let match = txt.match(/```json\\n([\\s\\S]*?)\\n```/); if(match) parsed = JSON.parse(match[1]); } }catch(e){} if(!parsed){ throw new Error("Manus retornou sucesso, mas JSON é inválido ou ausente."); } if(!parsed.estrategia_texto || !parsed.produto) { throw new Error("JSON do Manus incompleto."); } return {json: parsed};'
      },
      'id': 'clean_json',
      'name': 'Limpar JSON do Manus',
      'type': 'n8n-nodes-base.code',
      'typeVersion': 2,
      'position': [1600, 0]
    },
    {
      'parameters': {
        'chatId': '-1002012015091',
        'text': '={{ "🎯 DIRETRIZ MANUS B2B \\n\\nPúblico: " + $json.publico_alvo + "\\nProduto: " + $json.produto + "\\nEstratégia: " + $json.estrategia_texto }}'
      },
      'id': 'telegram',
      'name': 'Telegram Entrega',
      'type': 'n8n-nodes-base.telegram',
      'typeVersion': 1.1,
      'position': [1800, 0],
      'continueOnFail': True
    },
    {
      'parameters': {
        'workflowId': '020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO'
      },
      'id': 'call_020',
      'name': 'Chamar MarkSolar (020)',
      'type': 'n8n-nodes-base.executeWorkflow',
      'typeVersion': 1,
      'position': [2000, 0]
    }
  ],
  'connections': {
    'Schedule Trigger': {'main': [[{'node': 'Init Loop Variables', 'type': 'main', 'index': 0}]]},
    'Init Loop Variables': {'main': [[{'node': 'Prepare Prompt', 'type': 'main', 'index': 0}]]},
    'Prepare Prompt': {'main': [[{'node': 'HTTP Request Manus Task', 'type': 'main', 'index': 0}]]},
    'HTTP Request Manus Task': {'main': [[{'node': 'Extract Task ID', 'type': 'main', 'index': 0}]]},
    'Extract Task ID': {'main': [[{'node': 'Check Task Status', 'type': 'main', 'index': 0}]]},
    'Check Task Status': {'main': [[{'node': 'Normalize Status', 'type': 'main', 'index': 0}]]},
    'Normalize Status': {'main': [[{'node': 'IF Manus concluído?', 'type': 'main', 'index': 0}]]},
    'IF Manus concluído?': {
      'main': [
        [{'node': 'Limpar JSON do Manus', 'type': 'main', 'index': 0}],
        [{'node': 'Check Loop/Wait', 'type': 'main', 'index': 0}]
      ]
    },
    'Check Loop/Wait': {'main': [[{'node': 'Wait 30s', 'type': 'main', 'index': 0}]]},
    'Wait 30s': {'main': [[{'node': 'Check Task Status', 'type': 'main', 'index': 0}]]},
    'Limpar JSON do Manus': {'main': [[{'node': 'Telegram Entrega', 'type': 'main', 'index': 0}]]},
    'Telegram Entrega': {'main': [[{'node': 'Chamar MarkSolar (020)', 'type': 'main', 'index': 0}]]}
  }
}

paths = [
  r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json',
  r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\070_CRON_MANUS_DIARIO_config.json',
  r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\09_PRONTOS_PARA_PRODUCAO\070_CRON_MANUS_DIARIO.json'
]

for p in paths:
  os.makedirs(os.path.dirname(p), exist_ok=True)
  with open(p, 'w', encoding='utf-8') as f:
    json.dump(wf_data, f, ensure_ascii=False, indent=2)

print('Workflows salvos com sucesso nas 3 pastas.')
