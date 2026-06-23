# Árvore de Evolução do Projeto DL Nexus n8n

**Objetivo:** Documentar a arquitetura atual, o status operacional e a evolução planejada do ecossistema inteligente DL Nexus, abrangendo automações, frontend, segurança e integrações de terceiros.
**Base:** Sincronizado a partir do `13_N8N_PRODUCAO_SYNC`.

---

## Legenda de Classificação
- 🟢 **ATIVO:** Em operação na produção.
- ⏸️ **PAUSADO:** Desativado temporariamente na produção.
- 🟡 **HOMOLOGAÇÃO:** Em testes, não liberado para uso comercial.
- 🔵 **PLANEJADO:** Mapeado para futuras sprints.
- 🔴 **CRÍTICO:** Módulo estrutural vital. Falhas derrubam outras dependências.
- ⚙️ **LEGADO / NÃO MEXER:** Rotinas antigas preservadas para fallback.

---

## 1. Infraestrutura Base
- 🟢 **008_mcp_server:** Motor de integração MCP.
- 🟢 **004_skill_router_dl_nexus_v3:** Roteamento central de skills. [🔴 CRÍTICO]

## 2. Monitoramento e Segurança
- 🟢 **090_GUARDIAO_N8N_DL_NEXUS_V3:** Cão de guarda do ecossistema. [🔴 CRÍTICO]
- 🟢 **091_SENTINELA_AUDITORIA_N8N_DL_NEXUS:** Rastreador de anomalias.
- 🟢 **147_SENTINELA_NOTICIAS_VERIFICADAS:** Filtro de desinformação.

## 3. Atendimento Aninha (IA Conversacional)
- 🟢 **001_TELEGRAM_RECEPCAO_ANINHA_V3:** Gateway de entrada via Telegram.
- 🟢 **002_roteador_aninha_v3_atendimento:** Direcionador de chamados.
- 🟢 **053_ANINHA_SOCIAL_HANDOFF_TELEGRAM:** Handoff de leads sociais para Telegram.
- 🟢 **054_ANINHA_SOCIAL_RELATORIO_DIARIO:** Geração de relatórios de atendimento.

## 4. SDR Social Meta (Facebook / Instagram)
- 🟢 **050_AGENTE_SDR_SOCIAL_DL:** Máquina de triagem de leads nas redes sociais. [🔴 CRÍTICO]
- 🟢 **051_ANINHA_SOCIAL_MEMORIA_SUPABASE:** Persistência de conversação em banco relacional.
- 🟢 **052_ANINHA_SOCIAL_RESPOSTA_META:** Engrenagem de disparo de mensagens Meta.

## 5. Prospecção Interna DL Nexus (Corporativo e Condominial Outbound)
- ⏸️ **130_MANUS_PROSPECCAO_B2B_RJ:** [LEGADO / NÃO MEXER] Identificação de alvos comerciais no RJ. (Manus.IA removido)
- ⏸️ **060_AGENT_MANUS_PROSPECCAO_ATIVA:** [LEGADO / NÃO MEXER] Motor de contato ativo outbound. (Manus.IA removido)
- 🟢 **130_PROSPECCAO_INTERNA_CORPORATIVA_CONDOMINIAL_DL:** Identificação de alvos corporativos e condominiais no RJ.
- 🟢 **060_AGENT_PROSPECCAO_ATIVA_DL:** Motor de contato ativo outbound via inteligência interna.
- 🟢 **131_SCORING_LEADS_DL_NEXUS:** Máquina de pontuação térmica de leads corporativos e condominiais.

## 6. Conteúdo e Marketing
- 🟢 **150_MAQUINA_CONTEUDO_DIARIA_DL:** Gerador central de pautas.
- 🟢 **142_CLASSIFICADOR_TEMA_MIDIA:** Roteador temático (Ex: Solar, CFTV, Elétrica).
- 🟢 **143_GERADOR_POST_EDUCATIVO_DL:** Criação específica de publicações técnicas.
- 🟢 **141_REVISOR_MIDIAS_DL_NEXUS:** Validador textual de copy.
- 🟢 **144_REVISOR_IA_DUPLO:** Dupla checagem anti-alucinação.

## 7. Publicação Facebook/Instagram
- ⏸️ **020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO:** Central de publicação com aprovação manual. [🟡 HOMOLOGAÇÃO]
- ⏸️ **146_PUBLICADOR_MULTICANAL_DL:** Distribuidor omnichannel.
- ⏸️ **081_PUBLICADOR_INSTAGRAM_META_API:** Worker de disparo (Instagram).
- ⏸️ **082_PUBLICADOR_FACEBOOK_META_API:** Worker de disparo (Facebook).

## 8. Motor de Precificação e Orçamento
- 🟢 **170_MOTOR_PRECIFICACAO_DL_NEXUS:** Orquestrador-mãe de valores. [🔴 CRÍTICO]
- 🟢 **172_CALCULAR_MAO_DE_OBRA:** Worker de custo homem/hora.
- 🟢 **173_CALCULAR_MATERIAIS_TERCEIROS:** Worker de insumos.
- 🟢 **174_CALCULAR_SLA_PARTNER:** Custos de contratos de manutenção.
- 🟢 **175_GERAR_FAIXA_COMERCIAL:** Precificador de margem bruta.
- 🟢 **176_KILLCRITIC_PRECIFICACAO:** Filtro auditor anti-prejuízo comercial. [🔴 CRÍTICO]
- 🟢 **177_GERAR_PROPOSTA_MARKDOWN:** Renderizador do documento.
- 🟢 **178_LOG_PRECIFICACAO:** Trace e compliance de preços.
- 🟢 **019_GERADOR_ORCAMENTO_RAPIDO:** Fluxo comercial rápido.
- 🟢 **190_MOTOR_ORCAMENTO_MASTER:** Módulo avançado em produção.

## 9. Site e Formulário de Orçamento
- 🔵 **Motor de Orçamento via Site:** Planejado para receber via Webhook.
- 🔵 **Geração PDF com Gotenberg:** Endpoint para PDF.
- 🔵 **Formulário Completo de Avaliação Técnica:** Front-end.
- ⚠️ **Status do Site:** Site foi localizado em `DL_SITE_B2B`, mas conforme solicitado nos dados base, registramos oficialmente a pendência de mapeamento arquitetônico final da via web.

## 10. Google Drive e Agente Zelador
- ⏸️ **140_ZELADOR_MIDIAS_GOOGLE_DRIVE:** Desligado por segurança.
- 🔵 **140B_AGENTE_ZELADOR_EXECUTOR_MOVIMENTACAO_APROVADA:** Planejado para atuar estritamente em modo sugerido/diagnóstico até aprovação.

## 11. GitHub e Versionamento
- 🔴 **Pendência Crítica:** Histórico git contendo vazamento de segredo antigo (GitHub Push Protection Code 190 / GH013). (NOTA: Corrigido recentemente via reescrita local, pendente de flush limpo caso retorne a bloquear na próxima árvore de push de dependências severas).

## 12. Próximas Fases e Status Meta API
* **Meta Page ID real:** `100166804716824`
* **Instagram Business ID real:** `17841403185822108`
* **Status do appsecret_proof:** Validado e gerando HMAC-SHA256 corretos.
* **Publicação Real:** O token atual gera Code 200 no Facebook por falta de escopo (`pages_read_engagement` e `pages_manage_posts`). Portanto, a publicação real ainda **não** está liberada para a rotina automática em volume. O Instagram passou no teste, mas o sistema segue travado na esteira geral.

---
*Gerado automaticamente pelo Agente Antigravity baseado no ecosistema n8n local e cloud.*
