-- Migration V7: Social Publications Log Table (Revisada V1)
CREATE TABLE IF NOT EXISTS dl_social_publicacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    semana_ref VARCHAR(50),
    data_planejada DATE,
    origem_conteudo VARCHAR(100),
    fonte_tipo VARCHAR(100),
    fonte_nome VARCHAR(255),
    fonte_url TEXT,
    fonte_data_publicacao DATE,
    fonte_data_consulta TIMESTAMP WITH TIME ZONE,
    produto_dl VARCHAR(100),
    publico_alvo VARCHAR(255),
    tema VARCHAR(255),
    resumo_fonte TEXT,
    comentario_tecnico_dl TEXT,
    texto_base TEXT,
    legenda_instagram TEXT,
    legenda_facebook TEXT,
    texto_google_business TEXT,
    roteiro_tiktok TEXT,
    texto_linkedin TEXT,
    hashtags JSONB DEFAULT '[]'::jsonb,
    image_url TEXT,
    video_url TEXT,
    status_revisao VARCHAR(50) DEFAULT 'rascunho_planejado',
    status_global VARCHAR(50) DEFAULT 'rascunho_planejado',
    bloqueios JSONB DEFAULT '[]'::jsonb,
    status_instagram VARCHAR(50) DEFAULT 'pendente',
    status_facebook VARCHAR(50) DEFAULT 'pendente',
    status_google_business VARCHAR(50) DEFAULT 'pendente',
    status_tiktok VARCHAR(50) DEFAULT 'pendente',
    status_linkedin VARCHAR(50) DEFAULT 'pendente',
    url_instagram TEXT,
    url_facebook TEXT,
    url_google_business TEXT,
    url_tiktok TEXT,
    url_linkedin TEXT,
    erros JSONB DEFAULT '{}'::jsonb,
    tentativas JSONB DEFAULT '{}'::jsonb,
    publicado_em JSONB DEFAULT '{}'::jsonb,
    relatorio_enviado BOOLEAN DEFAULT FALSE
);

-- Enable RLS
ALTER TABLE dl_social_publicacoes ENABLE ROW LEVEL SECURITY;

-- Create policy for authenticated users (n8n API / backend)
CREATE POLICY "Allow all operations for authenticated users" 
ON dl_social_publicacoes 
FOR ALL 
TO authenticated 
USING (true) 
WITH CHECK (true);

-- Allow public read access
CREATE POLICY "Allow public read access" 
ON dl_social_publicacoes 
FOR SELECT 
TO public 
USING (true);
