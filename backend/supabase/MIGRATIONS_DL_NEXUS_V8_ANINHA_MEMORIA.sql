-- Migration V8: Conversational Memory and Logs for Telegram Bot Aninha (Fase 2)

-- Table 1: conversas_aninha (Conversations State)
CREATE TABLE IF NOT EXISTS conversas_aninha (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canal TEXT NOT NULL,
    chat_id TEXT NOT NULL,
    username TEXT,
    nome_usuario TEXT,
    telefone TEXT,
    intencao_atual TEXT,
    etapa_funil TEXT DEFAULT 'inicio',
    segmento TEXT DEFAULT 'indefinido',
    dados_coletados JSONB DEFAULT '{}'::jsonb,
    ultima_mensagem TEXT,
    ultima_resposta TEXT,
    status TEXT DEFAULT 'em_atendimento',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(canal, chat_id)
);

-- Table 2: eventos_aninha (Logs of Events)
CREATE TABLE IF NOT EXISTS eventos_aninha (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canal TEXT,
    chat_id TEXT,
    message_id TEXT,
    direcao TEXT,
    tipo_evento TEXT,
    conteudo TEXT,
    payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Indices for eventos_aninha
CREATE INDEX IF NOT EXISTS idx_eventos_aninha_canal ON eventos_aninha(canal);
CREATE INDEX IF NOT EXISTS idx_eventos_aninha_chat ON eventos_aninha(chat_id);
CREATE INDEX IF NOT EXISTS idx_eventos_aninha_msg ON eventos_aninha(message_id);
CREATE INDEX IF NOT EXISTS idx_eventos_aninha_date ON eventos_aninha(created_at);

-- Table 3: logs_aninha_erros (System Error Logs)
CREATE TABLE IF NOT EXISTS logs_aninha_erros (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workflow TEXT,
    node_name TEXT,
    canal TEXT,
    chat_id TEXT,
    erro TEXT,
    payload JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS workflow TEXT;
ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS node_name TEXT;
ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS canal TEXT;
ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS chat_id TEXT;
ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS erro TEXT;
ALTER TABLE logs_aninha_erros ADD COLUMN IF NOT EXISTS payload JSONB DEFAULT '{}'::jsonb;

-- Table 4: mensagens_processadas_aninha (Deduplication)
CREATE TABLE IF NOT EXISTS mensagens_processadas_aninha (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    canal TEXT NOT NULL,
    chat_id TEXT NOT NULL,
    message_id TEXT,
    hash_mensagem TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    UNIQUE(canal, chat_id, message_id)
);

-- Indices for mensagens_processadas_aninha
CREATE INDEX IF NOT EXISTS idx_msg_processadas_hash ON mensagens_processadas_aninha(hash_mensagem);
