-- ==============================================================================
-- DL NEXUS - ESQUEMA DE FUNIL SOCIAL E ATENDIMENTO B2B
-- ==============================================================================

-- 1. Tabela de Campanhas (Publicador Social Automático)
CREATE TABLE IF NOT EXISTS dl_campaigns (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    linha_servico VARCHAR(100),
    tipo_conteudo VARCHAR(100),
    palavra_chave VARCHAR(100),
    cta_principal TEXT,
    
    -- Controle de Agendamento e Auto-Publish
    status_aprovacao VARCHAR(50) DEFAULT 'draft_created', 
    -- status possíveis: draft_created, killcritic_approved, auto_published, blocked_by_killcritic, needs_human_review, publication_failed, deleted_manually, lead_generated
    permitir_publicacao_automatica BOOLEAN DEFAULT true,
    scheduled_for TIMESTAMP WITH TIME ZONE,
    
    -- Conteúdos multi-canal reaproveitados
    conteudo_instagram JSONB,
    conteudo_facebook JSONB,
    conteudo_tiktok JSONB,
    conteudo_gmb JSONB,
    
    -- Rastreamento Pós-Publicação e Fallback
    publicado_em_instagram TIMESTAMP WITH TIME ZONE,
    publicado_em_facebook TIMESTAMP WITH TIME ZONE,
    publicado_em_tiktok TIMESTAMP WITH TIME ZONE,
    publicado_em_gmb TIMESTAMP WITH TIME ZONE,
    
    url_publicacao_instagram TEXT,
    url_publicacao_facebook TEXT,
    url_publicacao_tiktok TEXT,
    url_publicacao_gmb TEXT,
    
    erros_publicacao JSONB DEFAULT '{}'::jsonb,
    publication_attempts INT DEFAULT 0,
    
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Tabela de Eventos Sociais (Social Listener)
CREATE TABLE IF NOT EXISTS dl_social_events (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    campaign_id UUID REFERENCES dl_campaigns(id) ON DELETE SET NULL,
    canal VARCHAR(50) NOT NULL, -- instagram, facebook, tiktok, gmb, whatsapp
    origem VARCHAR(50) NOT NULL, -- direct, comentario, feed, whatsapp_api
    usuario_nome VARCHAR(255),
    usuario_id VARCHAR(255) NOT NULL,
    mensagem TEXT,
    palavra_chave_detectada VARCHAR(100),
    tipo_evento VARCHAR(50), -- orcamento, duvida, suporte, emergencia, humano
    processado BOOLEAN DEFAULT false,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    UNIQUE(canal, usuario_id, mensagem, criado_em) -- Anti-duplicidade na entrada
);

-- 3. Tabela de Leads Qualificados (Router -> CRM)
CREATE TABLE IF NOT EXISTS dl_leads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    social_event_id UUID REFERENCES dl_social_events(id) ON DELETE SET NULL,
    nome VARCHAR(255),
    telefone VARCHAR(50),
    empresa_condominio VARCHAR(255),
    bairro VARCHAR(100),
    servico VARCHAR(255),
    urgencia VARCHAR(50), -- baixa, media, alta, imediata
    status VARCHAR(50) DEFAULT 'novo', -- novo, em_atendimento, qualificado, perdido, convertido
    responsavel VARCHAR(100), -- aninha, diogo, equipe_tecnica
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 4. Tabela de Sessões da Aninha (Estado de Conversa / Anti-Loop)
CREATE TABLE IF NOT EXISTS dl_aninha_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    lead_id UUID REFERENCES dl_leads(id) ON DELETE CASCADE,
    usuario_id VARCHAR(255) NOT NULL,
    canal VARCHAR(50) NOT NULL,
    estado_conversa VARCHAR(50) DEFAULT 'coleta_inicial', -- coleta_inicial, qualificacao, handoff_humano, encerrado
    ultima_mensagem TEXT,
    tentativas_loop INT DEFAULT 0,
    precisa_humano BOOLEAN DEFAULT false,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()),
    UNIQUE(usuario_id, canal)
);

-- Indexes para performance
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON dl_campaigns(status_aprovacao);
CREATE INDEX IF NOT EXISTS idx_campaigns_scheduled ON dl_campaigns(scheduled_for);
CREATE INDEX IF NOT EXISTS idx_events_usuario ON dl_social_events(usuario_id, processado);
CREATE INDEX IF NOT EXISTS idx_leads_telefone ON dl_leads(telefone);
CREATE INDEX IF NOT EXISTS idx_aninha_sessions_usuario ON dl_aninha_sessions(usuario_id);
