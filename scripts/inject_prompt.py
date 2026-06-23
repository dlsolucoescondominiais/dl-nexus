import json

path = r'd:\AntiGravity\projeto_01\DL_NEXUS_V3_LOCAL\12_N8N_WORKFLOWS_PROXIMOS\206_AGENTE_REDATOR_PROPOSTA_LAUDO.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)

example = """
**TEMPLATE DE ESTRUTURA PARA A PROPOSTA CLIENTE:**
(Substitua os dados entre colchetes pelos reais do orçamento)

PROPOSTA COMERCIAL DE MANUTENÇÃO TÉCNICA
CONTRATADA:
DL Soluções Condominiais
CNPJ: 36.354.697/0001-46
Responsável Técnico: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura / CREA-RJ: 2022106230)
CONTRATANTE:
[Nome do Cliente]
[CNPJ do Cliente]
[Endereço do Cliente]

1. OBJETIVO
Prestação de serviço de mão de obra especializada para retrofit e manutenção corretiva em [X] equipamentos industriais, utilizando peças de reposição fornecidas previamente pela contratante.

2. ESCOPO TÉCNICO E INVESTIMENTO (MÃO DE OBRA)
● Equipamento 01 ([Modelo]): [Descrição exata da manutenção: Desmontagem, substituição de peças, calibração]. Valor: R$ [X]
● Equipamento 02 ([Modelo]): [Descrição exata da manutenção]. Valor: R$ [X]

3. CONDIÇÕES COMERCIAIS
● Investimento Total do Projeto: R$ [Soma]
● Inclusos: Mão de obra técnica especializada, todos os custos logísticos operacionais (deslocamento e estacionamento rotativo para os dias de imersão técnica no Centro do RJ) e emissão de Nota Fiscal.
● Isenções: A taxa de Avaliação Técnica foi integralmente abonada na composição deste pacote.
● Condição de Pagamento: A combinar.

4. GARANTIA TÉCNICA
Serviço executado com rigor técnico, garantindo a integridade da montagem, instalação e segurança do circuito elétrico refeito. A garantia contra defeitos de fabricação dos componentes eletrônicos e mecânicos instalados permanece sob total responsabilidade do fabricante/fornecedor das peças.
"""

for node in data.get('nodes', []):
    if node.get('name') == 'API LLM':
        # Safely replace the json string
        body_str = node['parameters']['jsonBody']
        body_json = json.loads(body_str)
        # Assuming the first message is the system prompt
        original_prompt = body_json['messages'][0]['content']
        # Evitar duplicar
        if "TEMPLATE DE ESTRUTURA PARA A PROPOSTA CLIENTE" not in original_prompt:
            new_prompt = original_prompt + "\n\nSiga EXATAMENTE a estrutura abaixo na sua redação da Proposta Cliente:\n" + example
            body_json['messages'][0]['content'] = new_prompt
            node['parameters']['jsonBody'] = json.dumps(body_json, ensure_ascii=False)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated 206')
