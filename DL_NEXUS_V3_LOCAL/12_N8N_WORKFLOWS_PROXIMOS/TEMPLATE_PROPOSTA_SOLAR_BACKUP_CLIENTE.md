# PROPOSTA COMERCIAL PRELIMINAR — SOLUÇÃO ECOVOLT (SOLAR HÍBRIDO & BACKUP DE BATERIAS)
**Protocolo:** {{ $json.protocolo }}
**Data de Emissão:** {{ new Date().toLocaleDateString('pt-BR') }}

---

## 1. TÍTULO
**Estudo de Pré-Dimensionamento de Sistema Solar Fotovoltaico Híbrido com Armazenamento de Energia para Cargas Críticas**

## 2. IDENTIFICAÇÃO DO CLIENTE
- **Cliente / Condomínio:** {{ $json.cliente.nome }}
- **Tipo de Cliente:** {{ $json.cliente.tipo_cliente }}
- **Responsável / Decisor:** {{ $json.cliente.responsavel }}
- **Local de Instalação:** {{ $json.cliente.endereco }}, {{ $json.cliente.bairro }} - {{ $json.cliente.cidade }}/RJ
- **Contato:** {{ $json.cliente.whatsapp }} / {{ $json.cliente.email }}

## 3. OBJETIVO DA SOLUÇÃO
Prover resiliência energética contínua para cargas essenciais do cliente por meio de armazenamento de bateria de lítio integrado a sistema gerador fotovoltaico híbrido. O foco reside na autonomia durante falhas da concessionária de energia e na otimização do perfil de consumo, operando de forma autônoma e segura.

## 4. DIAGNÓSTICO PRELIMINAR
Com base no histórico médio de consumo de **{{ $json.dados_conta.consumo_mensal_kwh }} kWh/mês** e no custo financeiro informado, identificou-se a demanda para contingência das cargas críticas pré-selecionadas e a viabilidade técnica de microgeração fotovoltaica complementar para redução do consumo elétrico da rede da concessionária.

## 5. PREMISSAS TÉCNICAS
- **Tensão de Atendimento:** {{ $json.dados_eletricos.tensao }} V
- **Padrão de Ligação:** {{ $json.dados_eletricos.tipo_ligacao }}
- **Disjuntor Geral:** {{ $json.dados_eletricos.disjuntor_geral }} A
- **Autonomia de Backup Solicitada:** {{ $json.autonomia_desejada_horas }} horas
- **Parâmetros Técnicos Básicos:** Eficiência do sistema de 85% e Profundidade de Descarga (DoD) de 80% para baterias de fosfato de ferro-lítio (LFP).

## 6. CARGAS CRÍTICAS CONSIDERADAS
Lista de cargas essenciais integradas ao circuito de backup preliminar:
{{#each $json.cargas_criticas}}
- **{{this.nome_carga}}:** {{this.potencia_w}} W | Qtd: {{this.quantidade}} | Uso diário: {{this.horas_uso_diario}}h {{#if this.motor}}| *Motor com pico de partida (requer análise específica)*{{/if}}
{{/each}}
- **Potência Crítica Instalada:** {{ $json.dimensionamento_backup_calculado.potencia_critica_total_kw }} kW
- **Potência de Simultaneidade Estimada:** {{ $json.dimensionamento_backup_calculado.potencia_critica_simultanea_kw }} kW
- **Consumo Energético Diário Crítico:** {{ $json.dimensionamento_backup_calculado.energia_critica_diaria_kwh }} kWh/dia

## 7. ESTIMATIVA DE SISTEMA SOLAR
- **Arranjo Fotovoltaico Preliminar:** {{ $json.dimensionamento_solar_calculado.sistema_solar_kwp_preliminar }} kWp
- **Geração Média Estimada:** {{ $json.dimensionamento_solar_calculado.geracao_mensal_estimada_kwh }} kWh/mês
- **Redução Estimada de Consumo:** Estimativa de redução de consumo da rede da concessionária, sujeita à análise final da conta de energia, irradiação local efetiva, perfil de consumo de cargas, homologação e tarifas. **Não há promessa ou garantia de economia fixa.**

## 8. ESTIMATIVA DE BACKUP COM BATERIAS
- **Energia Útil Necessária:** {{ $json.dimensionamento_backup_calculado.bateria_util_necessaria_kwh }} kWh (para suprir a autonomia durante ausência de sol)
- **Energia Nominal do Banco:** {{ $json.dimensionamento_backup_calculado.bateria_nominal_banco_kwh }} kWh
- **Margem de Segurança Técnica Aplicada:** {{ ($json.dimensionamento_backup_calculado.paramentos_calculo.margem_tecnica * 100) }}%
- **Capacidade de Descarga Suportada:** {{ $json.dimensionamento_backup_calculado.bateria_capacidade_descarga_kw }} kW contínuos

## 9. EQUIPAMENTOS PRINCIPAIS SUGERIDOS (CORSOLAR / SOLAXPOWER)
- **Inversor Híbrido:** {{ $json.dimensionamento_backup_calculado.inversor_sugerido }} (SolaXPower Híbrido)
- **Módulos de Armazenamento:** Bateria Triple Power LFP (capacidade total aproximada de {{ $json.dimensionamento_backup_calculado.bateria_nominal_banco_kwh }} kWh)
- *Obs: Modelos, quantidades e capacidades definitivos estão sujeitos à validação comercial e estoque de fornecedores no momento do fechamento.*

## 10. ESCOPO DE FORNECIMENTO
- Equipamento inversor híbrido inteligente.
- Banco de baterias de lítio Triple Power (LFP) com módulo BMS integrado.
- Módulos solares fotovoltaicos de silício monocristalino de alta eficiência.
- Estrutura de fixação metálica e String Box de proteção (CC/CA).

## 11. ESCOPO DE INSTALAÇÃO
- Engenharia e projeto de adequação física do espaço.
- Fixação mecânica e elétrica dos inversores, baterias e módulos.
- Lançamento de cabos de potência e conexões.
- Parametrização e ativação operacional do sistema híbrido.

## 12. EXCLUSÕES
- Adequações estruturais de telhados, reforço de lajes ou remoção de obstáculos físicos (árvores, antenas).
- Modificações no padrão de entrada da concessionária que superem o disjuntor geral existente.
- Alimentação de cargas pesadas não críticas (como fornos elétricos, chapas, resistências elétricas, fritadeiras ou ar-condicionado central).

## 13. PENDÊNCIAS PARA CONFIRMAÇÃO
As pendências críticas identificadas que bloqueiam a emissão de uma proposta comercial final são:
{{#each $json.compliance_killcritic.pendencias_criticas}}
- [ ] {{this}}
{{/each}}

## 14. OBSERVAÇÕES TÉCNICAS (OBRIGATÓRIO)
> **[!IMPORTANT]**
> **Dimensionamento preliminar sujeito à Avaliação Técnica, análise da conta de energia, confirmação das cargas críticas, tensão de atendimento, local de instalação e compatibilidade dos equipamentos.**

## 15. CONDIÇÕES COMERCIAIS
- **Valor Estimado Preliminar:** R$ {{ $json.financeiro.valor_final_estimado.toFixed(2) }}
- **Validade do Estudo:** 10 dias corridos a partir desta emissão.
- **Tipo de Orçamento:** Pré-dimensionamento. O preço final e o cronograma de instalação definitiva serão definidos em proposta final após a realização de Avaliação Técnica presencial obrigatória.

## 16. CONCLUSÃO
Este pré-dimensionamento visa fundamentar as discussões sobre o investimento técnico em resiliência de energia para o condomínio/estabelecimento. Convidamos o responsável para agendamento de uma **Avaliação Técnica presencial** para validação física e elétrica dos pontos de rede.

## 17. DADOS DA DL
**DL Soluções Condominiais LTDA**
CNPJ: 37.953.703/0001-00
Rio de Janeiro - RJ
Fale com nosso consultor no Direct/WhatsApp.
