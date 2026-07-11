"""
[DEPRECATED] Manus.IA removido do ecossistema DL Nexus.
Este script foi desativado.
"""
import sys
from utils.n8n_api import n8n_request

sys.exit("Script obsoleto. Manus.IA foi removido.")

import os
import json
import urllib.request
import urllib.error

ENV_FILE = r"d:\AntiGravity\projeto_01\.env"
# 1. Atualizar Workflow 070 (Manus)
wf_070, err = n8n_request("workflows/UBH2RWc3CK2AyVR3")
if err or not wf_070:
    print(f"Erro ao buscar 070: {err}")
else:
    for node in wf_070.get("nodes", []):
        if node["name"] == "Preparar Prompt Diário":
            node["parameters"]["jsCode"] = """
const date = new Date().toLocaleDateString('pt-BR');
return {
  json: {
    prompt: `Você é Manus AI, o Diretor de Marketing B2B da DL Soluções Condominiais.
Hoje é dia ${date}. Vasculhe e pense em condomínios pequenos/médios, colégios e restaurantes na zona e região do Rio de Janeiro.
Sua missão: Gerar a estratégia do dia de postagem para o Agente MarkSolar (Copywriter).
A estratégia DEVE focar em um ou mais de nossos produtos chave: DL Fortress, DL Guardião e DL Acqua.

Você DEVE retornar sua saída estritamente em um JSON válido com a seguinte estrutura:
{
  "estrategia_texto": "Descreva o gancho, a dor do público e o tom que o MarkSolar deve usar no post.",
  "produto": "Nome do produto foco",
  "publico_alvo": "Ex: Síndicos de pequenos condomínios",
  "bairro": "Ex: Zona Sul, Barra ou Tijuca",
  "canal_destino": "Instagram, Facebook e TikTok",
  "objetivo": "Agendar Avaliação Técnica"
}`
  }
};
"""
        elif node["name"] == "HTTP Request Manus API":
            node["parameters"]["bodyParameters"]["parameters"][1]["value"] = "[{\"role\": \"user\", \"content\": \"{{ $json.prompt }}\"}]"
            # Precisamos extrair o JSON da resposta
            node["parameters"]["options"] = {"response": {"response": {"responseFormat": "json"}}}
            
        elif node["name"] == "Telegram Entrega":
            node["parameters"]["text"] = "🎯 *DIRETRIZ B2B DO MANUS GERADA E ENVIADA AO MARKSOLAR*\\n\\n*Público:* {{ $json.publico_alvo }}\\n*Produto:* {{ $json.produto }}\\n*Região:* {{ $json.bairro }}\\n\\n*Estratégia:* {{ $json.estrategia_texto }}"

    # Vamos adicionar um nó "Parse JSON Manus" porque às vezes a LLM devolve com markdown ```json
    parse_node = {
        "parameters": {
            "jsCode": """
let content = $input.all()[0].json.choices[0].message.content;
if(content.includes('```json')) {
    content = content.replace(/```json/g, '').replace(/```/g, '').trim();
}
try {
    return { json: JSON.parse(content) };
} catch(e) {
    return { json: { estrategia_texto: content, produto: "DL Guardião", publico_alvo: "Síndicos", bairro: "Rio de Janeiro" } };
}
"""
        },
        "id": "parse_manus_json",
        "name": "Limpar JSON do Manus",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [600, 100]
    }

    execute_020_node = {
        "parameters": {
            "workflowId": "publicadorSocialDlNexusV320260518",
            "mode": "wait"
        },
        "id": "call_020",
        "name": "Chamar MarkSolar (020)",
        "type": "n8n-nodes-base.executeWorkflow",
        "typeVersion": 1,
        "position": [800, 100]
    }

    # Reestruturar nodes
    wf_070["nodes"] = [n for n in wf_070["nodes"] if n["name"] not in ["Limpar JSON do Manus", "Chamar MarkSolar (020)", "Telegram Entrega"]]
    
    telegram_node = [n for n in wf_070["nodes"] if n["name"] == "Telegram Entrega"]
    if not telegram_node:
        telegram_node = [{
            "parameters": {
                "chatId": "-1002012015091",
                "text": "🎯 *DIRETRIZ B2B DO MANUS GERADA E ENVIADA AO MARKSOLAR*\\n\\n*Público:* {{ $json.publico_alvo }}\\n*Produto:* {{ $json.produto }}\\n*Região:* {{ $json.bairro }}\\n\\n*Estratégia:* {{ $json.estrategia_texto }}",
                "additionalFields": {"parse_mode": "Markdown"}
            },
            "id": "send_telegram",
            "name": "Telegram Entrega",
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.1,
            "position": [800, -100],
            "credentials": {"telegramApi": {"id": "R4tW3uI2z7P9X1vL", "name": "Conta do Telegram"}}
        }]
    else:
        telegram_node = telegram_node[0]
        telegram_node["position"] = [800, -100]

    wf_070["nodes"].extend([parse_node, execute_020_node, telegram_node])

    # Refazer conexões
    wf_070["connections"]["HTTP Request Manus API"] = {
        "main": [[{"node": "Limpar JSON do Manus", "type": "main", "index": 0}]]
    }
    wf_070["connections"]["Limpar JSON do Manus"] = {
        "main": [
            [{"node": "Chamar MarkSolar (020)", "type": "main", "index": 0}, {"node": "Telegram Entrega", "type": "main", "index": 0}]
        ]
    }

    res, err = n8n_request("workflows/UBH2RWc3CK2AyVR3", method="PUT", data=wf_070)
    if err:
        print(f"Erro PUT 070: {err}")
    else:
        print("Workflow 070 atualizado!")

# 2. Atualizar Workflow 020 (MarkSolar)
wf_020, err = n8n_request("workflows/publicadorSocialDlNexusV320260518")
if err or not wf_020:
    print(f"Erro ao buscar 020: {err}")
else:
    for node in wf_020.get("nodes", []):
        if node["name"] == "Gerar Textos IA":
            # Atualizar link da Aninha e pegar input do Execute Workflow (que entra no root via Entrada do Post ou direto)
            # Como o Execute Workflow envia direto pro primeiro nó que não tem input (ou Execute Workflow Trigger), o payload vai estar lá.
            node["parameters"]["messages"]["messageValues"][1]["content"] = """={{ 'A Estratégia Ditada pelo Manus AI é:\\n\\n' + JSON.stringify($json) + '\\n\\nCanais Oficiais DL Soluções (use sempre no CTA):\\n- Site: https://dlsolucoescondominiais.com\\n- Instagram: https://www.instagram.com/dl.solucoescondominiais/\\n- WhatsApp da Aninha (CTA Principal): https://wa.me/5521964742439?text=Quero+agendar+uma+Avaliação+Técnica\\n\\nRegras obrigatórias:\\n- O CTA DEVE sempre ser "Avaliação Técnica" e direcionar pro WhatsApp da Aninha final 39.\\n- NUNCA prometer "visita técnica".\\n- Alvo: síndicos, colégios e pequenos/médios condomínios do RJ.\\n\\nForneça a resposta em JSON estrito com as chaves: legenda_facebook, legenda_instagram, texto_telegram, hashtags, cta' }}"""
            
    # Garantir que 020 comece com Webhook e Execute Workflow Trigger
    has_ewt = any(n["type"] == "n8n-nodes-base.executeWorkflowTrigger" for n in wf_020["nodes"])
    if not has_ewt:
        ewt_node = {
            "parameters": {},
            "id": "execute_workflow_trigger",
            "name": "Execute Workflow Trigger",
            "type": "n8n-nodes-base.executeWorkflowTrigger",
            "typeVersion": 1,
            "position": [-200, 200]
        }
        wf_020["nodes"].append(ewt_node)
        wf_020["connections"]["Execute Workflow Trigger"] = {
            "main": [[{"node": "Gerar Textos IA", "type": "main", "index": 0}]]
        }

    res, err = n8n_request("workflows/publicadorSocialDlNexusV320260518", method="PUT", data=wf_020)
    if err:
        print(f"Erro PUT 020: {err}")
    else:
        print("Workflow 020 atualizado!")

