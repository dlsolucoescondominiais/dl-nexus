# RELATÓRIO INTERNO DE ANÁLISE TÉCNICA E COMERCIAL — ECOVOLT
**Protocolo:** {{ $json.protocolo }}
**Versão Atual:** {{ $json.versao_status }} (ex: V1, V2)

---

## 1. CUSTOS ESTIMADOS
- **Custo Insumos / Equipamentos SolaX/Baterias:** R$ {{ $json.financeiro.custos_estimados_equipamentos.toFixed(2) }}
- **Custo Logística / Impostos:** R$ {{ $json.financeiro.logistica_impostos.toFixed(2) }}
- **Custo Instalação e Homologação (Homem-Hora):** R$ {{ $json.financeiro.custo_instalacao_estimado.toFixed(2) }}
- **Custo Total Estimado (C.O.GS):** R$ {{ ($json.financeiro.custos_estimados_equipamentos + $json.financeiro.logistica_impostos + $json.financeiro.custo_instalacao_estimado).toFixed(2) }}

## 2. FORNECEDOR
- **Parceiro Fornecedor Principal:** Corsolar (Distribuição SolaXPower Oficial Brasil)
- **Status Comercial:** Distribuição direta do distribuidor no RJ.
- **Validade Preços Fornecedor:** Sujeito a consulta de cotação diária.

## 3. MODELO SUGERIDO
- **Inversor:** {{ $json.dimensionamento_backup_calculado.inversor_sugerido }}
- **Banco de Baterias:** Baterias Triple Power LFP sugeridas para banco nominal de {{ $json.dimensionamento_backup_calculado.bateria_nominal_banco_kwh }} kWh.
- **Módulos Solares:** Monocristalinos de alta performance compatíveis com o arranjo kWp.

## 4. PREÇO MÁXIMO DE COMPRA (META DE COMPRA INTERNA)
- **Inversor Metas de Compra:** R$ {{ ($json.financeiro.custos_estimados_equipamentos * 0.45).toFixed(2) }}
- **Banco de Baterias Metas de Compra:** R$ {{ ($json.financeiro.custos_estimados_equipamentos * 0.55).toFixed(2) }}
- *Aviso: Os preços de compra de equipamentos reais devem ser obtidos de cotações diretas no portal da Corsolar, marcados como "estimados para validação" antes do fechamento definitivo.*

## 5. MARGEM
- **Margem Bruta (Margem de Contribuição):** {{ $json.financeiro.margem_bruta_porcentagem }}%
- **Markup Aplicado:** {{ (1 / (1 - ($json.financeiro.margem_bruta_porcentagem / 100))).toFixed(2) }}
- **Valor Final de Venda Proposto:** R$ {{ $json.financeiro.valor_final_estimado.toFixed(2) }}

## 6. RISCO TÉCNICO
- **Instalação física:** Telhado/laje e espaço ventilado para baterias (peso e calor).
- **Adequação Elétrica:** Necessidade de verificar distância e compatibilidade física no QGBT (Quadro Geral de Baixa Tensão).
- **Motores em Backup:** Risco técnico crítico caso motores operem sem soft-starter ou inversor de frequência (bloqueia dimensionamento automático).

## 7. RISCO COMERCIAL
- Risco de flutuação de estoque da Corsolar.
- Expectativa de economia pelo cliente baseada na tarifa (Fio B e tarifa de disponibilidade da rede).
- Risco de subdimensionamento das cargas críticas pelo próprio cliente (necessidade de medições em campo).

## 8. PENDÊNCIAS
Lista de pendências comerciais e técnicas que devem ser tratadas pelo consultor comercial DL:
{{#each $json.compliance_killcritic.pendencias_criticas}}
- [ ] {{this}}
{{/each}}

## 9. ESTRATÉGIA DE NEGOCIAÇÃO
- **Primeiro passo:** Agendar a **Avaliação Técnica presencial obrigatória**.
- **Apresentação de valor:** Focar na resiliência energética do condomínio/empresa (SLA de funcionamento das portarias, bombas e CFTV) e na previsibilidade das despesas fixas.
- **Limite de Desconto:** Não praticar descontos sobre a margem de engenharia de instalação sem aprovação da diretoria (Diogo/Nielton).

## 10. HISTÓRICO DE VERSÕES
- **Versões e Modificações Registradas:**
  - V1: Versão inicial gerada automaticamente pelo Motor Solar.
  - V2: Revisão do KILLCRITIC técnico/comercial.
  - V3: Ajustes e validações manuais realizadas em campo.

## 11. RECOMENDAÇÃO KILLCRITIC
- **Decisão do Auditor:** {{ $json.compliance_killcritic.status_killcritic }}
- **Nível de Risco:** Risco {{ $json.compliance_killcritic.risco_killcritic }}
- **Motivos de Bloqueio Encontrados:**
{{#each $json.compliance_killcritic.motivos_bloqueio}}
  - {{this}}
{{/each}}
