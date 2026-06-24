# Árvore Atualizada do Projeto DL Nexus n8n

**Objetivo:** Documentar a arquitetura real, o status operacional e a evolução do ecossistema DL Nexus, após a auditoria KILLCRITIC e remoção de redundâncias.
**Status Base:** Sincronizado a partir do `13_N8N_PRODUCAO_SYNC` e do ecossistema de arquivos locais reais.

---

## Legenda de Classificação
- 🟢 **ATIVO:** Em operação na produção.
- ⏸️ **PAUSADO:** Desativado temporariamente (`active=false`) ou aguardando deploy/credencial.
- 🟡 **HOMOLOGAÇÃO:** Existe, mas depende de teste real, migration, validação ou credenciais ativas.
- 🔵 **PLANEJADO:** Mapeado/desenhado, mas ainda não está operacional.
- ⚙️ **LEGADO / NÃO MEXER:** Workflows antigos preservados estritamente por histórico (nunca acionar).
- 🔴 **BLOQUEADO:** Gargalo real (token pendente, permissão negada, imagem pública pendente).

---

## 1. Infraestrutura Base
- 🟢 **004_skill_router_dl_nexus_v3:** Roteamento central de skills.
- 🟢 **008_mcp_server:** Motor de integração MCP.

## 2. Monitoramento e Segurança
- 🟢 **090_GUARDIAO_N8N_DL_NEXUS_V3:** Cão de guarda do ecossistema.
- 🟢 **091_SENTINELA_AUDITORIA_N8N_DL_NEXUS:** Rastreador de anomalias.
- 🟢 **147_SENTINELA_NOTICIAS_VERIFICADAS:** Filtro de desinformação.

## 3. Atendimento Aninha (IA Conversacional)
- 🟢 **001_TELEGRAM_RECEPCAO_ANINHA_V3:** Gateway de entrada via Telegram.
- 🟢 **002_roteador_aninha_v3_atendimento:** Direcionador de chamados.
- 🟢 **053_ANINHA_SOCIAL_HANDOFF_TELEGRAM:** Handoff de leads sociais para Telegram.
- 🟢 **054_ANINHA_SOCIAL_RELATORIO_DIARIO:** Geração de relatórios de atendimento.

## 4. SDR Social Meta (Facebook / Instagram)
- 🟢 **050_AGENTE_SDR_SOCIAL_DL:** Máquina de triagem de leads nas redes sociais.
- 🟢 **051_ANINHA_SOCIAL_MEMORIA_SUPABASE:** Persistência de conversação em banco relacional.
- 🟡 **052_ANINHA_SOCIAL_RESPOSTA_META:** Engrenagem de disparo de respostas diretas (depende de homologação para habilitar disparo real).

## 5. Prospecção Interna DL Nexus (Corporativo e Condominial)
- ⏸️ **130_PROSPECCAO_INTERNA_CORPORATIVA_CONDOMINIAL_DL:** Identificação de alvos no RJ (via DeepSeek/Gemini, pendente credenciais de produção).
- ⏸️ **060_AGENT_PROSPECCAO_ATIVA_DL:** Motor de contato ativo outbound (via DeepSeek/Gemini, pendente credenciais de produção).
- ⏸️ **070_CRON_PROSPECCAO_DIARIA_DL:** Disparador diário de prospecção.
- 🟢 **131_SCORING_LEADS_DL_NEXUS:** Máquina de pontuação térmica de leads.

## 6. Conteúdo e Marketing
- 🟢 **150_MAQUINA_CONTEUDO_DIARIA_DL:** Gerador central de pautas.
- 🟡 **151_MAQUINA_CONTEUDO_META_DL_4X_DIA:** Máquina autônoma de geração de conteúdo para Meta (Facebook/Instagram), 4x ao dia (08:00, 12:00, 18:00, 20:00), com KILLCRITIC integrado, armazenamento Google Drive, geração de imagem IA, suporte a carrossel (mín. 1/dia), linha editorial baseada em notícias e publicação direta nos workflows 082 e 081. HOMOLOGAÇÃO — pendente configuração de variáveis de ambiente e credenciais de IA/Google Drive no servidor.
- 🟢 **142_CLASSIFICADOR_TEMA_MIDIA:** Roteador temático.
- 🟢 **143_GERADOR_POST_EDUCATIVO_DL:** Criação específica de publicações técnicas.
- 🟢 **141_REVISOR_MIDIAS_DL_NEXUS:** Validador textual de copy.
- 🟢 **144_REVISOR_IA_DUPLO:** Dupla checagem anti-alucinação.

## 7. Publicação Facebook/Instagram Meta API
- ⏸️ **020_PUBLICADOR_SOCIAL_DL_NEXUS_V3_APROVACAO:** PAUSADO / CENTRAL DE APROVAÇÃO / DEPENDE DOS PUBLICADORES 081 E 082. O 151 já alimenta os publicadores diretamente.
- ⏸️ **146_PUBLICADOR_MULTICANAL_DL:** PAUSADO / ROTEADOR / NÃO VALIDADO COMO PUBLICADOR REAL.
- 🟡 **081_PUBLICADOR_INSTAGRAM_META_API:** HOMOLOGAÇÃO VALIDADA / PENDENTE INFRAESTRUTURA DE IMAGEM PÚBLICA (CDN ou endpoint DL). O 151 roteará automaticamente se `image_url_publica_meta` estiver disponível.
- 🟡 **082_PUBLICADOR_FACEBOOK_META_API:** HOMOLOGAÇÃO VALIDADA VIA GRAPH API / PENDENTE SINCRONIZAR TOKEN NO N8N CLOUD. O 151 já chama diretamente o endpoint `/feed` via HTTP Request com `$env.META_PAGE_ACCESS_TOKEN_DL`.

## 8. Motor de Precificação e Orçamento
- 🟢 **170_MOTOR_PRECIFICACAO_DL_NEXUS:** Orquestrador-mãe de valores.
- 🟢 **172_CALCULAR_MAO_DE_OBRA:** Worker de custo homem/hora.
- 🟢 **173_CALCULAR_MATERIAIS_TERCEIROS:** Worker de insumos.
- 🟢 **174_CALCULAR_SLA_PARTNER:** Custos de contratos de manutenção.
- 🟢 **175_GERAR_FAIXA_COMERCIAL:** Precificador de margem bruta.
- 🟢 **176_KILLCRITIC_PRECIFICACAO:** Filtro auditor anti-prejuízo comercial.
- 🟢 **177_GERAR_PROPOSTA_MARKDOWN:** Renderizador do documento.
- 🟢 **178_LOG_PRECIFICACAO:** Trace e compliance de preços.
- 🟢 **019_GERADOR_ORCAMENTO_RAPIDO:** Fluxo comercial rápido.
- 🟢 **190_MOTOR_ORCAMENTO_MASTER:** Módulo avançado.

## 9. Site e Formulário de Orçamento (Esteira V2/Site)
- 🟢 **060_ORCAMENTO_RECEPCAO_SITE_DL:** Status atual: operando como `/webhook/dl-receptor` via fallback #dl-contact-form. O V2 real ainda depende de importação/migration no servidor.
- 🟡 **061_ORCAMENTO_CLASSIFICADOR_CLIENTE_DL:** Criado interno, depende ativação n8n produção.
- 🟡 **062_ORCAMENTO_PLANILHA_GOOGLE_SHEETS_DL:** Criado interno, depende ativação n8n produção.
- 🟡 **063_ORCAMENTO_GERADOR_MARKDOWN_DL:** Criado interno, depende ativação n8n produção.
- 🟡 **064_ORCAMENTO_KILLCRITIC_DL:** Criado interno, depende ativação n8n produção.
- 🔵 **065_ORCAMENTO_GOOGLE_DOCS_PDF_DL:** Planejado.
- 🔵 **066_ORCAMENTO_ENVIO_E_FOLLOWUP_DL:** Planejado.
- 🔵 **067_AGENTE_EVOLUCAO_ORCAMENTOS_DL:** Planejado.

## 10. Google Drive e Agente Zelador
- ⚙️ **140_ZELADOR_MIDIAS_GOOGLE_DRIVE:** Operando apenas como auditor/sugestão (não destrutivo).
- 🔵 **140B_AGENTE_ZELADOR_EXECUTOR_MOVIMENTACAO_APROVADA:** Planejado (iniciará com GOOGLE_DRIVE_EXECUTOR_DRY_RUN=true).

## 11. GitHub e Versionamento
- 🔴 **Monitoramento de Credenciais:** Status crítico aguardando confirmação de rotação efetiva das credenciais legadas expostas na branch histórica (GH013). O push foi limpo, mas a rotação mandatório das chaves das plataformas de destino deve ser comprovada e mantida fora do controle de versão.

\n## 13. Motor Solar e Backup DL EcoVolt
- 🟢 **200_SOLAR_BACKUP_RECEPCAO_DADOS:** Recebe dados do cliente por formulário, WhatsApp, input manual ou planilha.
- 🟢 **201_SOLAR_BACKUP_ANALISE_CONTA_ENERGIA:** Analisa consumo, conta, tarifa, concessionária, tipo de ligação e histórico.
- 🟢 **202_SOLAR_BACKUP_CARGAS_CRITICAS:** Calcula cargas críticas, potência simultânea, autonomia, motores e prioridade.
- 🟢 **203_SOLAR_BACKUP_DIMENSIONAMENTO_BATERIAS:** Calcula energia necessária, bateria útil, bateria nominal, perdas, DoD, margem técnica e quantidade estimada.
- 🟢 **204_SOLAR_BACKUP_DIMENSIONAMENTO_INVERSOR:** Calcula potência do inversor, pico de partida, compatibilidade e margem.
- 🟢 **205_SOLAR_BACKUP_DIMENSIONAMENTO_FOTOVOLTAICO:** Calcula sistema solar preliminar em kWp conforme consumo, geração estimada, área e objetivo.
- 🟢 **206_SOLAR_BACKUP_BASE_EQUIPAMENTOS_CORSOLAR_SOLAX:** Consulta base de equipamentos, modelos, custos, compatibilidade e fornecedor.
- 🟢 **207_SOLAR_BACKUP_KILLCRITIC_TECNICO:** Audita riscos técnicos, comerciais, dados faltantes e promessas indevidas.
- 🟢 **208_SOLAR_BACKUP_GERADOR_PROPOSTA_MARKDOWN:** Gera proposta em Markdown com versão cliente e versão interna.
- 🟢 **209_SOLAR_BACKUP_GERADOR_PDF_GOOGLE_DOCS:** Gera Google Docs e PDF.
- 🟢 **210_SOLAR_BACKUP_AGENTE_EVOLUCAO_ORCAMENTOS:** Analisa orçamentos anteriores para melhorar o motor automaticamente.

## 12. Workflows Legados / Não Mexer
- ⚙️ **130_MANUS_PROSPECCAO_B2B_RJ** (`active=false`, Manus.IA removido, mantido para histórico)
- ⚙️ **060_AGENT_MANUS_PROSPECCAO_ATIVA** (`active=false`, Manus.IA removido, mantido para histórico)
- ⚙️ **070_CRON_MANUS_DIARIO** (`active=false`, Manus.IA removido, mantido para histórico)
