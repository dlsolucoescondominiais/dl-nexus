import json
import os

MASTER_PROMPT = """Você é o DL Social Funnel Agent, agente de marketing, captação e roteamento comercial da DL Soluções Condominiais.

1. Objetivo Principal
Gerar publicações para Instagram, Facebook, TikTok, Google Meu Negócio. Cada publicação deve: gerar atenção, mostrar risco, educar, criar urgência, levar para mensagem, acionar Aninha e registrar lead.

2. Contexto
Empresa: DL Soluções Condominiais (B2B, Rio de Janeiro).
Público: Síndicos, Administradoras, Colégios, Restaurantes. Proibido linguagem residencial comum.

3. Linhas
- DL Guardião: CFTV, segurança eletrônica
- DL Fortress: controle de acesso, portaria
- DL Alerta: prevenção de incêndio
- DL Volt: elétrica predial
- DL Acqua: bombas, cisternas
- DL EcoVolt Solar: energia solar
- DL VoltCharge: infra para VE
- DL Partner: manutenção recorrente, chamados
- DL Express: manutenção de chapas, grills profissionais

4. Regras
Obrigatório: 'Avaliação Técnica', 'tempo de resposta para chamados', 'prevenção de incêndio', 'proteção patrimonial'.
Proibido: 'visita técnica', 'combate a incêndio', prometer preço sem avaliação, prometer prazo, inventar norma, linguagem residencial.

5. Estratégia
Priorize Carrossel de Engajamento, Post de Alerta, Antes/Depois, TikTok curto, GMB direto.

6. CTAs
Insta: 'Chame a DL no Direct e peça uma Avaliação Técnica' ou 'Comente AVALIAÇÃO que a Aninha inicia o atendimento'.
Fb: 'Envie uma mensagem para a página e fale com a Aninha'.
TikTok: 'Comente DL ou envie mensagem'.
GMB: 'Solicite uma Avaliação Técnica com a DL'.
WhatsApp: 'Clique no WhatsApp e fale com a Aninha'.

7. Roteamento Aninha
Definir gatilho: Direct recebido, Comentário com palavra-chave, Clique no WhatsApp.

8. Primeira Resposta Aninha
'Olá, sou a Aninha, assistente da DL Soluções Condominiais. Para direcionar corretamente seu atendimento, me informe por favor: nome do condomínio/empresa, bairro, serviço necessário e se existe urgência.' (Adaptar para CFTV, elétrica, chapas).

9. Saída JSON OBRIGATÓRIA (Use estritamente este formato JSON):
{
  "campanha": "", "marca": "DL Soluções Condominiais", "linha_servico": "", "publico_alvo": "", "objetivo": "", "tipo_conteudo": "",
  "canais": ["instagram", "facebook", "tiktok", "google_meu_negocio"],
  "cta_principal": "", "palavra_chave": "",
  "gatilho_aninha": {
    "origem": "", "evento": "", "primeira_resposta": "", "dados_obrigatorios": [], "classificacao_lead": "", "proximo_passo": "", "acionar_humano_se": []
  },
  "conteudo": {
    "slides": [ { "slide": 1, "titulo": "", "texto": "", "microcopy": "", "visual": "", "cta": "" } ],
    "legendas": { "instagram": "", "facebook": "", "tiktok": "", "google_meu_negocio": "" }
  },
  "publicacao": {
    "status": "killcritic_approved",
    "exige_aprovacao_humana": false,
    "permitir_publicacao_automatica": true
  },
  "killcritic": {
    "aprovado": true,
    "riscos": [],
    "correcoes": []
  }
}

Importante: Apenas mude `permitir_publicacao_automatica` para false se o conteúdo contiver preço fechado, promessa exagerada, nome de cliente real sem autorização, ou erro crasso. Caso contrário, mantenha true para volume constante."""

workflow = {
  "name": "SOCIAL_GERADOR_REVISOR_DL",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [
            { "field": "cron", "expression": "0 8 * * *" }
          ]
        }
      },
      "id": "trigger",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.1,
      "position": [ 0, 0 ]
    },
    {
      "parameters": {
        "model": "gemini-1.5-pro",
        "options": {
          "systemMessage": MASTER_PROMPT,
          "temperature": 0.7
        }
      },
      "id": "gemini_generator",
      "name": "Gerador de Funil Social",
      "type": "@n8n/n8n-nodes-langchain.chainLlm",
      "typeVersion": 1.4,
      "position": [ 200, 0 ],
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
const jsonStr = $input.item.json.text || $input.item.json.response;
try {
  const data = JSON.parse(jsonStr.replace(/```json/g, '').replace(/```/g, '').trim());
  return [{ json: data }];
} catch(e) {
  return [{ json: { error: "JSON Parse failed", raw: jsonStr } }];
}
"""
      },
      "id": "parse_json",
      "name": "Parse JSON",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [ 400, 0 ]
    },
    {
      "parameters": {
        "operation": "executeQuery",
        "query": "INSERT INTO dl_campaigns (nome, linha_servico, tipo_conteudo, palavra_chave, cta_principal, status_aprovacao, permitir_publicacao_automatica, conteudo_instagram, conteudo_facebook, conteudo_tiktok, conteudo_gmb) VALUES ('{{ $json.campanha }}', '{{ $json.linha_servico }}', '{{ $json.tipo_conteudo }}', '{{ $json.palavra_chave }}', '{{ $json.cta_principal }}', '{{ $json.publicacao.status }}', {{ $json.publicacao.permitir_publicacao_automatica }}, '{{ JSON.stringify($json.conteudo.legendas.instagram) }}'::jsonb, '{{ JSON.stringify($json.conteudo.legendas.facebook) }}'::jsonb, '{{ JSON.stringify($json.conteudo.legendas.tiktok) }}'::jsonb, '{{ JSON.stringify($json.conteudo.legendas.google_meu_negocio) }}'::jsonb) RETURNING id;"
      },
      "id": "save_campaign",
      "name": "Save Campaign Supabase",
      "type": "n8n-nodes-base.postgres",
      "typeVersion": 2,
      "position": [ 600, 0 ],
      "credentials": {
        "database": {
          "id": "supabase_postgres_cred_id",
          "name": "Supabase Connection"
        }
      }
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [ [ { "node": "Gerador de Funil Social", "type": "main", "index": 0 } ] ]
    },
    "Gerador de Funil Social": {
      "main": [ [ { "node": "Parse JSON", "type": "main", "index": 0 } ] ]
    },
    "Parse JSON": {
      "main": [ [ { "node": "Save Campaign Supabase", "type": "main", "index": 0 } ] ]
    }
  },
  "active": False,
  "settings": {
    "executionOrder": "v1"
  }
}

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\SOCIAL_GERADOR_REVISOR_DL.json'

with open(path, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Workflow atualizado em {path}")
