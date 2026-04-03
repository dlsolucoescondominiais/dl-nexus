-- ============================================================================
-- DL NEXUS - MIGRATION V4 (MÁQUINA DE ATRAÇÃO - MARKETING B2B)
-- Data: 25 de março de 2026
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TIPOS ENUMERADOS (MARKETING)
-- ----------------------------------------------------------------------------
DO $$ BEGIN
    CREATE TYPE tipo_conteudo AS ENUM ('educativo', 'comercial', 'case_study');
    CREATE TYPE problema_foco AS ENUM ('eletrica', 'solar', 'seguranca');
    CREATE TYPE status_conteudo AS ENUM ('pendente_ia', 'pendente_aprovacao', 'aprovado', 'rejeitado', 'agendado', 'publicado', 'erro');
    CREATE TYPE canal_rede_social AS ENUM ('instagram', 'facebook', 'linkedin', 'tiktok');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ----------------------------------------------------------------------------
-- TABELAS DE CONTEÚDO (O FUNIL SEMI-AUTOMÁTICO)
-- ----------------------------------------------------------------------------

-- 12. CONTEÚDO (Centraliza Criação, Aprovação e Agendamento)
CREATE TABLE IF NOT EXISTS conteudos_marketing (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tipo tipo_conteudo NOT NULL,
    problema problema_foco NOT NULL,
    copy_gerada TEXT NOT NULL,
    imagem_url TEXT, -- Link para a arte gerada pela IA ou do Drive
    canais_destino canal_rede_social[], -- Array de canais para postar
    status status_conteudo DEFAULT 'pendente_aprovacao',
    data_agendamento TIMESTAMPTZ, -- Quando o n8n deve disparar a API da Meta
    data_publicacao TIMESTAMPTZ, -- Quando realmente foi ao ar
    erro_meta_api TEXT, -- Guarda o log de falha se houver
    criado_em TIMESTAMPTZ DEFAULT now(),
    atualizado_em TIMESTAMPTZ DEFAULT now()
);

-- 13. PERFORMANCE DOS POSTS (O Retorno Sobre o Investimento - ROI)
CREATE TABLE IF NOT EXISTS performance_posts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conteudo_id UUID REFERENCES conteudos_marketing(id) ON DELETE CASCADE,
    canal canal_rede_social NOT NULL,
    post_id_externo VARCHAR(255) NOT NULL, -- ID do post lá na Meta/Facebook
    likes INTEGER DEFAULT 0,
    comentarios INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    cliques INTEGER DEFAULT 0,
    conversoes_leads INTEGER DEFAULT 0, -- Quantos leads esse post gerou no WhatsApp?
    data_coleta TIMESTAMPTZ DEFAULT now()
);

-- ----------------------------------------------------------------------------
-- ÍNDICES DE PERFORMANCE ESTRATÉGICA (MARKETING)
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_conteudos_status ON conteudos_marketing(status);
CREATE INDEX IF NOT EXISTS idx_conteudos_agendamento ON conteudos_marketing(data_agendamento);
CREATE INDEX IF NOT EXISTS idx_performance_conteudo_id ON performance_posts(conteudo_id);

-- ----------------------------------------------------------------------------
-- TRIGGERS DE AUTOMAÇÃO
-- ----------------------------------------------------------------------------
-- Aproveita a função V3 de timestamp
DO $$
DECLARE
    t TEXT;
BEGIN
    FOR t IN SELECT table_name FROM information_schema.columns WHERE column_name = 'atualizado_em' AND table_name = 'conteudos_marketing'
    LOOP
        EXECUTE format('DROP TRIGGER IF EXISTS set_timestamp ON %I', t);
        EXECUTE format('CREATE TRIGGER set_timestamp BEFORE UPDATE ON %I FOR EACH ROW EXECUTE FUNCTION trigger_set_timestamp()', t);
    END LOOP;
END $$;
