# Relatório: Esteira de Prospecção Social Assistida (Workflows 131, 132, 133)

## Visão Geral
A esteira de prospecção social da **DL Nexus V3** foi projetada para atuar em três estágios principais (Workflows 131, 132 e 133), garantindo segurança contra bloqueios (risco de spam) e alta personalização B2B para o setor de condomínios e colégios na região do Rio de Janeiro.

O foco da operação é a atração técnica de síndicos e gestores de facilities, evitando agressividade comercial e prezando pelo engajamento de autoridade.

## Estágios da Esteira

### 1. Workflow 131: Mapeamento e Triagem de Leads (Descoberta)
- **Objetivo**: Identificar síndicos e gestores de facilities em redes estratégicas como LinkedIn e Instagram.
- **Ação**: Faz a raspagem de dados permitidos (OSINT) ou utiliza webhooks do CRM para puxar novos leads potenciais.
- **Saída**: Cria o contexto inicial e estrutura o `lead_id` para o próximo nó de engajamento.

### 2. Workflow 132: Engajamento Social Assistido (Inteligência e Sugestão)
- **Objetivo**: Processar os dados do lead em conjunto com uma camada de inteligência (IA) para sugerir abordagens altamente consultivas.
- **Restrição Primordial**: É estritamente **proibido o envio automático ou não supervisionado**. O fluxo processa os dados e obrigatoriamente retorna a flag `precisa_aprovacao_humana=true`.
- **Glossário Termos de Qualidade (Regras Fortes)**:
  - Obrigatório uso do termo **"Avaliação Técnica"** (o termo "visita técnica" é banido).
  - Obrigatório uso do termo **"Tecnólogo Responsável"** ou "Responsável Técnico" (o uso de nomes pessoais para os agentes é banido nesta camada de automação).
- **Análise de Risco**: Avalia o perfil da mensagem e canalugerido, sinalizando o `risco_spam` (baixo/médio/alto) com base no tamanho do comentário, formato e gatilhos linguísticos de venda.

### 3. Workflow 133: Execução e Registro (Aprovação e Acionamento)
- **Objetivo**: Após aprovação manual (Human-in-the-loop), o workflow 133 orquestra o fechamento da tarefa. Ele pode interagir com integrações de postagem oficial se aplicável, ou atualizar o status e histórico de relacionamento (CRM/Supabase) como "Engajamento Finalizado".
- **Gatilho**: Recebe o payload do estágio 132 apenas com a confirmação positiva do analista de vendas.

## Diretrizes de Segurança e Compliance B2B (DL Soluções Condominiais)
1. **Nenhum envio desassistido** é permitido via DMs, WhatsApp ou comentários de redes sociais nesta fase do pipeline. Tudo é enviado como sugestão na esteira.
2. Todo comentário ou DM gerado pelo workflow 132 foca em agregar valor através de soluções de engenharia, como: **Automação Predial, CFTV, Energia Solar (Lei 14.300), Projetos de Incêndio e Elétrica**.
3. **Proteção de Segredos**: Nenhuma chave de API, Bearer Token ou senha trafega nos payloads dos nós. Sempre confie nas Credenciais Nativas do n8n (ex: 'OAuth2 Google Business', 'Conta do Telegram').
4. A lógica da arquitetura sempre prevê o bloqueio nativo (`active=false`) no versionamento para evitar acionamento não supervisionado ao efetuar uploads das automações.

> Este relatório documenta a consistência estrutural e obediência às diretrizes rígidas da empresa na construção da esteira de automação comercial e social.
