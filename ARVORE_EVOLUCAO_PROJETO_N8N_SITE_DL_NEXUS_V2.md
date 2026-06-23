# Árvore de Evolução do Projeto DL Nexus n8n (V2)

**Objetivo:** Documentar a arquitetura atual, o status operacional e a evolução planejada do ecossistema inteligente DL Nexus, abrangendo automações, site, segurança e integrações corporativas e condominiais.

**Base de Sincronização:** `13_N8N_PRODUCAO_SYNC`.

---

## Legenda de Classificação

* 🟢 **ATIVO:** Em operação na produção.
* ⏸️ **PAUSADO:** Desativado temporariamente na produção.
* 🟡 **HOMOLOGAÇÃO:** Em testes, não liberado para uso comercial.
* 🔵 **PLANEJADO:** Mapeado para futuras sprints.
* 🔴 **CRÍTICO:** Módulo estrutural vital. Falhas derrubam outras dependências.
* ⚙️ **LEGADO / NÃO MEXER:** Rotinas antigas preservadas para fallback.

**Nota de Linguagem Comercial:** termos internos como “B2B” são apenas nomenclatura de sistema. Publicamente usar “corporativo e condominial”.

---

## 1. Infraestrutura Base

* 🟢 **008_mcp_server:** Motor de integração MCP.
* 🟢 **004_skill_router_dl_nexus_v3:** Roteamento central de skills. [🔴 CRÍTICO]

---

## 2. Monitoramento e Segurança

* 🟢 **090_GUARDIAO_N8N_DL_NEXUS_V3:** Cão de guarda do ecossistema. [🔴 CRÍTICO]
* 🟢 **091_SENTINELA_AUDITORIA_N8N_DL_NEXUS:** Rastreador de anomalias.
* 🟢 **147_SENTINELA_NOTICIAS_VERIFICADAS:** Filtro de desinformação.

---

## 3. Atendimento Aninha

* 🟢 **001_TELEGRAM_RECEPCAO_ANINHA_V3:** Gateway de entrada via Telegram.
* 🟢 **002_roteador_aninha_v3_atendimento:** Direcionador de chamados.
* 🟢 **053_ANINHA_SOCIAL_HANDOFF_TELEGRAM:** Handoff de leads sociais corporativos e condominiais.
* 🟢 **054_ANINHA_SOCIAL_RELATORIO_DIARIO:** Geração de relatórios de atendimento.

---

## 4. SDR Social Meta

* 🟢 **050_AGENTE_SDR_SOCIAL_DL:** Máquina de triagem de leads nas redes sociais. [🔴 CRÍTICO]
* 🟢 **051_ANINHA_SOCIAL_MEMORIA_SUPABASE:** Persistência de conversação em banco relacional.
* 🟡 **052_ANINHA_SOCIAL_RESPOSTA_META:** Estrutura de resposta Meta. Ativo apenas em modo controlado, DRY_RUN ou handoff. Resposta real automática via Meta não está liberada sem App Review e validação final de permissões.

---

## 5. Prospecção Manus

* 🟢 **130_MANUS_PROSPECCAO_B2B_RJ:** Identificação de alvos comerciais no RJ. Nome legado interno; publicamente usar “prospecção corporativa e condominial”.
* 🟢 **060_AGENT_MANUS_PROSPECCAO_ATIVA:** Motor de contato ativo outbound.
* 🟢 **131_SCORING_LEADS_DL_NEXUS:** Máquina de pontuação térmica de leads.

---

## 6. Conteúdo e Marketing

* 🟢 **150_MAQUINA_CONTEUDO_DIARIA_DL:** Gerador central de pautas.
* 🟢 **142_CLASSIFICADOR_TEMA_MIDIA:** Roteador temático.
* 🟢 **143_GERADOR_POST_EDUCATIVO_DL:** Criação específica de publicações técnicas.
* 🟢 **141_REVISOR_MIDIAS_DL_NEXUS:** Validador textual de copy.
* 🟢 **144_REVISOR_IA_DUPLO:** Dupla checagem anti-alucinação.

---

## 7. Publicação Facebook/Instagram — Meta API

### Status consolidado

* Leitura Meta: **validada**.
* appsecret_proof: **validado**.
* Escrita/publicação Facebook: **não homologada**.
* Escrita/publicação Instagram: **não homologada**.
* Rotina automática de publicação: **proibida até teste real unitário**.
* OAuth Code 200 indica falta de permissão/escopo, não sucesso HTTP 200.
* Próximo teste permitido: **1 post real Facebook isolado, sem imagem, com `TESTE_REAL_FACEBOOK=true` e `TESTE_REAL_INSTAGRAM=false`**.

### IDs corretos

* `FACEBOOK_PAGE_ID=100166804716824`
* `INSTAGRAM_BUSINESS_ACCOUNT_ID=17841403185822108`
* `FACEBOOK_PAGE_USERNAME=dlsolucoescondominiais`
* `INSTAGRAM_USERNAME=dl.solucoescondominiais`

### IDs obsoletos neste fluxo

* `100063696635033`
* `3136866194`

### Workflows

* ⏸️ **020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO:** Central com aprovação manual. [🟡 HOMOLOGAÇÃO]
* ⏸️ **146_PUBLICADOR_MULTICANAL_DL:** Distribuidor multicanal.
* ⏸️ **081_PUBLICADOR_INSTAGRAM_META_API:** Worker de disparo Instagram.
* ⏸️ **082_PUBLICADOR_FACEBOOK_META_API:** Worker de disparo Facebook.

---

## 8. Motor de Precificação e Orçamento

* 🟢 **170_MOTOR_PRECIFICACAO_DL_NEXUS:** Orquestrador-mãe de valores. [🔴 CRÍTICO]
* 🟢 **172_CALCULAR_MAO_DE_OBRA:** Worker de custo homem/hora.
* 🟢 **173_CALCULAR_MATERIAIS_TERCEIROS:** Worker de insumos.
* 🟢 **174_CALCULAR_SLA_PARTNER:** Custos de contratos de manutenção.
* 🟢 **175_GERAR_FAIXA_COMERCIAL:** Precificador de margem bruta.
* 🟢 **176_KILLCRITIC_PRECIFICACAO:** Filtro auditor anti-prejuízo comercial. [🔴 CRÍTICO]
* 🟢 **177_GERAR_PROPOSTA_MARKDOWN:** Renderizador do documento.
* 🟢 **178_LOG_PRECIFICACAO:** Trace e compliance de preços.
* 🟢 **019_GERADOR_ORCAMENTO_RAPIDO:** Fluxo comercial rápido.
* 🟢 **190_MOTOR_ORCAMENTO_MASTER:** Módulo avançado em produção.

### Próxima fase prioritária — Novo Motor de Orçamento via Site

Integração planejada:

`Site DL_SITE_B2B → Formulário Avaliação Técnica V2 → /webhook/dl-receptor ou /webhook/orcamento-v2 → 060_ORCAMENTO_RECEPCAO_SITE_DL`

Workflows planejados:

* 🔵 **060_ORCAMENTO_RECEPCAO_SITE_DL**
* 🔵 **061_ORCAMENTO_ENRIQUECIMENTO_DADOS_DL**
* 🔵 **062_ORCAMENTO_ANALISE_VIDEO_IMAGEM_DL**
* 🔵 **063_ORCAMENTO_CALCULO_COMERCIAL_DL**
* 🔵 **064_ORCAMENTO_KILLCRITIC_DL**
* 🔵 **065_ORCAMENTO_GERADOR_PDF_GOTENBERG_DL**
* 🔵 **066_ORCAMENTO_ENVIO_E_FOLLOWUP_DL**

### Regra operacional obrigatória

`numero_unidades` é obrigatório para cálculo de rateio. Se faltar, bloquear cálculo de valor por unidade.

---

## 9. Site e Formulário de Orçamento

### Status

Site localizado.

### Dados

* **Caminho Local:** `d:\AntiGravity\projeto_01\DL_SITE_B2B`
* **Tecnologia:** HTML puro + CSS + Vanilla JS.
* **Home:** `index.html`
* **Formulário Principal:** `#dl-contact-form`
* **Webhook Principal:** `POST /webhook/dl-receptor`

### Definição dos formulários

* **Formulário atual:** captação de lead genérico; deve ser mantido como fallback.
* **Formulário V2:** Avaliação Técnica e entrada oficial do Motor de Orçamento.

### Campos atuais

`nome`, `whatsapp`, `email`, `nome_empresa_ou_condominio`, `tipo_cliente`, `cliente_ativo`, `bairro`, `cidade`, `servico_interesse`, `urgencia`, `melhor_horario`, `descricao`, `aceite_contato`, `aceite_lgpd`.

### Campos faltantes para V2

`cnpj`, `cpf`, `cep`, `endereco_completo`, `numero_unidades`, `numero_blocos`, `upload_video`, `upload_imagem`, `tipo_orcamento`, `responsavel_aprovacao`.

### Pendência correta

A pendência não é localizar o site. A pendência é evoluir o formulário para V2 e integrar ao Motor de Orçamento.

---

## 10. Google Drive e Agente Zelador

* ⏸️ **140_ZELADOR_MIDIAS_GOOGLE_DRIVE:** Pausado. Preservar como base de auditoria, descoberta e sugestão, sem execução destrutiva.
* 🔵 **140B_AGENTE_ZELADOR_EXECUTOR_MOVIMENTACAO_APROVADA:** Planejado. Executor seguro de movimentação aprovada. Deve iniciar com `GOOGLE_DRIVE_EXECUTOR_DRY_RUN=true`.

---

## 11. GitHub e Versionamento

### Status

🔴 **CRÍTICO / PARCIALMENTE RESOLVIDO**

### Regras

* Houve histórico com segredo antigo, incluindo Google OAuth.
* É obrigatório obter push limpo sem GH013.
* Push limpo não substitui rotação de credenciais.
* Tokens e chaves expostos devem ser invalidados e recriados nos provedores oficiais.
* Não considerar resolvido até:

  1. push limpo sem GH013;
  2. credenciais giradas;
  3. procedimento documentado.
