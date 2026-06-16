# BÍBLIA ARQUITETURAL DL NEXUS

=======================================================
🏢 1. IDENTIDADE E REGRA DE NEGÓCIO

- Empresa: DL Soluções Condominiais.
- Região de atuação prioritária: condomínios nas Zonas Sul, Sudoeste, Oeste e Norte do Rio de Janeiro.
- Liderança: Diogo Luiz de Oliveira é Tecnólogo em Infraestrutura e Pós-Graduado em Energia Solar.
- É terminantemente proibido referenciar a liderança como “engenheiro” em prompts, documentos, interfaces, propostas, schemas, comentários de código ou qualquer saída gerada.
- Pilares de atuação:
  - Elétrica
  - Energia Solar Híbrida
  - Mobilidade / CVE
  - Segurança Eletrônica
  - Prevenção de Incêndio
- Objetivo do sistema:
  O DL Nexus é uma máquina autônoma de captação, triagem, avaliação técnica, relacionamento, orçamento e fechamento de vendas.

=======================================================
🛠️ 2. A ARQUITETURA TÉCNICA (AS 4 CAMADAS)

▶ CAMADA 1: FRONTEND (A VITRINE E O CAMPO)

- Stack:
  - React
  - Vite
  - TailwindCSS
- Hospedagem:
  - Render
  - Serviço Web conectado ao GitHub
- Domínio principal:
  - nexus.dlsolucoescondominiais.com.br
- Interfaces obrigatórias:
  - Portal do Síndico
  - Dashboard Técnico
  - Checklist Mobile
  - Dashboard Comercial
  - Painel de Leads
  - Painel de Chamados
- Objetivo:
  - Permitir acompanhamento de propostas, chamados, KPIs, checklist técnico, andamento comercial e histórico do condomínio.

▶ CAMADA 2: ORQUESTRAÇÃO (A ESPINHA DORSAL)

- Stack:
  - n8n self-hosted
  - Docker
- Hospedagem:
  - VPS HostGator
- Função:
  - Receber webhooks Meta/WhatsApp
  - Receber e-mails
  - Receber formulários
  - Receber leads do site
  - Receber leads do Google Meu Negócio
  - Agendar tarefas via Cron
  - Enviar PDFs
  - Disparar e-mails
  - Disparar mensagens
  - Acionar agentes
  - Sincronizar Supabase
- Segurança:
  - Todo webhook exige HeaderAuth
  - Toda integração precisa de autenticação
  - Logs obrigatórios
  - Retry obrigatório
  - Fallback obrigatório

▶ CAMADA 3: CÉREBRO IA (O MOTOR PYTHON)

- Stack:
  - FastAPI
  - Antigravity
- Hospedagem:
  - VPS HostGator
- Agentes principais:
  - Aninha: triagem, classificação, atendimento inicial, agenda, qualificação e roteamento
  - Diego: orquestração técnica, distribuição de tarefas e supervisão dos agentes
  - Agentes Técnicos:
    - Elétrica
    - Solar
    - Segurança
    - Incêndio
    - Mobilidade
- Funções dos agentes:
  - Analisar imagens
  - Interpretar checklist
  - Gerar laudos
  - Classificar urgência
  - Criar orçamento
  - Criar follow-up
  - Criar resposta automática
  - Criar resumo de atendimento
- Integrações:
  - Google Drive via tec.network@gmail.com
  - Cache em memória
  - Controle de Rate Limit
  - Logs
  - Observabilidade

▶ CAMADA 4: BANCO DE DADOS (O COFRE)

- Stack:
  - Supabase
  - PostgreSQL
- Regras:
  - Uso obrigatório de UUID
  - Extensão uuid-ossp
  - RLS ativado rigorosamente
  - Realtime habilitado
  - Logs de auditoria
  - Soft delete quando necessário
- Tabelas principais esperadas:
  - leads
  - condominios
  - contatos
  - mensagens
  - mensagens_whatsapp
  - propostas
  - chamados
  - agendamentos
  - checklists
  - avaliacoes_tecnicas
  - anexos
  - agentes
  - audit_logs
  - notificacoes
  - campanhas
  - posts
  - followups

=======================================================
🔄 3. O FLUXO DO CRM (COMO A MÁQUINA GIRA)

Estágio 0 – Atração

- IA cria posts
- n8n publica no Instagram, Facebook, TikTok, Google Meu Negócio e site

Estágio 1 – Entrada

- Síndico entra por:
  - WhatsApp
  - Formulário
  - E-mail
  - Messenger
  - Instagram
  - Facebook
  - Google
  - TikTok
  - Site

Estágio 2 – Triagem

- Aninha classifica:
  - tipo de cliente
  - urgência
  - dor
  - serviço
  - localização
  - origem do lead
  - ticket estimado
- Depois cadastra tudo no Supabase

Estágio 3 – Gestão

- Lead aparece em tempo real no Dashboard React
- Equipe acompanha status, SLA, urgência, estágio comercial e responsável

Estágio 4 – Campo

- Técnico vai ao condomínio
- Preenche checklist mobile
- Faz upload de fotos
- Faz upload de documentos
- Salva tudo direto no banco

Estágio 5 – Fechamento

- Agente Python lê checklist
- Gera laudo
- Gera proposta técnica
- Gera PDF
- n8n dispara para orcamentos@dlsolucoescondominiais.com.br e para o cliente

Estágio 6 – Pós-venda

- Follow-up automático
- Solicitação de feedback
- Renovação de contrato
- Acompanhamento de manutenção
- Reativação de leads antigos

=======================================================
🔒 4. DIRETRIZES DE CÓDIGO

1. Nunca usar caminhos hardcoded Windows como D:/ ou C:/.
2. Sempre usar variáveis de ambiente e caminhos relativos.
3. Todo webhook deve ter autenticação.
4. Todo endpoint FastAPI deve validar origem e CORS.
5. Todo endpoint deve registrar logs.
6. Todo fluxo precisa ter retry.
7. Todo fluxo precisa ter fallback.
8. Todo código deve ser modular.
9. Todo código deve ser preparado para multi-tenant.
10. Toda integração deve ser desacoplada.
11. Nunca usar placeholders inúteis.
12. Sempre entregar código completo, funcional e otimizado.
13. Sempre agir como Desenvolvedor Sênior, Arquiteto de Soluções e Especialista em Google, Python, n8n, Supabase, FastAPI, React e automação corporativa.
