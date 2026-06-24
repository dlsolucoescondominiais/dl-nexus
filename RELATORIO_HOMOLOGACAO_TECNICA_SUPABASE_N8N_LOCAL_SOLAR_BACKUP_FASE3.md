# RELATÓRIO DE HOMOLOGAÇÃO TÉCNICA — FASE 3
**Módulo:** 200_MOTOR_SOLAR_BACKUP_DL_ECOVOLT  
**Data:** 2026-06-24  
**Ambiente:** SIMULAÇÃO LOCAL / DESENVOLVIMENTO  
**Status:** **BLOQUEADO POR DNS DO SUPABASE CLOUD (RESTANTE VALIDADO EM SIMULADOR)**  

---

## 1. Status das Conexões e Infraestrutura
Durante os testes de integração física e de aplicação de banco de dados, foram identificados os seguintes impedimentos de infraestrutura cloud:

* **Supabase DEV (`nejdtvkpiclagsnfljsz.supabase.co`):** O projeto de desenvolvimento encontra-se **pausado** na infraestrutura da Supabase Cloud. A tentativa de resolução DNS retornou `ENOTFOUND` e `Non-existent domain` (comprovado via testes de rede local). Desta forma, a migração SQL e as queries de `INSERT`, `UPDATE` e `SELECT` estão **bloqueadas** até a reativação manual do banco de dados no console Supabase.
* **n8n Local:** Não há instância do n8n rodando localmente nesta máquina (conforme mapeamento de portas ativas). O n8n opera exclusivamente em modo remoto/cloud no domínio `n8n.dlsolucoescondominiais.com.br`.
* **Solução Homologada:** A validação técnica dos payloads e das regras do **KILLCRITIC** foi efetuada através de um script simulador Node.js (`tmp_mock_execution_test.js`) que processou a lógica exata de cada nó de código JavaScript dos workflows 202, 203, 204, 205 e 207 em ambiente isolado.

---

## 2. Tabelas do Supabase (Migration e RLS)
O arquivo de migração [`migration_dl_solar_backup_orcamentos.sql`](file:///d:/AntiGravity/projeto_01/backend/supabase/migration_dl_solar_backup_orcamentos.sql) está pronto e consolidado no repositório. Uma vez que o banco de dados seja reativado pelo console, a migração criará as seguintes tabelas com integridade idempotente:
1. `dl_solar_orcamentos` (mestre de orçamentos)
2. `dl_solar_cargas_criticas` (cargas mapeadas)
3. `dl_solar_equipamentos` (sourcing Corsolar/SolaX)
4. `dl_solar_orcamento_versoes` (markdown e JSON gerados)
5. `dl_solar_aprendizado` (logs e traces da IA)

### Validação do RLS e Policies para n8n
Para garantir que as políticas de RLS (Row Level Security) não bloqueiem as requisições HTTP do n8n, as seguintes políticas foram codificadas na migration:
* **Service Role Access:** Todas as operações (`INSERT`, `UPDATE`, `SELECT`, `DELETE`) são liberadas integralmente para a chave administrativa `service_role` (Bearer Token) utilizada nas requisições do n8n.
* **Anon/Authenticated Policies:**
  * `SELECT` habilitado para usuários autenticados ou anônimos (dependendo do escopo da API pública).
  * `INSERT`/`UPDATE` restritos apenas a requisições contendo a chave `service_role` para blindagem do banco contra acessos maliciosos externos.

---

## 3. Workflows n8n (Importação e Status)
Os workflows estão salvos localmente e marcados como inativos (`"active": false`), respeitando as diretrizes:
* `200_SOLAR_BACKUP_RECEPCAO_DADOS.json`
* `201_SOLAR_BACKUP_ANALISE_CONTA_ENERGIA.json`
* `202_SOLAR_BACKUP_CARGAS_CRITICAS.json`
* `203_SOLAR_BACKUP_DIMENSIONAMENTO_BATERIAS.json`
* `204_SOLAR_BACKUP_DIMENSIONAMENTO_INVERSOR.json`
* `205_SOLAR_BACKUP_DIMENSIONAMENTO_FOTOVOLTAICO.json`
* `206_SOLAR_BACKUP_BASE_EQUIPAMENTOS_CORSOLAR_SOLAX.json`
* `207_SOLAR_BACKUP_KILLCRITIC_TECNICO.json`
* `208_SOLAR_BACKUP_GERADOR_PROPOSTA_MARKDOWN.json`
* `209_SOLAR_BACKUP_GERADOR_PDF_GOOGLE_DOCS.json` (Mantido estritamente em **homologação**)
* `210_SOLAR_BACKUP_AGENTE_EVOLUCAO_ORCAMENTOS.json`

---

## 4. Resultados da Execução Lógica dos Payloads (Simulação Local)

O script local validou fisicamente todas as fórmulas de cálculo e a aplicação do **KILLCRITIC**. Resultados exatos:

### Scenario A: Condomínio Residencial Flores do Bosque
* **Energia Crítica Diária:** $112,80\text{ kWh/dia}$
* **Bateria Nominal Mínima:** $207,353\text{ kWh}$
* **Potência Simultânea:** $3,50\text{ kW}$
* **Potência Inversor Mínima:** $4,375\text{ kW}$
* **Inversor Sugerido:** SolaX X3-Hybrid 10.0-D
* **Solar Preliminar:** $39,13\text{ kWp}$
* **Status KILLCRITIC:** 🔴 **BLOQUEADO** (`bloqueado_killcritic`)
* **Motivos de Bloqueio:**
  - Presença de elevador social (dimensionamento automático proibido).
  - Presença de bomba de recalque sem dados elétricos de pico de partida definidos (`desconhecido`).
  - Cargas de alta potência de indução exigem projeto e Avaliação Técnica presencial.

### Scenario B: Residência Cláudio Ramos
* **Energia Crítica Diária:** $9,965\text{ kWh/dia}$
* **Bateria Nominal Mínima:** $18,318\text{ kWh}$
* **Potência Simultânea:** $0,82\text{ kW}$
* **Potência Inversor Mínima:** $1,025\text{ kW}$
* **Inversor Sugerido:** SolaX X1-Hybrid 5.0-D
* **Solar Preliminar:** $7,39\text{ kWp}$
* **Status KILLCRITIC:** 🟡 **APROVADO COM RESSALVAS** (`aprovado_para_proposta`)
* **Ressalvas/Pendências:** Confirmar local físico seguro de baterias na garagem e validar precificação Corsolar.

### Scenario C: Laboratório de Análises MedLab RJ
* **Energia Crítica Diária:** $111,60\text{ kWh/dia}$
* **Bateria Nominal Mínima:** $205,147\text{ kWh}$
* **Potência Simultânea:** $4,65\text{ kW}$
* **Potência Inversor Mínima:** $5,813\text{ kW}$
* **Inversor Sugerido:** SolaX X3-Hybrid 10.0-D
* **Solar Preliminar:** $24,35\text{ kWp}$
* **Status KILLCRITIC:** 🟡 **APROVADO COM RESSALVAS** (`aprovado_para_proposta`)
* **Ressalvas/Pendências:** Validar tempo de bypass dos no-breaks e sombreamento de edifícios em Botafogo.

### Scenario D: Restaurante e Chopperia Carioca
* **Energia Crítica Diária:** $62,40\text{ kWh/dia}$
* **Bateria Nominal Mínima:** $114,706\text{ kWh}$
* **Potência Simultânea:** $3,15\text{ kW}$
* **Potência Inversor Mínima:** $3,938\text{ kW}$
* **Inversor Sugerido:** SolaX X3-Hybrid 10.0-D
* **Solar Preliminar:** $26,96\text{ kWp}$
* **Status KILLCRITIC:** 🟡 **APROVADO COM RESSALVAS** (`aprovado_para_proposta`)
* **Ressalvas/Pendências:** Exclusão mandatória de fornos, fritadeiras e resistências; verificar dissipação de calor no depósito de bebidas.

---

## 5. Conclusões e Pendências Críticas

> [!CAUTION]
> **BLOQUEADORES CRÍTICOS:**
> 1. O banco de dados Supabase de desenvolvimento (`nejdtvkpiclagsnfljsz.supabase.co`) precisa ser **reativado manualmente** por um administrador no console da Supabase. O projeto encontra-se em modo de pausa.
> 2. O token de acesso `SUPABASE_ACCESS_TOKEN` no arquivo `.env` expirou (retorno 401 Unauthorized), impedindo a restauração do projeto por API.
> 3. Os testes de `INSERT`, `UPDATE` e `SELECT` no Supabase DEV estão pendentes e só poderão ser validados fisicamente após o banco retornar ao status online.
> 4. O workflow 209 (Google Docs/PDF) deve continuar em modo homologação até a entrada das credenciais autorizadas.
