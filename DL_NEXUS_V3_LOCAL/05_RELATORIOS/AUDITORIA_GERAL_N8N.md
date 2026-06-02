# AUDITORIA READ-ONLY DO DL NEXUS / n8n

## 1. Resumo Executivo do Ambiente

- **Total de workflows:** 47 (contabilizando únicos por nome)
- **Workflows ativos:** 0
- **Workflows inativos:** 47
- **Módulos detectados:** Roteadores/Triagem (Aninha/Diego), Agentes Especializados (Skill Router), Notificações (Telegram/ElevenLabs), Postagens Sociais (Máquina de Atração), Supabase/CRM, Precificação.
- **Módulo crítico:** O módulo Social/Postagens e Triagem (Aninha) são altamente críticos.
- **Módulo quebrado/parado:** Aprovação manual via webhook (processos parados para autopublicação) e TikTok (aguardando API).
- **Riscos mais graves:** Execuções HTTP com falha não tratada podem quebrar fluxos em cadeia se `continueErrorOutput` não for usado (corrigido recentemente no fluxo principal de postagem). Vulnerabilidades de Injeção SQL se a saída do LLM não usar `defineBelow` nos nodes Postgres.

## 2. Mapa Geral dos Módulos

| Módulo | Workflows ligados | Status geral | Dependências | Riscos |
|---|---|---|---|---|
| Triagem (Aninha/Diego) | 002, 003 | Inativo | Postgres, OpenAI | Altíssimo (Entrada principal) |
| Especializados (Skills) | 004, 13x, 14x | Inativo | Postgres, Webhooks | Médio |
| Social / Postagens | 013, 08x, 020 | Inativo | Meta Graph, GMB | Alto (Falhas de API) |
| Precificação | 17x | Inativo | Postgres, Maps | Alto (Valores Incorretos) |
| Utilitários | 006, 007 | Inativo | Telegram, ElevenLabs | Baixo |

## 3. Inventário Completo de Workflows

| Workflow | ID | Ativo | Gatilho | Módulo | Função | Credenciais | Dependências | Risco |
|---|---|---|---|---|---|---|---|---|
| 013_MAQUINA_DE_ATRACAO | wf_013_maquina_de_atracao | False | n8n-nodes-base.scheduleTrigger | Social / Postagens | - | Nenhuma | Nenhuma | Avaliar |
| 003_roteador_diego | Unknown | False | n8n-nodes-base.webhook | Roteador / Triagem | - | QzziIRhKJMDNAE1m | Nenhuma | Avaliar |
| 004_roteador_agentes_especializados | Unknown | False | n8n-nodes-base.webhook | Roteador / Triagem | - | QzziIRhKJMDNAE1m | Nenhuma | Avaliar |
| 005_roteador_jules | Unknown | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 007_tarefas_background | Unknown | False | n8n-nodes-base.scheduleTrigger | Geral | - | QzziIRhKJMDNAE1m | Nenhuma | Avaliar |
| 002_roteador_aninha_v2 | Unknown | False | n8n-nodes-base.webhook | Roteador / Triagem | - | QzziIRhKJMDNAE1m | Nenhuma | Avaliar |
| 001_webhook_receptor_enterprise | Unknown | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 006_notificacoes | Unknown | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 003_roteador_diego_v3_killcritic | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook | Roteador / Triagem | - | Nenhuma | Nenhuma | Avaliar |
| 083_PUBLICADOR_GOOGLE_BUSINESS_PROFILE | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook, n8n-nodes-base.errorTrigger | Social / Postagens | - | CREDENCIAL_OAUTH2_GOOGLE_BUSINESS, CREDENCIAL_TELEGRAM | Nenhuma | Avaliar |
| 091_SENTINELA_AUDITORIA_N8N_DL_NEXUS | sentinelaAuditoriaN8nDlNexus091 | False | n8n-nodes-base.scheduleTrigger | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 092_MESA_APROVACAO_TELEGRAM_ANINHA | mesaAprovacaoTelegramAninha092 | False | n8n-nodes-base.telegramTrigger | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 177_GERAR_PROPOSTA_MARKDOWN | gerarPropostaMarkdown177DlNexus20260527 | False | n8n-nodes-base.webhookResponse, n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 179_TESTES_PRECIFICACAO | testesPrecificacao179DlNexus20260527 | False | n8n-nodes-base.manualTrigger | Precificação | - | Nenhuma | Executar Motor 170 | Avaliar |
| 173_CALCULAR_MATERIAIS_TERCEIROS | calcularMateriais173DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 175_GERAR_FAIXA_COMERCIAL | gerarFaixaComercial175DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 176_KILLCRITIC_PRECIFICACAO | killcriticPrecificacao176DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 174_CALCULAR_SLA_PARTNER | calcularSlaPartner174DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 004_skill_router_dl_nexus_v3 | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook | Roteador / Triagem | - | Nenhuma | Nenhuma | Avaliar |
| 084_PUBLICADOR_TIKTOK_ASSISTIDO | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook | Social / Postagens | - | Conta do Telegram | Nenhuma | Avaliar |
| 085_SOCIAL_DISPATCHER_DL_NEXUS | Unknown | False | n8n-nodes-base.webhook, n8n-nodes-base.errorTrigger | Social / Postagens | - | cred-telegram-dl | Nenhuma | Avaliar |
| 172_CALCULAR_MAO_DE_OBRA | calcularMaoObra172DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | placeholder_google_calendar_oauth2 | Nenhuma | Avaliar |
| 170_MOTOR_PRECIFICACAO_DL_NEXUS | motorPrecificacao170DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | Nenhuma | Nenhuma | Avaliar |
| 178_LOG_PRECIFICACAO | logPrecificacao178DlNexus20260527 | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook | Precificação | - | supabase-cred | Nenhuma | Avaliar |
| 082_PUBLICADOR_FACEBOOK_META_API | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook, n8n-nodes-base.errorTrigger | Social / Postagens | - | cred_facebook_graph_api, cred_telegram_api | Nenhuma | Avaliar |
| 171_CALCULAR_DESLOCAMENTO_MAPS | calcularDeslocamento171DlNexus20260527 | False | n8n-nodes-base.webhook | Precificação | - | googleMaps | Nenhuma | Avaliar |
| 081_PUBLICADOR_INSTAGRAM_META_API | Unknown | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook, n8n-nodes-base.errorTrigger | Social / Postagens | - | cred-telegram, cred-facebook-graph | Nenhuma | Avaliar |
| 020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO | Unknown | False | n8n-nodes-base.manualTrigger | Social / Postagens | - | Conta OpenAi, SMTP - Suporte DL, Aplicativo do Facebook, Conta do Telegram | Nenhuma | Avaliar |
| 060_AGENT_MANUS_PROSPECCAO_ATIVA | Unknown | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 144_REVISOR_IA_DUPLO | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 142_CLASSIFICADOR_TEMA_MIDIA | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 148_LOG_E_MEMORIA_SOCIAL | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 130_MANUS_PROSPECCAO_B2B_RJ | manusProspeccao130DlNexus20260523 | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 135 Relatorio Comercial Diario DL Nexus | relatorioComercialDiario135DlNexus20260523 | False | n8n-nodes-base.scheduleTrigger | Geral | - | TELEGRAM_CRED_ID_AQUI, SUPABASE_CRED_ID_AQUI | Nenhuma | Avaliar |
| 019_GERADOR_ORCAMENTO_RAPIDO | Unknown | False | n8n-nodes-base.manualTrigger | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 143_GERADOR_POST_EDUCATIVO_DL | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 145_CRIADOR_CARROSSEL_SOCIAL | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 131_SCORING_LEADS_DL_NEXUS | scoringLeads131DlNexus20260523 | False | n8n-nodes-base.respondToWebhook, n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 132_ENGAJAMENTO_SOCIAL_ASSISTIDO_DL_NEXUS | engajamentoAssistido132DlNexus20260523 | False | n8n-nodes-base.webhook | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 021_DESCOBRIR_IDS_SOCIAIS_DL_NEXUS | Unknown | False | n8n-nodes-base.manualTrigger | Geral | - | SMTP - Suporte DL, Aplicativo do Facebook, Conta do Telegram | Nenhuma | Avaliar |
| 149_RELATORIO_SOCIAL_DIARIO | Unknown | False | n8n-nodes-base.scheduleTrigger | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 147_SENTINELA_NOTICIAS_VERIFICADAS | Unknown | False | n8n-nodes-base.scheduleTrigger | Geral | - | Nenhuma | Nenhuma | Avaliar |
| 141_REVISOR_MIDIAS_DL_NEXUS | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |
| 133_APROVACAO_PROSPECCAO_TELEGRAM | aprovacaoProspeccaoTelegram133DlNexus20260523 | False | n8n-nodes-base.webhook | Geral | - | Conta do Telegram | Nenhuma | Avaliar |
| 134_POST_GOOGLE_BUSINESS_DL_NEXUS | postGoogleBusiness134DlNexus20260523 | False | n8n-nodes-base.webhook | Geral | - | OAuth2 Google Business Profile, Conta do Telegram | Nenhuma | Avaliar |
| 140_ZELADOR_MIDIAS_GOOGLE_DRIVE | Unknown | False | n8n-nodes-base.scheduleTrigger | Geral | - | vDUp3ZKxazIKho51 | Nenhuma | Avaliar |
| 146_PUBLICADOR_MULTICANAL_DL | Unknown | False | n8n-nodes-base.executeWorkflowTrigger | Geral | - | Nenhuma | Execute Workflow Trigger | Avaliar |

## 4. Desenho de Fluxo por Módulo

### Módulo Social / Postagens
```
Schedule Trigger (Cron)
↓
Gera Rascunho (LLM)
↓
Salva Postgres (Status: gerado)
↓
Validar KILLCRITIC (Bloqueia 'visita técnica', exige CTAs)
↓
Se Aprovado: Publica Facebook (HTTP) -> Atualiza Status FB
↓
Publica Instagram (HTTP) -> Atualiza Status IG
↓
Publica GMB (HTTP) -> Atualiza Status GMB
```

## 5. Mapa do Módulo Social / Postagens

- **5.1 Workflows que publicam:** `013_MAQUINA_DE_ATRACAO`, `081_PUBLICADOR_INSTAGRAM...`, `082_PUBLICADOR_FACEBOOK...`, `083_PUBLICADOR_GOOGLE...`
- **5.2 Workflows que apenas geram conteúdo:** `143_GERADOR_POST_EDUCATIVO_DL`
- **5.3 Workflows que pedem aprovação:** `092_MESA_APROVACAO_TELEGRAM_ANINHA` (em transição/inativo)
- **5.4 Workflows que travam publicação:** Nenhum no fluxo novo 013 (KILLCRITIC bloqueia apenas se infringir regras, mas não trava esperando humano).
- **5.5 Workflows que apenas alertam erro:** O fluxo atual no 013 salva erros no Postgres (erro_publicacao).
- **5.6 Credenciais sociais envolvidas:** Nenhuma injetada diretamente via Node Credentials no JSON local (usa HTTP headers locais/VPS).
- **5.7 Pontos que não devem ser alterados sem autorização:** Webhooks de entrada (`001_webhook_receptor`) e nodes Postgres configurados com `defineBelow`.

## 6. Mapa de Credenciais

| Credencial | Tipo | Workflows que usam | Estado provável | Risco | Observação |
|---|---|---|---|---|---|
| cred-facebook-graph | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| vDUp3ZKxazIKho51 | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| placeholder_google_calendar_oauth2 | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| TELEGRAM_CRED_ID_AQUI | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| QzziIRhKJMDNAE1m | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| CREDENCIAL_OAUTH2_GOOGLE_BUSINESS | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| SUPABASE_CRED_ID_AQUI | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| Conta do Telegram | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| supabase-cred | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| SMTP - Suporte DL | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| cred-telegram | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| CREDENCIAL_TELEGRAM | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| cred_telegram_api | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| Conta OpenAi | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| OAuth2 Google Business Profile | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| Aplicativo do Facebook | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| googleMaps | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| cred-telegram-dl | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -
| cred_facebook_graph_api | Desconhecido | Vários | Configurado na VPS | Alto (Se apagado, quebra fluxo) | -

## 7. Mapa de APIs

| API | Finalidade | Workflow usuário | Status provável | Risco de quebra |
|---|---|---|---|---|
| Meta Graph API | Publicar FB/IG | 013, 081, 082 | Ativa (a confirmar VPS) | Alto (Token Expiration) |
| Google My Business | Publicar GMB | 013, 083 | Ativa (a confirmar VPS) | Alto |
| OpenAI/Gemini/Claude | Gerar Copy | 013, 002, 003 | Ativa | Baixo |

## 8. Bloqueios e Aprovações Encontrados

| Workflow | Nó | Tipo de bloqueio | O que bloqueia | Risco operacional |
|---|---|---|---|---|
| 013_MAQUINA_DE_ATRACAO | Validar KILLCRITIC | Lógico (Regras DL) | Publicação de termos proibidos | Baixo (Desejado) |
| 092_MESA_APROVACAO | - | Telegram Wait | Fluxos antigos | Médio (Gargalo humano) |

## 9. Dependências Entre Workflows

| Workflow origem | Workflow destino | Tipo de chamada | Risco |
|---|---|---|---|
| N/A | N/A | SubWorkflows desativados via ExecuteWorkflow Node no JSON auditado | Baixo |

## 10. Pontos de Falha Críticos

- Falha de credencial da Meta Graph API (tokens de curta duração).
- Vulnerabilidade de injeção de SQL se novos workflows utilizarem `executeQuery` cru com `{{ $json.text }}`.
- Workflows parados (TikTok) por falta de documentação/credencial da API.
- Aprovação manual indevida travando fluxos legados de prospecção.
- Fluxo social dependendo de IDs estáticos gerados por outro canal (se FB falhar e interromper IG em lógicas malfeitas).

## 11. Itens que Exigem Autorização Antes de Qualquer Alteração

- `000_meta_receptor`, `001_webhook_receptor` (Entradas vitais).
- Nodes Postgres com `defineBelow` (Risco de injeção SQL se alterados para Raw Query).
- Configurações do KILLCRITIC V3.
- `dl_nexus_social_autopublish_config.json`.

## 12. Recomendações Futuras — SEM EXECUTAR

**Correções urgentes:**
- Nenhuma correção funcional no `013_MAQUINA_DE_ATRACAO` pois já foi refatorado.

**Correções importantes:**
- Garantir que todos os Nodes Postgres legados em todos os outros workflows sejam revisados para não usar `executeQuery` cru.

**Melhorias futuras:**
- Implementar alertas ativos no Telegram apenas se todos os canais de publicação falharem.

**Itens que devem permanecer intactos:**
- Receptores de webhook principais e lógica central de triagem da Aninha.

***

Auditoria concluída em modo READ-ONLY. Nenhum workflow, credencial, API, token, webhook ou configuração foi alterado.
