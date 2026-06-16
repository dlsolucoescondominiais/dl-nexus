# UPDATE TÉCNICO — DL NEXUS V3 / N8N / DEVOPS

**Empresa:** DL Soluções Condominiais
**Responsável:** Diogo Luiz de Oliveira — Tecnólogo responsável
**Ambiente principal:** https://n8n.dlsolucoescondominiais.com.br
**Projeto local:** D:\AntiGravity\projeto_01
**Base local:** DL_NEXUS_V3_LOCAL
**Container n8n:** n8n-main

## 1. Status atual da VPS e n8n
- **Acesso:** n8n online e acessível publicamente em `https://n8n.dlsolucoescondominiais.com.br`.
- **Infraestrutura:** Docker + Traefik atuando como proxy reverso, com certificado HTTPS ativo.
- **Correção Aplicada:** A variável `WEBHOOK_URL` foi ajustada para gerar URLs públicas corretamente (substituindo o antigo comportamento de localhost:5678).

## 2. Observação de Segurança (Obrigatória)
- **Diretriz Máxima:** Nenhuma credencial (senhas, tokens, JWT, API Keys) será exposta em relatórios, prompts, GitHub, JSON ou chat.
- **Máscaras Utilizadas:** `***OCULTO***`, `SENHA_PADRAO_DOS_EMAILS`, `N8N_API_TOKEN_AQUI`, `SUPABASE_SERVICE_KEY_AQUI`, `META_TOKEN_AQUI`.
- **Status de Senhas:** A senha padronizada dos e-mails é tratada como comprometida e deve ser rotacionada após a estabilização.

## 3. Status HostGator/Titan E-mail
- **Domínio:** `dlsolucoescondominiais.com.br`
- **Contas Relevantes:** admin, contato, suporte, sac, vendas (todas @dlsolucoescondominiais.com.br).
- **Status:** Pronto para integração.
- **Próximos Passos:** Validar configurações operacionais de IMAP/SMTP no n8n para `vendas@` e `suporte@` como ponto de entrada principal, dado o bloqueio atual do WhatsApp.

## 4. Status Meta / WhatsApp
- **Número pretendido:** 21 99269-8612
- **Número humano/principal:** 21 96474-2458
- **Status:** CONTA RESTRITA na Meta. O WhatsApp está temporariamente bloqueado para a API.
- **Diretrizes Atuais:**
  - NÃO forçar contato com a Meta.
  - NÃO utilizar o número humano/principal em automações.
  - NÃO criar automações de WhatsApp até resolução da restrição.
  - **Foco redirecionado para:** Webhooks HTTP, Supabase e E-mail.

## 5. Status dos workflows DL Nexus V3
- **Importados com Sucesso:**
  - `003_roteador_diego_v3_killcritic` (Triagem Técnica)
  - `004_skill_router_dl_nexus_v3` (Roteamento para Skills)
  - `002_roteador_aninha_v3_killcritic` (Triagem Comercial/Síndicos)

## 6. Próximos workflows a processar
- **019_GERADOR_ORCAMENTO_RAPIDO:** Precisa gerar rascunhos de orçamento separando custos (implantação, mensalidade, SLA, peças, equipamentos, chamados). Nunca prometer preço final sem aprovação humana.
- **060_AGENT_MANUS_PROSPECCAO_ATIVA:** Processar prospecção estruturada com JSON limpo, sem publicações/envios automáticos.

## 7. Problema operacional identificado: 007_tarefas_background
- **Sintoma:** Execuções falhando no painel n8n.
- **Diagnóstico Preliminar:** Usa `n8n-nodes-base.scheduleTrigger` (intervalo de 5 min) e lê a tabela `tarefas` no Supabase. O erro pode ser de credenciais expiradas/inválidas para a API do Supabase (`id: QzziIRhKJMDNAE1m`).
- **Ação Recomendada:** Manter inativo ou revisar credenciais no n8n. Não apagar.

## 8. Regras KILLCRITIC Aplicadas
- Nunca usar "visita técnica" (substituir por "Avaliação Técnica").
- Nunca chamar Diogo de "engenheiro" ("Tecnólogo responsável" ou "Responsável Técnico").
- Não sugerir canaleta plástica.
- Não vender hidráulica pura.
- Sem promessas de preços finais sem Avaliação Técnica.
- Separação clara de rubricas financeiras.
- Prioridade para contratos recorrentes (DL Partner, Fortress).
- Garantia apenas "estendida durante vigência do contrato".
- Sem WhatsApp/postagens automáticas a frio.

## 9. Prioridades Imediatas (Plano de Ação Raphael)
1. **Prioridade 1:** Credenciais IMAP/SMTP reais no n8n para vendas/suporte e validação de `000_email_receptor`.
2. **Prioridade 2:** Conexão Supabase/Postgres real com n8n.
3. **Prioridade 3:** Testar fluxos Aninha, Diego e Skill Router via Webhook HTTP.
4. **Prioridade 4:** Diagnosticar erro no node do Supabase no workflow `007_tarefas_background`.
5. **Prioridade 5:** Configurar Google Drive para mídia.
