import json
import os

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json'

with open(path, 'r', encoding='utf-8') as f:
    wf = json.load(f)

# ──────────────────────────────────────────────────────────────────
# 1. CORRIGIR PROMPT — nomes comerciais oficiais + foco comercial
# ──────────────────────────────────────────────────────────────────
novo_prompt_js = r'''const d = new Date().toLocaleDateString("pt-BR");

const prompt = `Você é Manus AI, o Diretor de Marketing B2B da DL Soluções Condominiais.
Hoje é dia ${d}. Sua missão: gerar a estratégia do dia de postagem para o Agente MarkSolar (Copywriter).

PRODUTOS OFICIAIS DA DL (usar exatamente esses nomes):
- DL Guardião: segurança eletrônica, CFTV, câmeras, proteção patrimonial
- DL Fortress: portaria autônoma, gestão de acesso
- DL GateKeeper: automação de portões
- DL Acqua: cisternas, caixas d'água, bombas, automação hídrica
- DL Volt: elétrica condominial, quadros, painéis, infraestrutura elétrica
- DL EcoVolt: energia solar on-grid, híbrida, off-grid
- DL Alerta: prevenção de incêndio, centrais, detectores
- DL Partner: manutenção continuada Basic/Master/Premium
- DL Suporte Grill's: atendimento técnico para equipamentos da linha Mult•Grill Express e similares

FOCO COMERCIAL PRIORITÁRIO:
- Receita recorrente rápida via DL Partner
- Condomínios verticais pequenos e médios (até 400 unidades)
- Condomínios antigos com infraestrutura defasada
- Condomínios de baixa e média renda, populares, Minha Casa Minha Vida
- Administradoras pequenas e médias
- Restaurantes, hamburguerias e lanchonetes para DL Suporte Grill's

REGIÕES: Rio de Janeiro — Zona Sul, Zona Norte, Zona Oeste, Barra, Recreio, Jacarepaguá, Tijuca, Centro, Niterói, São Gonçalo, Duque de Caxias, Nova Iguaçu.

REGRAS ABSOLUTAS:
- Nunca usar "visita técnica". Usar "Avaliação Técnica".
- Nunca citar Condfy.
- Nunca chamar Diogo de engenheiro. Usar "Tecnólogo Responsável".
- CTA principal: https://dlsolucoescondominiais.com
- CTA WhatsApp: https://wa.me/5521964742458

OBJETIVO FINAL: Gerar lead para Avaliação Técnica.

Retorne JSON com os campos: modo, estrategia_texto, produto, publico_alvo, perfil_condominio, bairro, dor_principal, oferta, angulo_comercial, canal_destino, objetivo, nivel_de_urgencia, cta.`;

return { json: { prompt: prompt } };'''

# ──────────────────────────────────────────────────────────────────
# 2. CORRIGIR structured_output_schema — campos expandidos
# ──────────────────────────────────────────────────────────────────
novo_schema = {
    "type": "object",
    "properties": {
        "modo": {"type": "string", "description": "economico"},
        "estrategia_texto": {"type": "string", "description": "Descreva o gancho, a dor do público e o tom que o MarkSolar deve usar no post."},
        "produto": {"type": "string", "description": "Nome do produto foco (ex: DL Partner, DL Guardião, DL Volt)"},
        "publico_alvo": {"type": "string", "description": "Ex: Síndicos de pequenos condomínios"},
        "perfil_condominio": {"type": "string", "description": "Ex: Vertical até 100 unidades, antigo, baixa renda"},
        "bairro": {"type": "string", "description": "Ex: Zona Sul, Barra ou Tijuca"},
        "dor_principal": {"type": "string", "description": "Ex: Fiação antiga, câmeras paradas, portaria cara"},
        "oferta": {"type": "string", "description": "Ex: Avaliação Técnica gratuita + plano DL Partner Basic"},
        "angulo_comercial": {"type": "string", "description": "Ex: Economia, segurança, valorização do imóvel"},
        "canal_destino": {"type": "string", "description": "Instagram, Facebook e TikTok"},
        "objetivo": {"type": "string", "description": "Gerar lead para Avaliação Técnica"},
        "nivel_de_urgencia": {"type": "string", "description": "Ex: alto, médio, baixo"},
        "cta": {"type": "string", "description": "Solicite uma Avaliação Técnica pelo WhatsApp da DL"}
    },
    "required": [
        "modo", "estrategia_texto", "produto", "publico_alvo",
        "perfil_condominio", "bairro", "dor_principal", "oferta",
        "angulo_comercial", "canal_destino", "objetivo",
        "nivel_de_urgencia", "cta"
    ]
}

# ──────────────────────────────────────────────────────────────────
# 3. APLICAR CORREÇÕES NOS NODES
# ──────────────────────────────────────────────────────────────────
for node in wf['nodes']:
    # Corrigir o prompt
    if node['name'] == 'Preparar Prompt Diário':
        node['parameters']['jsCode'] = novo_prompt_js

    # Corrigir o body do task.create (schema + agent_profile)
    if node['name'] == 'HTTP Request Manus API':
        novo_body = {
            "prompt": "={{$json.prompt}}",
            "agent_profile": "manus-1.6-lite",
            "interactive_mode": False,
            "structured_output_schema": novo_schema
        }
        node['parameters']['jsonBody'] = json.dumps(novo_body, ensure_ascii=False)

# ──────────────────────────────────────────────────────────────────
# 4. VALIDAÇÃO ANTES DE SALVAR
# ──────────────────────────────────────────────────────────────────
raw = json.dumps(wf, ensure_ascii=False)

checks = {
    'api.manus.ai/v2': raw.count('api.manus.ai/v2'),
    'api.manus.gg': raw.count('api.manus.gg'),
    'x-manus-api-key': raw.count('x-manus-api-key'),
    'Authorization Bearer': raw.count('Authorization'),
    'task.create': raw.count('task.create'),
    'task.detail': raw.count('task.detail'),
    'task.listMessages': raw.count('task.listMessages'),
    'manus-1.6-lite': raw.count('manus-1.6-lite'),
    'interactive_mode': raw.count('interactive_mode'),
    'structured_output_schema': raw.count('structured_output_schema'),
    'DL Fortress': raw.count('DL Fortress'),
    'DL GateKeeper': raw.count('DL GateKeeper'),
    'DL Suporte Grill': raw.count('DL Suporte Grill'),
    'Mult-Grill Express como marca DL': raw.count('"Mult'),
    'Fortress isolado': 0,
    'perfil_condominio': raw.count('perfil_condominio'),
    'dor_principal': raw.count('dor_principal'),
    'angulo_comercial': raw.count('angulo_comercial'),
}

# Check for isolated 'Fortress' (not preceded by 'DL ')
import re
fortress_isolated = len(re.findall(r'(?<!DL )Fortress', raw))

errors = []
if checks['api.manus.gg'] > 0:
    errors.append('ERRO: api.manus.gg encontrado')
if checks['Authorization Bearer'] > 0:
    errors.append('ERRO: Authorization Bearer encontrado')
if checks['api.manus.ai/v2'] < 3:
    errors.append('ERRO: api.manus.ai/v2 insuficiente')
if checks['x-manus-api-key'] < 3:
    errors.append('ERRO: x-manus-api-key insuficiente')
if checks['manus-1.6-lite'] < 1:
    errors.append('ERRO: manus-1.6-lite ausente')
if checks['DL Fortress'] < 1:
    errors.append('ERRO: DL Fortress ausente')
if checks['DL GateKeeper'] < 1:
    errors.append('ERRO: DL GateKeeper ausente')
if checks['DL Suporte Grill'] < 1:
    errors.append('ERRO: DL Suporte Grill ausente')
if checks['perfil_condominio'] < 1:
    errors.append('ERRO: perfil_condominio ausente no schema')

if errors:
    for e in errors:
        print(e)
    print('ABORTANDO — correções insuficientes.')
    exit(1)

# ──────────────────────────────────────────────────────────────────
# 5. SALVAR NAS 3 PASTAS
# ──────────────────────────────────────────────────────────────────
paths = [
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\070_CRON_MANUS_DIARIO.json',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\20_UPLOAD_N8N\070_CRON_MANUS_DIARIO.json',
    r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\09_PRONTOS_PARA_PRODUCAO\070_CRON_MANUS_DIARIO.json'
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)

print('OK: JSON salvo nas 3 pastas.')
for k, v in checks.items():
    print(f'  {k}: {v}')
print(f'  Fortress isolado (sem DL): {fortress_isolated}')
print(f'  Nodes: {len(wf["nodes"])}')
print(f'  Total erros: 0')
