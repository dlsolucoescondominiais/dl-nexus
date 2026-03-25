-- =============================================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
-- DL SOLUÇÕES CONDOMINIAIS - SCHEMA SUPABASE
-- Combinação: Jules (base) + Antigravity (expansão)
-- Data: 2026-03-22
-- =============================================

-- ===================
-- TABELA 1: LEADS (Jules + Antigravity)
-- Recebe dados do site via n8n webhook
-- ===================
CREATE TABLE IF NOT EXISTS leads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    
    -- Dados do contato (Jules)
    nome_contato VARCHAR(255) NOT NULL,
    nome_condominio VARCHAR(255),
    telefone VARCHAR(20),
    email VARCHAR(255),
    email_encaminhamento TEXT,
    tipo_imovel VARCHAR(50),           -- Condomínio, Colégio, Escola, etc.
    num_unidades INT,
    mensagem TEXT,
    
    -- Classificação ANINHA (Antigravity)
    tipo_servico TEXT,                  -- Solar, CFTV, Elétrica, Redes, etc.
    status VARCHAR(50) DEFAULT 'novo', -- novo → triado → em_contato → proposta → fechado → perdido
    porte VARCHAR(20),                 -- pequeno (<30), medio (30-100), grande (>100)
    prioridade VARCHAR(20) DEFAULT 'normal', -- normal, media, alta
    
    -- Rastreamento (Antigravity)
    origem VARCHAR(50) DEFAULT 'site', -- site, whatsapp, indicacao, google
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices para performance
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created ON leads(created_at DESC);
CREATE INDEX idx_leads_prioridade ON leads(prioridade);

-- ===================
-- TABELA 2: MENSAGENS WHATSAPP (Antigravity)
-- Recebe mensagens do WhatsApp Business API
-- ===================
CREATE TABLE IF NOT EXISTS mensagens_whatsapp (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    
    -- Dados da mensagem
    telefone VARCHAR(20) NOT NULL,
    nome_contato VARCHAR(255),
    mensagem TEXT,
    tipo VARCHAR(50),                   -- text, image, video, audio, document
    direcao VARCHAR(10) DEFAULT 'entrada', -- entrada, saida
    
    -- Vínculo com lead (se existir)
    lead_id UUID REFERENCES leads(id),
    
    -- Metadata
    lida BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índice para buscar conversas por telefone
CREATE INDEX idx_whatsapp_telefone ON mensagens_whatsapp(telefone);
CREATE INDEX idx_whatsapp_lida ON mensagens_whatsapp(lida) WHERE lida = false;

-- ===================
-- TABELA 3: AVALIACOES TÉCNICAS (Futuro - Fase 2)
-- Agendamentos de Avaliação Técnica
-- ===================
CREATE TABLE IF NOT EXISTS avaliacoes_tecnicas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    lead_id UUID REFERENCES leads(id) NOT NULL,
    
    -- Agendamento
    data_agendada TIMESTAMP WITH TIME ZONE,
    data_realizada TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'agendada', -- agendada → realizada → cancelada
    
    -- Resultado
    observacoes TEXT,
    fotos_url TEXT[],                    -- Array de URLs das fotos
    tipo_servico_confirmado TEXT,
    valor_estimado DECIMAL(12,2),
    
    -- Responsável
    tecnico_responsavel VARCHAR(255),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===================
-- TABELA 4: PROPOSTAS (Futuro - Fase 2)
-- Propostas comerciais geradas
-- ===================
CREATE TABLE IF NOT EXISTS propostas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    lead_id UUID REFERENCES leads(id) NOT NULL,
    avaliacao_id UUID REFERENCES avaliacoes_tecnicas(id),
    
    -- Proposta
    numero_proposta VARCHAR(20) UNIQUE,
    titulo TEXT,
    valor_total DECIMAL(12,2),
    prazo_execucao VARCHAR(100),
    validade_proposta DATE,
    
    -- Status
    status VARCHAR(50) DEFAULT 'rascunho', -- rascunho → enviada → aceita → recusada
    pdf_url TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===================
-- Row Level Security (RLS)
-- ===================
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE mensagens_whatsapp ENABLE ROW LEVEL SECURITY;
ALTER TABLE avaliacoes_tecnicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE propostas ENABLE ROW LEVEL SECURITY;

-- Políticas para service_role (n8n + API)
CREATE POLICY "service_full_access_leads" ON leads FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_whatsapp" ON mensagens_whatsapp FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_avaliacoes" ON avaliacoes_tecnicas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_propostas" ON propostas FOR ALL USING (true) WITH CHECK (true);

-- ===================
-- Trigger para updated_at automático
-- ===================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER leads_updated_at
    BEFORE UPDATE ON leads
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER avaliacoes_updated_at
    BEFORE UPDATE ON avaliacoes_tecnicas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER propostas_updated_at
    BEFORE UPDATE ON propostas
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();
