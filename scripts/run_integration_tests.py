import urllib.request
import json
import ssl
import time

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
n8n_api_key = ""
n8n_host = ""
supabase_anon_key = ""

with open(ENV_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith("N8N_API_KEY="):
            n8n_api_key = line.split("=", 1)[1].strip()
        elif line.startswith("N8N_HOST="):
            n8n_host = line.split("=", 1)[1].strip()
        elif line.startswith("SUPABASE_ANON_KEY="):
            supabase_anon_key = line.split("=", 1)[1].strip()

if not n8n_host.endswith("/"):
    n8n_host += "/"

headers = {
    "X-N8N-API-KEY": n8n_api_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

ctx = ssl.create_default_context()
ssl_fallback_active = False

def check_ssl_connection():
    global ctx, ssl_fallback_active
    try:
        req = urllib.request.Request(n8n_host + "workflows", headers=headers, method="GET")
        urllib.request.urlopen(req, context=ctx, timeout=5)
    except urllib.error.URLError as e:
        if "certificate verify failed" in str(e.reason) or (hasattr(e.reason, 'reason') and "certificate verify failed" in str(e.reason.reason)):
            print("[!] SSL certificate verification failed. Falling back to unverified context due to local/self-signed certificate in tests.")
            ctx = ssl._create_unverified_context()
            ssl_fallback_active = True
        else:
            pass
    except Exception:
        pass

check_ssl_connection()

def get_last_execution(wf_id):
    req = urllib.request.Request(n8n_host + f"executions?workflowId={wf_id}&limit=1", headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and data.get('data'):
                exec_id = data['data'][0]['id']
                # Get detailed execution data
                det_req = urllib.request.Request(n8n_host + f"executions/{exec_id}?includeData=true", headers=headers)
                with urllib.request.urlopen(det_req, context=ctx) as det_res:
                    return json.loads(det_res.read().decode('utf-8'))
    except Exception as e:
        print(f"Error fetching execution log: {e}")
    return None

def run_tests():
    # We will build a temporary testing workflow that uses a Webhook trigger instead of Telegram Trigger
    temp_wf = {
      "name": "TEMP_TEST_ANINHA_RECEPCAO",
      "nodes": [
        {
          "parameters": {
            "httpMethod": "POST",
            "path": "test-aninha-recepcao",
            "responseMode": "responseNode",
            "options": {}
          },
          "id": "webhook_trigger",
          "name": "Webhook Trigger",
          "type": "n8n-nodes-base.webhook",
          "typeVersion": 1,
          "position": [100, 300],
          "webhookId": "test-aninha-recepcao-wh"
        },
        {
          "parameters": {
            "jsCode": "const msg = $input.item.json.body.message || {};\nconst canal = 'telegram';\nconst chat_id = String(msg.chat?.id || '');\nconst message_id = String(msg.message_id || '');\nconst texto = msg.text || '';\nconst first_name = msg.from?.first_name || '';\nconst last_name = msg.from?.last_name || '';\nconst nome_usuario = (first_name + ' ' + last_name).trim() || 'Cliente Telegram';\nconst username = msg.from?.username || '';\n\nlet hash_mensagem = message_id;\nif (!message_id) {\n  const min = new Date().toISOString().substring(0, 16); // yyyy-mm-ddThh:mm\n  hash_mensagem = canal + '_' + chat_id + '_' + texto.substring(0, 50) + '_' + min;\n}\n\nreturn [{\n  json: {\n    canal,\n    chat_id,\n    message_id,\n    hash_mensagem,\n    nome_usuario,\n    username,\n    texto\n  }\n}];"
          },
          "id": "normalizar_entrada_node",
          "name": "Normalizar Entrada",
          "type": "n8n-nodes-base.code",
          "typeVersion": 2,
          "position": [300, 300]
        },
        {
          "parameters": {
            "method": "GET",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/mensagens_processadas_aninha?canal=eq.telegram&chat_id=eq.{{ $json.chat_id }}&hash_mensagem=eq.{{ $json.hash_mensagem }}&limit=1",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"}
              ]
            },
            "options": {
              "splitIntoItems": False
            }
          },
          "id": "buscar_processada_node",
          "name": "Buscar Processada",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [500, 300],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "conditions": {
              "boolean": [
                {
                  "value1": "={{ $json.length > 0 }}",
                  "value2": True
                }
              ]
            }
          },
          "id": "mensagem_duplicada_node",
          "name": "Mensagem Duplicada?",
          "type": "n8n-nodes-base.if",
          "typeVersion": 1,
          "position": [700, 300]
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/eventos_aninha",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
          ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { canal: \"telegram\", chat_id: $node[\"Normalizar Entrada\"].json.chat_id, message_id: $node[\"Normalizar Entrada\"].json.message_id, direcao: \"sistema\", tipo_evento: \"mensagem_duplicada_ignorada\", conteudo: \"Mensagem duplicada ignorada\", payload: $node[\"Normalizar Entrada\"].json } }}"
          },
          "id": "logar_duplicidade_node",
          "name": "Logar Duplicidade",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [900, 150],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/mensagens_processadas_aninha",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
              ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { canal: \"telegram\", chat_id: $node[\"Normalizar Entrada\"].json.chat_id, message_id: $node[\"Normalizar Entrada\"].json.message_id, hash_mensagem: $node[\"Normalizar Entrada\"].json.hash_mensagem } }}"
          },
          "id": "marcar_processada_node",
          "name": "Marcar Processada",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [900, 400],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "method": "GET",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/conversas_aninha?canal=eq.telegram&chat_id=eq.{{ $node[\"Normalizar Entrada\"].json.chat_id }}&limit=1",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"}
              ]
            },
            "options": {
              "splitIntoItems": False
            }
          },
          "id": "buscar_conversa_node",
          "name": "Buscar Conversa",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [1100, 400],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "conditions": {
              "boolean": [
                {
                  "value1": "={{ $json.length > 0 }}",
                  "value2": True
                }
              ]
            }
          },
          "id": "conversa_existe_node",
          "name": "Conversa Existe?",
          "type": "n8n-nodes-base.if",
          "typeVersion": 1,
          "position": [1300, 400]
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/conversas_aninha",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
              ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { canal: \"telegram\", chat_id: $node[\"Normalizar Entrada\"].json.chat_id, username: $node[\"Normalizar Entrada\"].json.username, nome_usuario: $node[\"Normalizar Entrada\"].json.nome_usuario, etapa_funil: \"inicio\", status: \"em_atendimento\", dados_coletados: {} } }}"
          },
          "id": "criar_conversa_node",
          "name": "Criar Conversa",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [1500, 300],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "jsCode": "const normalizado = $node[\"Normalizar Entrada\"].json;\nconst conversa = $items(\"Buscar Conversa\");\n\nlet contexto = {\n  intencao_atual: \"indefinido\",\n  etapa_funil: \"inicio\",\n  segmento: \"indefinido\",\n  dados_coletados: {},\n  ultima_mensagem: \"\",\n  ultima_resposta: \"\"\n};\n\nconst firstItem = (conversa && conversa.length > 0) ? conversa[0].json : null;\nconst c = (firstItem && !firstItem.error) ? (Array.isArray(firstItem) ? firstItem[0] : firstItem) : null;\nif (c && c.id) {\n  contexto.intencao_atual = c.intencao_atual || \"indefinido\";\n  contexto.etapa_funil = c.etapa_funil || \"inicio\";\n  contexto.segmento = c.segmento || \"indefinido\";\n  contexto.dados_coletados = c.dados_coletados || {};\n  contexto.ultima_mensagem = c.ultima_mensagem || \"\";\n  contexto.ultima_resposta = c.ultima_resposta || \"\";\n}\n\nreturn [{\n  json: {\n    canal: normalizado.canal,\n    chat_id: normalizado.chat_id,\n    message_id: normalizado.message_id,\n    nome_usuario: normalizado.nome_usuario,\n    username: normalizado.username,\n    mensagem_atual: normalizado.texto,\n    contexto: contexto\n  }\n}];"
          },
          "id": "preparar_payload_motor_node",
          "name": "Preparar Payload Motor",
          "type": "n8n-nodes-base.code",
          "typeVersion": 2,
          "position": [1750, 400]
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://n8n.dlsolucoescondominiais.com.br/webhook/dl-aninha-atendimento",
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ $json }}",
            "options": {}
          },
          "id": "aninha_atendimento_node",
          "name": "Aninha Atendimento",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [1950, 400],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "conditions": {
              "boolean": [
                {
                  "value1": "={{ $json.resposta_cliente !== undefined && $json.resposta_cliente !== null }}",
                  "value2": True
                }
              ]
            }
          },
          "id": "ia_retornou_resposta_node",
          "name": "IA Retornou Resposta?",
          "type": "n8n-nodes-base.if",
          "typeVersion": 1,
          "position": [2150, 400]
        },
        {
          "parameters": {
            "jsCode": "const err = $node[\"Aninha Atendimento\"].json.error || $node[\"Aninha Atendimento\"].json;\nlet userMsg = '';\ntry {\n  userMsg = ($node[\"Normalizar Entrada\"].json.texto || '').toLowerCase();\n} catch (e) {\n  userMsg = '';\n}\n\nconst residentialKeywords = [\n  \"apartamento\", \"apto\", \"minha casa\", \"residência\", \"residencial\", \n  \"chuveiro\", \"tomada\", \"disjuntor do meu apartamento\", \"casa\"\n];\nlet isResidential = false;\nfor (const keyword of residentialKeywords) {\n  if (userMsg.includes(keyword)) {\n    isResidential = true;\n    break;\n  }\n}\n\nlet result = {};\nif (isResidential) {\n  result = {\n    responder_cliente: true,\n    resposta_cliente: \"No momento, a DL Soluções Condominiais atende demandas técnicas voltadas a condomínios, escolas, empresas e suporte a equipamentos profissionais. Para esse tipo de solicitação residencial avulsa, não conseguimos seguir com atendimento.\",\n    intencao_atual: \"residencial_bloqueado\",\n    etapa_funil: \"bloqueado_residencial\",\n    segmento: \"residencial\",\n    dados_coletados: {},\n    lead_qualificado: false,\n    encaminhar_humano: false,\n    motivo_encaminhamento: null,\n    bloquear: true,\n    motivo_bloqueio: \"atendimento residencial avulsa\",\n    is_fallback: true,\n    error_details: JSON.stringify(err)\n  };\n} else {\n  result = {\n    responder_cliente: true,\n    resposta_cliente: \"Recebi sua mensagem. Para seguir com a Avaliação Técnica, me informe o nome do condomínio, bairro e o problema principal identificado.\",\n    intencao_atual: \"indefinido\",\n    etapa_funil: \"coletando_dados_condominio\",\n    segmento: \"indefinido\",\n    dados_coletados: {},\n    lead_qualificado: false,\n    encaminhar_humano: false,\n    motivo_encaminhamento: null,\n    bloquear: false,\n    motivo_bloqueio: null,\n    is_fallback: true,\n    error_details: JSON.stringify(err)\n  };\n}\n\nreturn [{ json: result }];"
          },
          "id": "preparar_fallback_node",
          "name": "Preparar Fallback",
          "type": "n8n-nodes-base.code",
          "typeVersion": 2,
          "position": [2350, 250]
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/logs_aninha_erros",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
              ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { workflow: \"001_TELEGRAM_RECEPCAO_ANINHA_V3\", node_name: \"Aninha Atendimento\", canal: \"telegram\", chat_id: $node[\"Normalizar Entrada\"].json.chat_id, erro: $json.error_details, payload: $json } }}"
          },
          "id": "logar_erro_ia_node",
          "name": "Logar Erro de IA (Supabase)",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [2550, 150],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "jsCode": "return [{ json: $json }];"
          },
          "id": "obter_resposta_final_node",
          "name": "Obter Resposta Final",
          "type": "n8n-nodes-base.code",
          "typeVersion": 2,
          "position": [2550, 400]
        },
        {
          "parameters": {
            "method": "PATCH",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/conversas_aninha?canal=eq.telegram&chat_id=eq.{{ $node[\"Normalizar Entrada\"].json.chat_id }}",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
              ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { intencao_atual: $json.intencao_atual, etapa_funil: $json.etapa_funil, segmento: $json.segmento, dados_coletados: $json.dados_coletados, ultima_mensagem: $node[\"Normalizar Entrada\"].json.texto, ultima_resposta: $json.resposta_cliente, status: $json.etapa_funil === 'lead_qualificado' ? 'lead_qualificado' : ($json.etapa_funil === 'bloqueado_residencial' ? 'bloqueado_residencial' : ($json.encaminhar_humano ? 'encaminhado_humano' : 'em_atendimento')), updated_at: new Date().toISOString() } }}"
          },
          "id": "atualizar_conversa_node",
          "name": "Atualizar Conversa",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [2750, 400],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "jsCode": "const normalizado = $node[\"Normalizar Entrada\"].json;\nconst motor = $node[\"Obter Resposta Final\"].json;\n\nconst events = [];\n\nevents.push({\n  canal: \"telegram\",\n  chat_id: normalizado.chat_id,\n  message_id: normalizado.message_id,\n  direcao: \"entrada\",\n  tipo_evento: \"entrada_usuario\",\n  conteudo: normalizado.texto,\n  payload: {}\n});\n\nevents.push({\n  canal: \"telegram\",\n  chat_id: normalizado.chat_id,\n  message_id: \"\",\n  direcao: \"saida\",\n  tipo_evento: \"resposta_aninha\",\n  conteudo: motor.resposta_cliente,\n  payload: motor\n});\n\nif (motor.lead_qualificado) {\n  events.push({\n    canal: \"telegram\",\n    chat_id: normalizado.chat_id,\n    message_id: \"\",\n    direcao: \"sistema\",\n    tipo_evento: \"lead_qualificado\",\n    conteudo: \"Lead qualificado pela Aninha\",\n    payload: motor.dados_coletados\n  });\n}\n\nif (motor.etapa_funil === \"bloqueado_residencial\") {\n  events.push({\n    canal: \"telegram\",\n    chat_id: normalizado.chat_id,\n    message_id: \"\",\n    direcao: \"sistema\",\n    tipo_evento: \"bloqueio_residencial\",\n    conteudo: \"Residencial bloqueado\",\n    payload: { motivo: motor.motivo_bloqueio }\n  });\n}\n\nreturn events.map(e => ({ json: e }));"
          },
          "id": "preparar_eventos_node",
          "name": "Preparar Eventos",
          "type": "n8n-nodes-base.code",
          "typeVersion": 2,
          "position": [2950, 400]
        },
        {
          "parameters": {
            "method": "POST",
            "url": "https://nejdtvkpiclagsnfljsz.supabase.co/rest/v1/eventos_aninha",
            "sendHeaders": True,
            "headerParameters": {
              "parameters": [
                {"name": "apikey", "value": supabase_anon_key},
                {"name": "Authorization", "value": f"Bearer {supabase_anon_key}"},
                {"name": "Content-Type", "value": "application/json"}
              ]
            },
            "sendBody": True,
            "specifyBody": "json",
            "jsonBody": "={{ { canal: $json.canal, chat_id: $json.chat_id, message_id: $json.message_id, direcao: $json.direcao, tipo_evento: $json.tipo_evento, conteudo: $json.conteudo, payload: $json.payload } }}"
          },
          "id": "salvar_eventos_node",
          "name": "Salvar Eventos",
          "type": "n8n-nodes-base.httpRequest",
          "typeVersion": 4.1,
          "position": [3150, 400],
          "onError": "continueRegularOutput"
        },
        {
          "parameters": {
            "respondWith": "json",
            "responseBody": "={{ JSON.stringify($json) }}",
            "options": {}
          },
          "id": "respond_caller",
          "name": "Retornar Resposta Webhook",
          "type": "n8n-nodes-base.respondToWebhook",
          "typeVersion": 1,
          "position": [3350, 400]
        }
      ],
      "connections": {
        "Webhook Trigger": {
          "main": [
            [
              {
                "node": "Normalizar Entrada",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Normalizar Entrada": {
          "main": [
            [
              {
                "node": "Buscar Processada",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Buscar Processada": {
          "main": [
            [
              {
                "node": "Mensagem Duplicada?",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Mensagem Duplicada?": {
          "main": [
            [
              {
                "node": "Logar Duplicidade",
                "type": "main",
                "index": 0
              }
            ],
            [
              {
                "node": "Marcar Processada",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Marcar Processada": {
          "main": [
            [
              {
                "node": "Buscar Conversa",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Buscar Conversa": {
          "main": [
            [
              {
                "node": "Conversa Existe?",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Conversa Existe?": {
          "main": [
            [
              {
                "node": "Preparar Payload Motor",
                "type": "main",
                "index": 0
              }
            ],
            [
              {
                "node": "Criar Conversa",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Criar Conversa": {
          "main": [
            [
              {
                "node": "Preparar Payload Motor",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Preparar Payload Motor": {
          "main": [
            [
              {
                "node": "Aninha Atendimento",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Aninha Atendimento": {
          "main": [
            [
              {
                "node": "IA Retornou Resposta?",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "IA Retornou Resposta?": {
          "main": [
            [
              {
                "node": "Obter Resposta Final",
                "type": "main",
                "index": 0
              }
            ],
            [
              {
                "node": "Preparar Fallback",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Preparar Fallback": {
          "main": [
            [
              {
                "node": "Logar Erro de IA (Supabase)",
                "type": "main",
                "index": 0
              },
              {
                "node": "Obter Resposta Final",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Obter Resposta Final": {
          "main": [
            [
              {
                "node": "Retornar Resposta Webhook",
                "type": "main",
                "index": 0
              },
              {
                "node": "Atualizar Conversa",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Atualizar Conversa": {
          "main": [
            [
              {
                "node": "Preparar Eventos",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Preparar Eventos": {
          "main": [
            [
              {
                "node": "Salvar Eventos",
                "type": "main",
                "index": 0
              }
            ]
          ]
        },
        "Salvar Eventos": {
          "main": [
            []
          ]
        }
      },
      "settings": {}
    }
    
    print("[*] Deploying temporary testing workflow...")
    req_post = urllib.request.Request(n8n_host + "workflows", data=json.dumps(temp_wf).encode('utf-8'), headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req_post, context=ctx)
        wf_data = json.loads(resp.read().decode('utf-8'))
        wf_id = wf_data.get('id')
        print(f"[+] Temp workflow created! ID: {wf_id}")
    except Exception as e:
        print(f"[-] Failed to create temp workflow: {e}")
        return
        
    try:
        # Activate it
        req_act = urllib.request.Request(n8n_host + f"workflows/{wf_id}/activate", data=b'{}', headers=headers, method="POST")
        urllib.request.urlopen(req_act, context=ctx)
        print("[+] Activated temp workflow.")
        
        webhook_url = n8n_host.replace("/api/v1/", "/webhook/") + "test-aninha-recepcao"
        
        # Test 1 — Início de atendimento
        print("\n--- TEST 1: Início de atendimento ---")
        p1 = {
          "message": {
            "chat": {"id": 112233},
            "message_id": 1001,
            "from": {"first_name": "Diogo", "last_name": "Oliveira", "username": "diogotest"},
            "text": "Agendar uma Avaliação Técnica para o sistema de bombas do condomínio"
          }
        }
        
        try:
            req_t = urllib.request.Request(webhook_url, data=json.dumps(p1).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
            res_t = urllib.request.urlopen(req_t, context=ctx)
            resp_json = json.loads(res_t.read().decode('utf-8'))
            print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        except Exception as te:
            print(f"[-] Test 1 failed: {te}")
            # Fetch last execution
            print("[*] Fetching detailed execution error log from n8n...")
            details = get_last_execution(wf_id)
            if details:
                with open("scripts/test_execution_error.json", "w", encoding="utf-8") as f:
                    json.dump(details, f, indent=2, ensure_ascii=False)
                print("[+] Detailed execution log saved to scripts/test_execution_error.json")
            return # stop if it fails
            
        time.sleep(15)
        # Test 2 — Continuação com memória
        print("\n--- TEST 2: Continuação com memória ---")
        p2 = {
          "message": {
            "chat": {"id": 112233},
            "message_id": 1002,
            "from": {"first_name": "Diogo", "last_name": "Oliveira", "username": "diogotest"},
            "text": "São duas bombas. O painel está desarmando. Fica na Barra da Tijuca."
          }
        }
        req_t = urllib.request.Request(webhook_url, data=json.dumps(p2).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
        res_t = urllib.request.urlopen(req_t, context=ctx)
        resp_json = json.loads(res_t.read().decode('utf-8'))
        print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        
        time.sleep(15)
        # Test 3 — Qualificação
        print("\n--- TEST 3: Qualificação ---")
        p3 = {
          "message": {
            "chat": {"id": 112233},
            "message_id": 1003,
            "from": {"first_name": "Diogo", "last_name": "Oliveira", "username": "diogotest"},
            "text": "Condomínio Solar da Barra, responsável Diogo, pode ser amanhã de manhã."
          }
        }
        req_t = urllib.request.Request(webhook_url, data=json.dumps(p3).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
        res_t = urllib.request.urlopen(req_t, context=ctx)
        resp_json = json.loads(res_t.read().decode('utf-8'))
        print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        
        time.sleep(15)
        # Test 4 — Residencial bloqueado
        print("\n--- TEST 4: Residencial bloqueado ---")
        p4 = {
          "message": {
            "chat": {"id": 445566},
            "message_id": 2001,
            "from": {"first_name": "Carlos", "last_name": "Silva"},
            "text": "Quero trocar o disjuntor do meu apartamento."
          }
        }
        req_t = urllib.request.Request(webhook_url, data=json.dumps(p4).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
        res_t = urllib.request.urlopen(req_t, context=ctx)
        resp_json = json.loads(res_t.read().decode('utf-8'))
        print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        
        time.sleep(15)
        # Test 5 — Preço
        print("\n--- TEST 5: Preço ---")
        p5 = {
          "message": {
            "chat": {"id": 778899},
            "message_id": 3001,
            "from": {"first_name": "Ana", "last_name": "Souza"},
            "text": "Quanto custa para arrumar uma bomba?"
          }
        }
        req_t = urllib.request.Request(webhook_url, data=json.dumps(p5).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
        res_t = urllib.request.urlopen(req_t, context=ctx)
        resp_json = json.loads(res_t.read().decode('utf-8'))
        print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        
        time.sleep(15)
        # Test 6 — Duplicidade
        print("\n--- TEST 6: Duplicidade ---")
        print("[*] Repetindo a mensagem do Teste 1 com mesmo chat_id e message_id...")
        req_t = urllib.request.Request(webhook_url, data=json.dumps(p1).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
        res_t = urllib.request.urlopen(req_t, context=ctx)
        resp_json = json.loads(res_t.read().decode('utf-8'))
        print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        
        time.sleep(15)
        # Test 7 — Falha Supabase/IA Fallback
        print("\n--- TEST 7: Falha IA / Fallback ---")
        p7 = {
          "message": {
            "chat": {"id": 990011},
            "message_id": 4001,
            "from": {"first_name": "Test", "last_name": "Fallback"},
            "text": "Simular uma falha do motor."
          }
        }
        print("[*] Desativando temporariamente o Motor 002...")
        req_deact_002 = urllib.request.Request(n8n_host + "workflows/NgXUbJ96dXJqxGGX/deactivate", data=b'{}', headers=headers, method="POST")
        urllib.request.urlopen(req_deact_002, context=ctx)
        
        try:
            req_t = urllib.request.Request(webhook_url, data=json.dumps(p7).encode('utf-8'), headers={"Content-Type": "application/json"}, method="POST")
            res_t = urllib.request.urlopen(req_t, context=ctx)
            resp_json = json.loads(res_t.read().decode('utf-8'))
            print("Response:", json.dumps(resp_json, indent=2, ensure_ascii=False))
        finally:
            print("[*] Reativando o Motor 002...")
            req_act_002 = urllib.request.Request(n8n_host + "workflows/NgXUbJ96dXJqxGGX/activate", data=b'{}', headers=headers, method="POST")
            urllib.request.urlopen(req_act_002, context=ctx)
            
    finally:
        print("\n[*] Cleaning up temporary workflow...")
        req_deact = urllib.request.Request(n8n_host + f"workflows/{wf_id}/deactivate", data=b'{}', headers=headers, method="POST")
        try: urllib.request.urlopen(req_deact, context=ctx)
        except: pass
        req_del = urllib.request.Request(n8n_host + f"workflows/{wf_id}", headers=headers, method="DELETE")
        try: urllib.request.urlopen(req_del, context=ctx)
        except: pass
        print("[+] Temp workflow cleaned up.")

if __name__ == "__main__":
    run_tests()
