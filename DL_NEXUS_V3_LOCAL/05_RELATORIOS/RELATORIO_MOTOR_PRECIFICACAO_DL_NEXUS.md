# RELATÓRIO: MOTOR DE PRECIFICAÇÃO DL NEXUS (170-179)

## Visão Geral
Este documento relata a estrutura e as diretrizes do Motor de Precificação (workflows 170 ao 179) da DL Soluções Condominiais, desenvolvido para o sistema automatizado n8n (DL Nexus V3).

## Arquitetura
O Motor de Precificação atua como um core-system do DL Nexus, recebendo solicitações de "Avaliação Técnica" ou orçamentos diretos para os condomínios clientes. Todo o cálculo baseia-se num fluxo multi-estágios:
- Recebimento de Payload de Entrada
- Triagem de Categoria (Gastronomia, CFTV, Elétrica, Controle de Acesso, etc)
- Aplicação de Fatores de Multiplicação (Urgência, Localização, Complexidade, etc)
- Validação e Aplicação de Impostos ("imposto_estimado_percentual")
- Formatação de Proposta ou Direcionamento para "Sob Avaliação Técnica"

## Regras de Negócio e Restrições Atendidas
1. **Terminologia Rigorosa:**
   - Proibido o uso de "visita técnica"; utilizado estritamente "Avaliação Técnica".
   - A solução de controle de acesso foi atualizada para "Fortress" (Condfy banido).
   - O cargo de "Engenheiro" não é usado; utilizado o título de "Tecnólogo Responsável" para o especialista técnico.

2. **Sigilo de Custos:**
   - O custo interno não é exposto. A proposta apresenta apenas a faixa comercial de investimento e o preço recomendado final.

3. **Gatilhos de Avaliação:**
   - Caso faltem dados estruturais ou parâmetros críticos de precificação, o sistema aborta o orçamento automático e emite o status: "Sob Avaliação Técnica".

4. **Tratamento de Urgência (Gastronomia):**
   - Atendimentos voltados para gastronomia (chapas, fritadeiras, etc) possuem multiplicador de urgência elevado e são priorizados dentro do pipeline operacional.

## Workflows Relacionados
- 170 a 178: Componentes lógicos de triagem, cálculo e validação.
- 179: Workflow exclusivo de testes (Mock Payloads) para auditar a precisão do Motor de Precificação.

---
*Relatório gerado automaticamente pelo Engenheiro de Automação n8n residente do Antigravity (DL Nexus).*
