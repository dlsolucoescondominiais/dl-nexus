# RELATÓRIO: TESTES DE PRECIFICAÇÃO (WORKFLOW 179)

## Objetivo
Documentar os casos de teste estipulados para validar o Motor de Precificação DL Nexus. O workflow 179 (`179_TESTES_PRECIFICACAO.json`) foi construído com a finalidade de injetar os 6 payloads de testes listados abaixo e assegurar a resposta correta dos módulos 170-178.

## Payloads de Teste Implementados (Mocks)

### 1. Multgrill Zona Sul
- **Categoria:** Gastronomia
- **Equipamento:** Chapas e Fritadeiras
- **Local:** Zona Sul
- **Urgência:** Alta
- **Comportamento Esperado:** Identificar o serviço como altíssima prioridade, aplicando fator multiplicador pesado de urgência e direcionando atendimento imediato.

### 2. Chapa Emergência
- **Categoria:** Gastronomia
- **Equipamento:** Chapa
- **Local:** Centro
- **Urgência:** Emergência
- **Comportamento Esperado:** Custo agressivo para deslocamento emergencial. Confirmação do multiplicador para maquinário crítico parado.

### 3. Fortress Barra 300und
- **Categoria:** Controle de Acesso
- **Sistema:** Fortress
- **Local:** Barra da Tijuca
- **Unidades:** 300
- **Comportamento Esperado:** Garantir que o nome Fortress seja validado com sucesso e que a precificação faça a correta relação de volume (300 unidades). Se faltarem dados do cabeamento, deve acionar "Sob Avaliação Técnica".

### 4. SLA CFTV Pequeno
- **Categoria:** CFTV
- **Porte:** Pequeno
- **Câmeras:** 8
- **Local:** Tijuca
- **Comportamento Esperado:** Fornecimento de faixa de preço recorrente (contrato SLA) com imposto_estimado_percentual.

### 5. Elétrica Madrugada
- **Categoria:** Elétrica
- **Horário:** Madrugada
- **Urgência:** Emergência
- **Local:** Copacabana
- **Comportamento Esperado:** Aplicação dos adicionais noturnos e de emergência sobre o quadro elétrico de bombas.

### 6. Dados Incompletos
- **Categoria:** Vazia / Indefinida
- **Equipamento:** Não informado
- **Local:** Não informado
- **Comportamento Esperado:** O motor deve identificar a falta de parâmetros críticos e travar o orçamento, emitindo imediatamente o status "Sob Avaliação Técnica" sem retornar valores zerados ou errôneos.

## Status de Deploy
O workflow foi injetado (active=false) e sincronizado com os ambientes locais. Para testar, basta acioná-lo manualmente ou via console n8n.

---
*Relatório gerado automaticamente pelo Engenheiro de Integração DL Nexus V3.*
