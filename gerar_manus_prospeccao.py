from pathlib import Path
import json

BASE = Path("DL_NEXUS_V3_LOCAL") / "11_N8N_AGENTES_V3"
BASE.mkdir(parents=True, exist_ok=True)

def salvar_json(nome, conteudo):
    path = BASE / nome
    path.write_text(json.dumps(conteudo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✔️ OK JSON: {path}")

def workflow_manus_prospeccao():
    code_prompt = r'''
const lead = $json.body || $json;

const nome_condominio = lead.nome || "Condomínio";
const bairro = lead.bairro || "Rio de Janeiro";
const foco_produto = lead.produto_foco || "Fortress"; // Pode ser Fortress, DL Acqua ou Gatekeeper

let contexto_produto = "";
if(foco_produto === "Fortress") contexto_produto = "gestão de acesso, portaria autônoma e controle de entrada via Condfy";
if(foco_produto === "DL Acqua") contexto_produto = "monitoramento de cisternas, prevenção de transbordamento e automação de bombas via Metabo";
if(foco_produto === "Gatekeeper") contexto_produto = "automação de portões e acesso bluetooth/wireless via Mobgate";

const system_prompt = `Você é o Agente Manus, o SDR (Representante de Desenvolvimento de Vendas) da DL Soluções Condominiais.
Sua missão é escrever UMA mensagem de WhatsApp de prospecção (outbound) para o síndico ou gestor do ${nome_condominio}, localizado em ${bairro}.

REGRAS RÍGIDAS (KILLCRITIC):
1. A mensagem deve ser curta, amigável e extremamente profissional. Não pareça um robô de spam.
2. Não tente vender o produto de cara. O objetivo é iniciar uma conversa.
3. Mencione sutilmente que a DL Soluções é especialista em ${contexto_produto}.
4. O Call to Action (CTA) final deve ser um convite para uma "Avaliação Técnica" sem compromisso para entender a infraestrutura atual deles.
5. NUNCA use a expressão "visita técnica". Use apenas "Avaliação Técnica".
6. NUNCA cite preços ou fale sobre "canaleta plástica".
7. Formate com espaçamento para facilitar a leitura no WhatsApp e use no máximo 2 emojis.`;

return [{
  json: {
    telefone_destino: lead.telefone,
    system_prompt: system_prompt,
    prompt_usuario: `Escreva a mensagem de abordagem inicial para o ${nome_condominio}.`
  }
}];
'''
    return {
        "name": "060_AGENT_MANUS_PROSPECCAO_ATIVA",
        "nodes": [
            {
                "parameters": {
                    "path": "manus-outbound-trigger",
                    "httpMethod": "POST",
                    "responseMode": "onReceived",
                    "options": {}
                },
                "id": "webhook_manus",
                "name": "Receber Lead do Google Maps",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [200, 300]
            },
            {
                "parameters": {"jsCode": code_prompt},
                "id": "preparar_prompt",
                "name": "Preparar Abordagem (SDR)",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [460, 300]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://api.openai.com/v1/chat/completions",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {"name": "Authorization", "value": "Bearer {SUA_CHAVE_OPENAI_AQUI}"},
                            {"name": "Content-Type", "value": "application/json"}
                        ]
                    },
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {"name": "model", "value": "gpt-4o-mini"},
                            {"name": "messages", "value": "={{ [\n  {\n    \"role\": \"system\",\n    \"content\": $json.system_prompt\n  },\n  {\n    \"role\": \"user\",\n    \"content\": $json.prompt_usuario\n  }\n] }}"}
                        ]
                    },
                    "options": {}
                },
                "id": "gerar_texto_ia",
                "name": "IA Escreve a Mensagem",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [720, 300]
            },
            {
                "parameters": {
                    "method": "POST",
                    "url": "https://graph.facebook.com/v19.0/{SEU_PHONE_NUMBER_ID}/messages",
                    "sendHeaders": True,
                    "headerParameters": {
                        "parameters": [
                            {"name": "Authorization", "value": "Bearer {SEU_ACCESS_TOKEN_PERMANENTE}"},
                            {"name": "Content-Type", "value": "application/json"}
                        ]
                    },
                    "sendBody": True,
                    "bodyParameters": {
                        "parameters": [
                            {"name": "messaging_product", "value": "whatsapp"},
                            {"name": "recipient_type", "value": "individual"},
                            {"name": "to", "value": "={{ $('Preparar Abordagem (SDR)').item.json.telefone_destino }}"},
                            {"name": "type", "value": "text"},
                            {"name": "text", "value": "={{ { \"body\": $json.choices[0].message.content } }}"}
                        ]
                    },
                    "options": {}
                },
                "id": "disparo_meta_api",
                "name": "Disparar WhatsApp (Meta API)",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 4.1,
                "position": [980, 300]
            }
        ],
        "connections": {
            "Receber Lead do Google Maps": {
                "main": [[{"node": "Preparar Abordagem (SDR)", "type": "main", "index": 0}]]
            },
            "Preparar Abordagem (SDR)": {
                "main": [[{"node": "IA Escreve a Mensagem", "type": "main", "index": 0}]]
            },
            "IA Escreve a Mensagem": {
                "main": [[{"node": "Disparar WhatsApp (Meta API)", "type": "main", "index": 0}]]
            }
        },
        "active": False,
        "settings": {"executionOrder": "v1"},
        "tags": [{"name": "DL_NEXUS_V3"}, {"name": "MANUS_PROSPECCAO"}]
    }

salvar_json("060_AGENT_MANUS_PROSPECCAO_ATIVA.json", workflow_manus_prospeccao())

print("")
print("🚀 MÓDULO DE PROSPECÇÃO 'MANUS' GERADO COM SUCESSO.")
print("O arquivo foi salvo na sua Zona de Quarentena.")
