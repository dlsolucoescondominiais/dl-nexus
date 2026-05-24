# Relatório de Status dos Workflows N8N - DL Nexus V3

Este relatório detalha o status de todos os workflows JSON e suas dependências no ecosistema DL Nexus.

## Resumo Executivo

- **Total de Arquivos Analisados:** 35
- **Workflows Válidos:** 33
- **Workflows Inválidos/Com Erro:** 2
- **Workflows Ativos:** 0

## Arquivos Inválidos

- `DL_NEXUS_V3_LOCAL/01_WORKFLOWS_RECEBIDOS_JULES/004_skill_router_dl_nexus_v3.json`: Invalid JSON
- `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/004_skill_router_dl_nexus_v3.json`: Invalid JSON

## Detalhamento dos Workflows

| Arquivo | Nome do Workflow | Status Ativo | Qtd. Nodes | Dependências Principais |
|---------|------------------|--------------|------------|-------------------------|
| `DL_NEXUS_V3_LOCAL/00_CONFIG/dl_nexus_canais_oficiais.json` | N/A | ❌ Não | 0 | Nenhuma detectada |
| `DL_NEXUS_V3_LOCAL/01_WORKFLOWS_RECEBIDOS_JULES/003_roteador_diego_v3_killcritic.json` | 003_roteador_diego_v3_killcritic | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/003_roteador_diego_v3_killcritic.json` | 003_roteador_diego_v3_killcritic | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/004_skill_router_dl_nexus_v3.json` | 004_skill_router_dl_nexus_v3 | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/081_PUBLICADOR_INSTAGRAM_META_API.json` | 081_PUBLICADOR_INSTAGRAM_META_API | ❌ Não | 15 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/082_PUBLICADOR_FACEBOOK_META_API.json` | 082_PUBLICADOR_FACEBOOK_META_API | ❌ Não | 13 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE.json` | 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/084_PUBLICADOR_TIKTOK_ASSISTIDO.json` | 084_PUBLICADOR_TIKTOK_ASSISTIDO | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/09_PRONTOS_PARA_PRODUCAO/085_SOCIAL_DISPATCHER_DL_NEXUS.json` | 085_SOCIAL_DISPATCHER_DL_NEXUS | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/11_N8N_AGENTES_V3/060_AGENT_MANUS_PROSPECCAO_ATIVA.json` | 060_AGENT_MANUS_PROSPECCAO_ATIVA | ❌ Não | 4 | Webhooks |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/019_GERADOR_ORCAMENTO_RAPIDO.json` | 019_GERADOR_ORCAMENTO_RAPIDO | ❌ Não | 4 | Nenhuma detectada |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO.json` | 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO | ❌ Não | 16 | AI/LLM, Telegram |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/081_PUBLICADOR_INSTAGRAM_META_API.json` | 081_PUBLICADOR_INSTAGRAM_META_API | ❌ Não | 15 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/082_PUBLICADOR_FACEBOOK_META_API.json` | 082_PUBLICADOR_FACEBOOK_META_API | ❌ Não | 13 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE.json` | 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/084_PUBLICADOR_TIKTOK_ASSISTIDO.json` | 084_PUBLICADOR_TIKTOK_ASSISTIDO | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/12_N8N_WORKFLOWS_PROXIMOS/085_SOCIAL_DISPATCHER_DL_NEXUS.json` | 085_SOCIAL_DISPATCHER_DL_NEXUS | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/003_roteador_diego_v3_killcritic.json` | 003_roteador_diego_v3_killcritic | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/003_roteador_diego_v3_killcritic_config.json` | 003_roteador_diego_v3_killcritic | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/004_skill_router_dl_nexus_v3_config.json` | 004_skill_router_dl_nexus_v3 | ❌ Não | 3 | Webhooks |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO_config.json` | 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO | ❌ Não | 16 | AI/LLM, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/081_PUBLICADOR_INSTAGRAM_META_API_config.json` | 081_PUBLICADOR_INSTAGRAM_META_API | ❌ Não | 15 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/082_PUBLICADOR_FACEBOOK_META_API_config.json` | 082_PUBLICADOR_FACEBOOK_META_API | ❌ Não | 13 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE_config.json` | 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/084_PUBLICADOR_TIKTOK_ASSISTIDO_config.json` | 084_PUBLICADOR_TIKTOK_ASSISTIDO | ❌ Não | 12 | Webhooks, Telegram |
| `DL_NEXUS_V3_LOCAL/20_UPLOAD_N8N/085_SOCIAL_DISPATCHER_DL_NEXUS_config.json` | N/A | ❌ Não | 0 | Nenhuma detectada |
| `backend/n8n/workflows/001_webhook_receptor.json` | 001_webhook_receptor_enterprise | ❌ Não | 13 | Supabase, AI/LLM, Webhooks |
| `backend/n8n/workflows/002_roteador_aninha.json` | 002_roteador_aninha_v2 | ❌ Não | 17 | Supabase, AI/LLM, Webhooks |
| `backend/n8n/workflows/003_roteador_diego.json` | 003_roteador_diego | ❌ Não | 3 | Supabase, Webhooks |
| `backend/n8n/workflows/004_roteador_agentes_especializados.json` | 004_roteador_agentes_especializados | ❌ Não | 7 | Supabase, AI/LLM, Webhooks |
| `backend/n8n/workflows/005_roteador_jules.json` | 005_roteador_jules | ❌ Não | 2 | Webhooks |
| `backend/n8n/workflows/006_notificacoes.json` | 006_notificacoes | ❌ Não | 2 | Webhooks |
| `backend/n8n/workflows/007_tarefas_background.json` | 007_tarefas_background | ❌ Não | 2 | Supabase |
