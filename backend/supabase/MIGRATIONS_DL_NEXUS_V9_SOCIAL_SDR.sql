-- =============================================
-- DL SOLUÇÕES CONDOMINIAIS — MIGRATION V9
-- SDR Social: Instagram Direct + Facebook Messenger
-- Tabelas para 050_AGENTE_SDR_SOCIAL_DL
-- Data: 2026-06-15
-- =============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- TABELA: dl_social_conversas
-- Rastreia cada conversa por canal_origem + sender_id
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_social_conversas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Identificação do canal
    canal_origem VARCHAR(50) NOT NULL,  -- instagram_direct, facebook_messenger
    sender_id VARCHAR(100) NOT NULL,
    page_id VARCHAR(100),
    instagram_business_account_id VARCHAR(100),

    -- Dados do contato
    nome_contato VARCHAR(255),
    username VARCHAR(255),
    telefone VARCHAR(50),
    email VARCHAR(255),

    -- Qualificação
    tipo_cliente VARCHAR(100),
    nome_condominio_empresa VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255) DEFAULT 'Rio de Janeiro',
    servico_interesse TEXT,
    urgencia VARCHAR(50),

    -- Estado da conversa
    status_conversa VARCHAR(50) DEFAULT 'ativa',
    etapa_funil VARCHAR(100) DEFAULT 'recepcao',
    lead_score INTEGER DEFAULT 0,
    responsavel_humano VARCHAR(255),
    precisa_humano BOOLEAN DEFAULT FALSE,
    ultimo_resumo TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    raw_profile JSONB DEFAULT '{}'::jsonb,

    CONSTRAINT uq_social_conversa_canal_sender UNIQUE (canal_origem, sender_id)
);

CREATE INDEX IF NOT EXISTS idx_social_conv_canal_sender ON dl_social_conversas(canal_origem, sender_id);
CREATE INDEX IF NOT EXISTS idx_social_conv_status ON dl_social_conversas(status_conversa);
CREATE INDEX IF NOT EXISTS idx_social_conv_etapa ON dl_social_conversas(etapa_funil);
CREATE INDEX IF NOT EXISTS idx_social_conv_created ON dl_social_conversas(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_social_conv_humano ON dl_social_conversas(precisa_humano) WHERE precisa_humano = true;

-- ==========================================
-- TABELA: dl_social_mensagens
-- Log completo de mensagens (inbound/outbound/internal)
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_social_mensagens (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    conversa_id UUID REFERENCES dl_social_conversas(id) ON DELETE SET NULL,
    canal_origem VARCHAR(50) NOT NULL,
    sender_id VARCHAR(100),
    direction VARCHAR(20) NOT NULL DEFAULT 'inbound',  -- inbound, outbound, internal
    message_id VARCHAR(255),
    texto TEXT,
    tipo_mensagem VARCHAR(50) DEFAULT 'text',
    raw_event JSONB DEFAULT '{}'::jsonb,
    status_processamento VARCHAR(50) DEFAULT 'recebido'
);

-- Unique constraint on canal+message_id to prevent duplicates (only when message_id is not null)
CREATE UNIQUE INDEX IF NOT EXISTS idx_social_msg_dedup
    ON dl_social_mensagens(canal_origem, message_id)
    WHERE message_id IS NOT NULL AND message_id != '';

CREATE INDEX IF NOT EXISTS idx_social_msg_conversa ON dl_social_mensagens(conversa_id);
CREATE INDEX IF NOT EXISTS idx_social_msg_canal_sender ON dl_social_mensagens(canal_origem, sender_id);
CREATE INDEX IF NOT EXISTS idx_social_msg_created ON dl_social_mensagens(created_at DESC);

-- ==========================================
-- TABELA: dl_social_leads
-- Leads qualificados extraídos das conversas
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_social_leads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    conversa_id UUID REFERENCES dl_social_conversas(id) ON DELETE SET NULL,
    canal_origem VARCHAR(50),
    nome VARCHAR(255),
    username VARCHAR(255),
    telefone VARCHAR(50),
    email VARCHAR(255),
    tipo_cliente VARCHAR(100),
    nome_condominio_empresa VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255) DEFAULT 'Rio de Janeiro',
    servico_interesse TEXT,
    urgencia VARCHAR(50),
    dor_principal TEXT,
    cargo_decisor VARCHAR(255),
    lead_score INTEGER DEFAULT 0,
    status_lead VARCHAR(50) DEFAULT 'novo',
    proxima_acao TEXT,
    data_preferida_avaliacao VARCHAR(255),
    observacoes TEXT,
    origem_ia VARCHAR(100) DEFAULT 'aninha_sdr_social'
);

CREATE INDEX IF NOT EXISTS idx_social_lead_status ON dl_social_leads(status_lead);
CREATE INDEX IF NOT EXISTS idx_social_lead_score ON dl_social_leads(lead_score DESC);
CREATE INDEX IF NOT EXISTS idx_social_lead_canal ON dl_social_leads(canal_origem);
CREATE INDEX IF NOT EXISTS idx_social_lead_conversa ON dl_social_leads(conversa_id);
CREATE INDEX IF NOT EXISTS idx_social_lead_created ON dl_social_leads(created_at DESC);

-- ==========================================
-- Row Level Security
-- ==========================================
ALTER TABLE dl_social_conversas ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_social_mensagens ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_social_leads ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist (idempotent)
DROP POLICY IF EXISTS "service_full_access_social_conversas" ON dl_social_conversas;
DROP POLICY IF EXISTS "service_full_access_social_mensagens" ON dl_social_mensagens;
DROP POLICY IF EXISTS "service_full_access_social_leads" ON dl_social_leads;

CREATE POLICY "service_full_access_social_conversas" ON dl_social_conversas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_social_mensagens" ON dl_social_mensagens FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_social_leads" ON dl_social_leads FOR ALL USING (true) WITH CHECK (true);

-- ==========================================
-- Trigger para updated_at automático
-- ==========================================
CREATE OR REPLACE FUNCTION update_social_conversas_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_social_conversas_updated_at ON dl_social_conversas;
CREATE TRIGGER trg_social_conversas_updated_at
    BEFORE UPDATE ON dl_social_conversas
    FOR EACH ROW EXECUTE FUNCTION update_social_conversas_updated_at();

-- ==========================================
-- DONE
-- ==========================================
-- Tabelas criadas:
--   dl_social_conversas (rastreamento de conversas por canal + sender)
--   dl_social_mensagens (log de todas as mensagens com deduplicação)
--   dl_social_leads (leads qualificados pela IA)
-- RLS ativo com service_full_access
-- Trigger updated_at em dl_social_conversas
