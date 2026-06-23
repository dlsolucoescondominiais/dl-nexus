
-- Tabela para gerenciar conteudos de marketing
CREATE TABLE IF NOT EXISTS public.conteudos_marketing (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tema TEXT NOT null,
    canal TEXT,
    titulo TEXT,
    legenda TEXT,
    status TEXT DEFAULT 'gerado',
    killcritic_status TEXT,
    killcritic_motivo TEXT,
    post_id TEXT,
    post_url TEXT,
    erro_publicacao TEXT,
    payload JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    published_at TIMESTAMP WITH TIME ZONE
);
