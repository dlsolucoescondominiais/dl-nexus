# INVENTARIO_REFERENCIAS_MANUS_DL

## 1. Arquivos / Workflows Identificados
- `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/130_MANUS_PROSPECCAO_B2B_RJ.json`
- `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/070_CRON_MANUS_DIARIO.json`
- `DL_NEXUS_V3_LOCAL/11_N8N_AGENTES_V3/060_AGENT_MANUS_PROSPECCAO_ATIVA.json`
- `ARVORE_EVOLUCAO_PROJETO_N8N_DL_NEXUS.md`

## 2. Scripts Python Identificados
- `gerar_manus_prospeccao.py`
- `linkar_manus_marketing.py`
- `linkar_manus_marketing_v2.py`
- `linkar_manus_marketing_v3.py`
- `deploy_manus_070.py`
- `scripts/rebuild_070_manus_real.py`
- `scripts/fetch_070_from_n8n.py`

## 3. Variáveis e Credenciais Encontradas
- **Variáveis (`.env` ou referências n8n):** `MANUS_API_KEY`, `MANUS_URL`
- **Credenciais n8n:** Conexões de Header Auth utilizadas nos nós do Manus foram rastreadas e marcadas para substituição por credenciais do DeepSeek.
- **Risco de Remoção:** Muito baixo, visto que os workflows principais foram substituídos sem deleção e pausados com fallback, e o ambiente de produção real não sofrerá deploy sem intervenção humana.

## 4. Substituição Recomendada
- **Função:** IA Avançada de Prospecção / Planejamento.
- **Substituto Recomendado:** DeepSeek para processos densos (agente principal) e Gemini Flash para roteamentos rápidos e extração JSON estruturada no n8n.
