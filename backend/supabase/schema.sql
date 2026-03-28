-- =============================================
-- DL NEXUS - ESQUEMA DE BANCO DE DADOS (SUPABASE)
-- Rodar este script no Editor SQL para blindar o sistema
-- =============================================

-- 1. TABELA DE LEADS (Se já existir, ignore erro)
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_contato TEXT,
    nome_condominio TEXT,
    telefone TEXT UNIQUE,
    email TEXT,
    tipo_imovel TEXT,
    num_unidades INTEGER,
    mensagem TEXT,
    tipo_servico TEXT, -- ELETRICO, SOLAR, SEGURANCA, INCENDIO...
    porte TEXT, -- PEQUENO, MEDIO, GRANDE, COMPLEXO
    valor_estimado NUMERIC(15,2),
    status TEXT DEFAULT 'novo', -- novo, triado, agendado, avaliado, proposta, fechado
    prioridade TEXT DEFAULT 'baixa',
    origem TEXT, -- whatsapp, site, email
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 2. TABELA DE MENSAGENS (Histórico do Bot)
CREATE TABLE IF NOT EXISTS mensagens_whatsapp (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    telefone TEXT,
    nome_contato TEXT,
    mensagem TEXT,
    tipo TEXT,
    direcao TEXT DEFAULT 'entrada', -- entrada, saida
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. TABELA DE AVALIAÇÕES TÉCNICAS
CREATE TABLE IF NOT EXISTS avaliacoes_tecnicas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id),
    checklist JSONB,
    tecnico_responsavel TEXT,
    data_avaliacao DATE,
    resultado TEXT,
    proposta_gerada BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 4. TABELA DE TAREFAS (Background Tasks)
CREATE TABLE IF NOT EXISTS tarefas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo TEXT,
    descricao TEXT,
    status TEXT DEFAULT 'pendente',
    prioridade INTEGER DEFAULT 1,
    executar_em TIMESTAMPTZ,
    resultado TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 5. TABELA DE AUDITORIA (Logs de Fluxo n8n)
CREATE TABLE IF NOT EXISTS auditoria (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entidade TEXT, -- Lead, OS, WhatsApp
    entidade_id TEXT,
    acao TEXT,
    contexto JSONB,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Habilitar Realtime
alter publication supabase_realtime add table leads;
alter publication supabase_realtime add table mensagens_whatsapp;
