# Relatório de Lacunas, Métricas e Dados Necessários - DL Nexus V3

## Resumo Executivo
Este documento apresenta uma análise crítica e arquitetural do estado atual do projeto **DL Nexus V3**. O objetivo é mapear detalhadamente as lacunas técnicas, operacionais e comerciais que impedem a transição de um ambiente de desenvolvimento/mock para uma operação autônoma real e segura. As informações aqui contidas garantem o cumprimento das diretrizes KILLCRITIC e protegem a operação da DL Soluções Condominiais contra riscos financeiros, de imagem e operacionais. Nenhuma ação no ambiente de produção deve ser tomada sem a resolução dos itens listados neste relatório.

---

## Estado Atual da Arquitetura

### O que já está implantado
* `003_roteador_diego_v3_killcritic` (Importado no n8n com sucesso)
* `004_skill_router_dl_nexus_v3` (Importado no n8n com sucesso)
* `002_roteador_aninha_v3_killcritic` (Já existia no n8n)

### O que está conectado de verdade
* *PENDENTE DE CONFIRMAÇÃO* (Necessita auditoria técnica rigorosa nos nodes ativos do n8n para validar quais conexões possuem credenciais de produção válidas e funcionais).

### O que está apenas planejado (PLANEJADO, NÃO VALIDADO)
* Integração final e autônoma do Manus para prospecção ativa (`060_AGENT_MANUS_PROSPECCAO_ATIVA`).
* Gerador de Orçamento Rápido (`019_GERADOR_ORCAMENTO_RAPIDO`).
* Atendimento autônomo end-to-end integrando DeepSeek, Kimi, Claude e Gemini com ações no mundo real.
* Estrutura de banco de mídias e datasheets no Google Drive.
* CRM completo e centralizado no Supabase.

### O que está mockado
* Estruturas de banco de dados locais utilizadas para testes de scripts.
* Workflows não importados ou cujos nodes não possuam credenciais reais preenchidas.
* Simulações de chamadas de APIs externas (ex: Gemini, ElevenLabs) nos ambientes de teste.

### O que ainda depende de credencial (DEPENDE DE CREDENCIAL)
* WhatsApp Meta (Número 21 99269-8612).
* E-mail IMAP/SMTP (HostGator/Titan).
* Telegram Bot.
* Redes Sociais: Instagram, Facebook Page/Business Manager, TikTok, Google Meu Negócio.
* Integração de IA de produção: ElevenLabs, DeepSeek, Kimi/KimiClaw/PicoClaw.
* Google Drive (Permissões da API e tokens OAuth/Service Account).
* Supabase (Anon Key, Service Role Key válidas e seguras).

### O que ainda depende de decisão comercial (PENDENTE DE CONFIRMAÇÃO)
* Metas financeiras e de volume (faturamento, propostas/mês, leads/dia).
* Estratégia de precificação (Preço mínimo de produtos como Fortress, margens mínimas).
* Custos operacionais base (Equipe, deslocamento, licenças).
* Limites de autonomia dos Agentes IA (Quando aprovar automaticamente vs Quando exigir aprovação humana).
* SLA de resposta, orçamento e Avaliação Técnica por perfil de cliente.
* Produtos prioritários para push ativo.
* Autorização explícita para disparo de respostas automáticas.

### O que ainda depende de teste operacional (DEPENDE DE TESTE OPERACIONAL)
* Resolução do erro no workflow `007_tarefas_background`.
* Funcionalidade completa dos roteadores V3 com payloads reais de Meta/Webhook.
* Validação de ponta a ponta: Entrada do lead -> Triagem Aninha -> Análise Diego -> Skill Router -> Resposta/Registro no Supabase.
* Confirmação de que os webhooks internos do n8n (headerAuth) estão funcionando sem bloquear tráfego legítimo do roteador.
* Envio de email real via HostGator/Titan.

---

## Blocos de Análise e Perguntas Mapeadas

### A) Métricas comerciais necessárias
* Meta mensal de faturamento: *PENDENTE DE CONFIRMAÇÃO*
* Meta de contratos recorrentes DL Partner: *PENDENTE DE CONFIRMAÇÃO*
* Ticket médio desejado: *PENDENTE DE CONFIRMAÇÃO*
* Margem mínima por produto: *PENDENTE DE CONFIRMAÇÃO*
* Preço mínimo de Fortress: *PENDENTE DE CONFIRMAÇÃO*
* Custo real de cada licença/plataforma: *PENDENTE DE CONFIRMAÇÃO*
* Custo de equipe: *PENDENTE DE CONFIRMAÇÃO*
* Custo de deslocamento: *PENDENTE DE CONFIRMAÇÃO*
* Regiões prioritárias: *PENDENTE DE CONFIRMAÇÃO*
* Número de leads por dia: *PENDENTE DE CONFIRMAÇÃO*
* Número de posts por dia/semana: *PENDENTE DE CONFIRMAÇÃO*
* Número de propostas por semana: *PENDENTE DE CONFIRMAÇÃO*
* SLA desejado por tipo de cliente: *PENDENTE DE CONFIRMAÇÃO*

### B) Métricas operacionais necessárias
* Quantos chamados/dia a DL suporta: *PENDENTE DE CONFIRMAÇÃO*
* Quem atende WhatsApp: *PENDENTE DE CONFIRMAÇÃO*
* Quem aprova posts: *PENDENTE DE CONFIRMAÇÃO*
* Quem aprova propostas: *PENDENTE DE CONFIRMAÇÃO*
* Quem executa serviço de campo (Avaliação Técnica): *PENDENTE DE CONFIRMAÇÃO*
* Horários de atendimento: *PENDENTE DE CONFIRMAÇÃO*
* Tempo máximo de resposta: *PENDENTE DE CONFIRMAÇÃO*
* Tempo máximo para orçamento: *PENDENTE DE CONFIRMAÇÃO*
* Tempo máximo para Avaliação Técnica: *PENDENTE DE CONFIRMAÇÃO*
* Capacidade semanal de execução: *PENDENTE DE CONFIRMAÇÃO*
* Quais serviços não devem ser aceitos: *PENDENTE DE CONFIRMAÇÃO* (Confirmado exclusão de hidráulica pura via KILLCRITIC)

### C) Dados técnicos necessários
* Status real das credenciais n8n: *DEPENDE DE VERIFICAÇÃO*
* Credenciais IMAP/SMTP HostGator/Titan: *DEPENDE DE CREDENCIAL*
* Status real Meta WhatsApp: *DEPENDE DE CREDENCIAL*
* Status real Instagram/Facebook: *DEPENDE DE CREDENCIAL*
* Status real TikTok: *DEPENDE DE CREDENCIAL*
* Status real Telegram Bot: *DEPENDE DE CREDENCIAL*
* Status real Google Drive: *DEPENDE DE CREDENCIAL*
* Status real Supabase: *DEPENDE DE CREDENCIAL*
* Status real DeepSeek: *DEPENDE DE CREDENCIAL*
* Status real ElevenLabs: *DEPENDE DE CREDENCIAL*
* Status real Manus: *DEPENDE DE CREDENCIAL*
* Status real Kimi/KimiClaw/PicoClaw: *DEPENDE DE CREDENCIAL*
* Quais nodes n8n já têm credenciais configuradas: *DEPENDE DE VERIFICAÇÃO*
* Quais workflows estão ativos: *DEPENDE DE VERIFICAÇÃO*
* Quais workflows estão com erro: *DEPENDE DE VERIFICAÇÃO*

### D) Dados de banco/Supabase necessários
* Quais tabelas existem: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela leads: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela clientes: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela propostas: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela chamados: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela posts: *PENDENTE DE CONFIRMAÇÃO*
* Se existe tabela logs: *PENDENTE DE CONFIRMAÇÃO*
* Campos obrigatórios de cada tabela: *PENDENTE DE CONFIRMAÇÃO*
* RLS está ativo ou não: *DEPENDE DE VERIFICAÇÃO*
* Chaves anon/service role estão seguras ou não: *DEPENDE DE VERIFICAÇÃO*
* Onde o n8n grava dados hoje: *PENDENTE DE CONFIRMAÇÃO*

### E) Dados de Google Drive necessários
* ID da pasta raiz do banco de mídia: *PENDENTE DE CONFIRMAÇÃO*
* Se a estrutura DL_NEXUS_MIDIA_E_DATASHEETS existe: *PENDENTE DE CONFIRMAÇÃO*
* Pastas por produto: *PENDENTE DE CONFIRMAÇÃO*
* Quem pode acessar: *PENDENTE DE CONFIRMAÇÃO*
* Se o n8n tem permissão: *DEPENDE DE VERIFICAÇÃO*
* Onde salvar posts aprovados: *PENDENTE DE CONFIRMAÇÃO*
* Onde salvar propostas: *PENDENTE DE CONFIRMAÇÃO*
* Onde salvar relatórios: *PENDENTE DE CONFIRMAÇÃO*

### F) Dados de e-mail necessários
* Quais contas serão lidas: *PENDENTE DE CONFIRMAÇÃO*
* Se cada conta tem IMAP ativo: *DEPENDE DE VERIFICAÇÃO*
* Se cada conta tem SMTP ativo: *DEPENDE DE VERIFICAÇÃO*
* Limites de envio: *PENDENTE DE CONFIRMAÇÃO*
* Regras anti-loop: *PLANEJADO, NÃO VALIDADO*
* Assinatura padrão: *PENDENTE DE CONFIRMAÇÃO*
* Respostas automáticas permitidas: *PENDENTE DE CONFIRMAÇÃO*
* E-mails que nunca devem receber auto-resposta: *PENDENTE DE CONFIRMAÇÃO*
* Quem recebe cópia: *PENDENTE DE CONFIRMAÇÃO*
* Como classificar comercial, suporte, SAC, financeiro, fornecedor e spam: *PENDENTE DE CONFIRMAÇÃO*

### G) Dados de WhatsApp/Meta necessários
* WABA ID: *DEPENDE DE CREDENCIAL*
* Phone Number ID: *DEPENDE DE CREDENCIAL*
* Token permanente ou temporário: *DEPENDE DE CREDENCIAL*
* Webhook callback URL: *DEPENDE DE VERIFICAÇÃO*
* Verify token: *DEPENDE DE CREDENCIAL*
* Status do número 21 99269-8612: *DEPENDE DE VERIFICAÇÃO*
* Se o número está no WhatsApp Business app ou Cloud API: *PENDENTE DE CONFIRMAÇÃO*
* Templates aprovados: *PENDENTE DE CONFIRMAÇÃO*
* Política para responder mensagens recebidas: *PENDENTE DE CONFIRMAÇÃO*
* Regra para não fazer cold outreach: *PLANEJADO, NÃO VALIDADO*
* Quem aprova respostas: *PENDENTE DE CONFIRMAÇÃO*

### H) Dados de redes sociais necessários
* Instagram conectado: *DEPENDE DE VERIFICAÇÃO*
* Facebook Page ID: *DEPENDE DE CREDENCIAL*
* Business Manager ID: *DEPENDE DE CREDENCIAL*
* TikTok API disponível: *DEPENDE DE VERIFICAÇÃO*
* Google Meu Negócio conectado: *DEPENDE DE VERIFICAÇÃO*
* Frequência de postagem: *PENDENTE DE CONFIRMAÇÃO*
* Temas prioritários: *PENDENTE DE CONFIRMAÇÃO*
* Aprovações obrigatórias: *PENDENTE DE CONFIRMAÇÃO*
* Onde buscar imagens: *PENDENTE DE CONFIRMAÇÃO*
* Onde salvar rascunhos: *PENDENTE DE CONFIRMAÇÃO*
* Formato de post por rede: *PENDENTE DE CONFIRMAÇÃO*

### I) Dados dos agentes necessários
* Prompt final da Aninha: *PLANEJADO, NÃO VALIDADO*
* Prompt final do Diego: *PLANEJADO, NÃO VALIDADO*
* Prompt final SocialPilot: *PLANEJADO, NÃO VALIDADO*
* Prompt final Procurement: *PLANEJADO, NÃO VALIDADO*
* Prompt final Customer Success: *PLANEJADO, NÃO VALIDADO*
* Prompt final Dispatcher: *PLANEJADO, NÃO VALIDADO*
* Prompt final DBA/Supabase: *PLANEJADO, NÃO VALIDADO*
* Tom de voz: *PENDENTE DE CONFIRMAÇÃO*
* Limites de autonomia: *PENDENTE DE CONFIRMAÇÃO*
* Quando escalar para Diogo: *PENDENTE DE CONFIRMAÇÃO*
* Quando escalar para Raphael: *PENDENTE DE CONFIRMAÇÃO*
* Quando escalar para equipe de campo: *PENDENTE DE CONFIRMAÇÃO*

### J) Riscos e pendências
* 007_tarefas_background com erro: *DEPENDE DE TESTE OPERACIONAL*
* Risco de loops: *DEPENDE DE TESTE OPERACIONAL*
* Risco de auto-resposta indevida: *PLANEJADO, NÃO VALIDADO*
* Risco de WhatsApp banido: *DEPENDE DE VERIFICAÇÃO*
* Risco de token expirado: *DEPENDE DE VERIFICAÇÃO*
* Risco de workflow duplicado: *PLANEJADO, NÃO VALIDADO*
* Risco de JSON sem id: *PLANEJADO, NÃO VALIDADO*
* Risco de workflows mock serem confundidos com produção real: *PLANEJADO, NÃO VALIDADO*
* Risco de post sem aprovação: *PLANEJADO, NÃO VALIDADO*
* Risco de proposta com preço automático: *PLANEJADO, NÃO VALIDADO*

---

## Lista de Perguntas para Diogo Responder
- Metas comerciais (faturamento, ticket médio, número de leads/posts/propostas).
- Preços mínimos (ex: Fortress), margens aceitáveis e custos operacionais (equipe, licenças, deslocamento).
- Prioridades de vendas (regiões prioritárias e foco no modelo DL Partner).
- Limites de atendimento (tempo de resposta máximo, SLA para orçamentos e Avaliação Técnica).
- Autorização de publicação autônoma em redes sociais vs. aprovação manual.
- Autorização de respostas automáticas no WhatsApp para prospects ou clientes ativos.
- Política rígida sobre serviços não aceitos.

## Lista de Perguntas para Raphael Responder
- Status real das credenciais em produção (API Meta WhatsApp 21 99269-8612, IMAP/SMTP Titan, Telegram, Redes Sociais).
- Status real dos workflows (O que está realmente rodando com sucesso).
- Causa raiz do nó/workflow com erro (`007_tarefas_background`).
- Funcionalidade atual das integrações essenciais (Supabase está com RLS e tabelas ativas? Google Drive está mapeado e acessível?).

## Lista de Perguntas Técnicas (Para quem tem acesso ao n8n)
- Quais nodes de autenticação (OAuth2/Header) já estão validados no n8n Cloud?
- Os tokens temporários foram convertidos em tokens permanentes (System User / Service Accounts)?
- Existem logs detalhados de payload falho para investigar os erros recentes de execuções?

---

## Checklists de Ativação

### Checklist de Dados Mínimos para Ativar "Operação Assistida" (Human in the Loop)
- [ ] Credenciais validadas (Supabase, Meta/WhatsApp, Email Principal).
- [ ] Conexão n8n -> Supabase testada (Leitura e Escrita na tabela de Leads/Logs).
- [ ] Workflows de entrada configurados apenas para roteamento e notificação interna (Sem auto-resposta externa).
- [ ] Prompt base dos Agentes (Aninha/Diego) definidos e alinhados com KILLCRITIC.
- [ ] Diogo recebe notificação (ex: Telegram) com o draft da resposta/proposta para aprovação manual.
- [ ] Tratamento de Erros básico ativo.

### Checklist de Dados Mínimos para Ativar "Automação Real" (Fully Autonomous)
- [ ] Todas as exigências da "Operação Assistida" validadas.
- [ ] Modelos de precificação e metas comerciais parametrizadas no sistema.
- [ ] SLAs definidos e monitorados via `007_tarefas_background`.
- [ ] Templates do WhatsApp Business API aprovados pela Meta.
- [ ] Regras estritas de *rate limit* e anti-loop configuradas em todos os canais.
- [ ] Banco de Mídias e Datasheets populado no Google Drive e mapeado no n8n.
- [ ] RLS (Row Level Security) ativo no Supabase.
- [ ] Aprovação comercial e legal explícita para o envio autônomo de orçamentos (respeitando a regra de necessitar Avaliação Técnica).

---

## Próximo Passo Recomendado (Sem executar nada)

1. Reunião de alinhamento com Diogo e Raphael para preenchimento das lacunas comerciais e técnicas documentadas no arquivo `PERGUNTAS_OBJETIVAS_PARA_DIOGO_E_RAPHAEL.md`.
2. Após o preenchimento, auditar exclusivamente o n8n e o Supabase em produção para validar tecnicamente as respostas recebidas.
