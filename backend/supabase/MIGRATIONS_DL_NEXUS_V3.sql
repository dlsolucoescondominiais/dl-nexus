-- ============================================================================
-- DL NEXUS - COMANDOS EXECUTIVOS PARA JULES - V3 (PRODUÇÃO)
-- Data: 25 de março de 2026
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ----------------------------------------------------------------------------
-- TIPOS ENUMERADOS (DOMÍNIOS DE DADOS)
-- ----------------------------------------------------------------------------
DO $$ BEGIN
    CREATE TYPE tipo_usuario AS ENUM ('sindico', 'admin', 'agente');
    CREATE TYPE origem_lead AS ENUM ('whatsapp', 'telegram', 'email', 'site');
    CREATE TYPE status_lead AS ENUM ('novo', 'triagem', 'roteado', 'proposta_gerada', 'aceito', 'rejeitado');
    CREATE TYPE viabilidade_avaliacao AS ENUM ('alta', 'media', 'baixa');
    CREATE TYPE status_proposta AS ENUM ('rascunho', 'enviada', 'visualizada', 'aceita', 'rejeitada');
    CREATE TYPE tipo_notificacao AS ENUM ('novo_lead', 'proposta_gerada', 'proposta_aceita', 'proposta_rejeitada', 'erro_sistema');
    CREATE TYPE status_integracao AS ENUM ('enviada', 'entregue', 'lida', 'erro', 'recebido', 'respondido', 'agendado', 'publicado');
    CREATE TYPE tipo_rede_social AS ENUM ('instagram', 'facebook');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ----------------------------------------------------------------------------
-- TABELAS NÚCLEO
-- ----------------------------------------------------------------------------

-- 2. CONDOMINIOS
CREATE TABLE IF NOT EXISTS condominios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(255) NOT NULL,
    endereco VARCHAR(500),
    telefone VARCHAR(20),
    email VARCHAR(255),
    cnpj VARCHAR(20) UNIQUE,
    ativo BOOLEAN DEFAULT TRUE,
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 1. USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    nome VARCHAR(255) NOT NULL,
    tipo tipo_usuario NOT NULL,
    condominio_id UUID REFERENCES condominios(id) ON DELETE SET NULL,
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 3. LEADS (A Porta de Entrada)
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    condominio_id UUID REFERENCES condominios(id) ON DELETE SET NULL,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    telefone VARCHAR(20),
    origem origem_lead,
    mensagem TEXT,
    status status_lead DEFAULT 'novo',
    email_encaminhamento VARCHAR(255),
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 4. AVALIAÇÕES TÉCNICAS (O Trabalho dos Especialistas)
CREATE TABLE IF NOT EXISTS avaliacoes_tecnicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    agente VARCHAR(100) NOT NULL, -- Elétrica, Solar, Segurança, etc.
    score INTEGER CHECK (score >= 0 AND score <= 100),
    recomendacoes TEXT,
    viabilidade viabilidade_avaliacao,
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 5. PROPOSTAS (A Oferta de Valor)
CREATE TABLE IF NOT EXISTS propostas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    condominio_id UUID REFERENCES condominios(id) ON DELETE CASCADE,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    valor_total DECIMAL(15,2),
    servicos JSONB,
    status status_proposta DEFAULT 'rascunho',
    data_envio TIMESTAMPTZ,
    data_resposta TIMESTAMPTZ,
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 6. NOTIFICAÇÕES (O Cérebro Avisando)
CREATE TABLE IF NOT EXISTS notificacoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE CASCADE,
    tipo tipo_notificacao NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    mensagem TEXT NOT NULL,
    lida BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- TABELAS DE INTEGRAÇÃO (OMNICHANNEL)
-- ----------------------------------------------------------------------------

-- 7. WHATSAPP (A Voz Direta)
CREATE TABLE IF NOT EXISTS integracao_whatsapp (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    numero_telefone VARCHAR(20) NOT NULL,
    mensagem_enviada TEXT,
    mensagem_recebida TEXT,
    status status_integracao,
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- 8. TELEGRAM (A Alternativa)
CREATE TABLE IF NOT EXISTS integracao_telegram (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    chat_id VARCHAR(50) NOT NULL,
    mensagem_enviada TEXT,
    mensagem_recebida TEXT,
    status status_integracao,
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- 9. E-MAIL (Documentação Oficial Titan HostGator)
CREATE TABLE IF NOT EXISTS integracao_email (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    email_origem VARCHAR(255) NOT NULL,
    assunto VARCHAR(500),
    corpo TEXT,
    status status_integracao,
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- 10. REDES SOCIAIS (A Presença Digital DL)
CREATE TABLE IF NOT EXISTS integracao_redes_sociais (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo tipo_rede_social NOT NULL,
    post_id VARCHAR(255),
    conteudo TEXT NOT NULL,
    data_agendamento TIMESTAMPTZ,
    status status_integracao DEFAULT 'agendado',
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- 11. AUDITORIA (O Rastreador Incorruptível)
CREATE TABLE IF NOT EXISTS auditoria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    usuario_id UUID REFERENCES usuarios(id) ON DELETE SET NULL,
    acao VARCHAR(100) NOT NULL,
    tabela_afetada VARCHAR(100) NOT NULL,
    registro_id UUID NOT NULL,
    valores_anteriores JSONB,
    valores_novos JSONB,
    criado_em TIMESTAMPTZ DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- ÍNDICES DE PERFORMANCE ESTRATÉGICA
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_leads_condominio_id ON leads(condominio_id);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_leads_origem ON leads(origem);

CREATE INDEX IF NOT EXISTS idx_avaliacoes_tecnicas_lead_id ON avaliacoes_tecnicas(lead_id);

CREATE INDEX IF NOT EXISTS idx_propostas_lead_id ON propostas(lead_id);
CREATE INDEX IF NOT EXISTS idx_propostas_status ON propostas(status);

CREATE INDEX IF NOT EXISTS idx_notificacoes_usuario_id ON notificacoes(usuario_id);
CREATE INDEX IF NOT EXISTS idx_notificacoes_lida ON notificacoes(lida);

-- ----------------------------------------------------------------------------
-- FUNÇÕES E TRIGGERS (AUTOMATIZAÇÕES DO BANCO)
-- ----------------------------------------------------------------------------

-- A. Trigger para atualização automática da coluna atualizado_em
CREATE OR REPLACE FUNCTION trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.atualizado_em = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t TEXT;
BEGIN
    FOR t IN SELECT table_name FROM information_schema.columns WHERE column_name = 'atualizado_em' AND table_schema = 'public'
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS set_timestamp ON %I', t);
        EXECUTE format('CREATE TRIGGER set_timestamp BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp()', t);
    END LOOP;
END $$;


-- B. Trigger para Log de Auditoria
CREATE OR REPLACE FUNCTION trigger_log_auditoria()
RETURNS TRIGGER AS $$
DECLARE
    usuario_id_auth UUID;
BEGIN
    -- Tenta pegar o ID do usuário da sessão atual do Supabase Auth, se existir
    BEGIN
        usuario_id_auth := auth.uid();
    EXCEPTION WHEN OTHERS THEN
        usuario_id_auth := NULL;
    END;

    IF (TG_OP = 'DELETE') THEN
        INSERT INTO auditoria (usuario_id, acao, tabela_afetada, registro_id, valores_anteriores, valores_novos)
        VALUES (usuario_id_auth, 'DELETE', TG_TABLE_NAME, OLD.id, row_to_json(OLD), NULL);
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO auditoria (usuario_id, acao, tabela_afetada, registro_id, valores_anteriores, valores_novos)
        VALUES (usuario_id_auth, 'UPDATE', TG_TABLE_NAME, NEW.id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO auditoria (usuario_id, acao, tabela_afetada, registro_id, valores_anteriores, valores_novos)
        VALUES (usuario_id_auth, 'INSERT', TG_TABLE_NAME, NEW.id, NULL, row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE
    t TEXT;
BEGIN
    -- Ignorar a própria tabela de auditoria e tabelas menores de integração pra não gerar ruído infinito
    FOR t IN SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE' AND table_name NOT IN ('auditoria', 'notificacoes')
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS log_auditoria ON %I', t);
        EXECUTE format('CREATE TRIGGER log_auditoria AFTER INSERT OR UPDATE OR DELETE ON %I FOR EACH ROW EXECUTE FUNCTION trigger_log_auditoria()', t);
    END LOOP;
END $$;
