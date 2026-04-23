-- =============================================
-- DL NEXUS - ESQUEMA DE BANCO DE DADOS (SUPABASE)
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- Foco: Escalar OPEX através de ecossistema integrado
-- Rodar este script no Editor SQL para blindar o sistema
-- =============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. TABELA DE LEADS (Se já existir, ignore erro)
-- Armazena os contatos (Síndicos, Gestores) e demandas iniciais
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome_contato TEXT,
    nome_condominio TEXT,
    telefone TEXT UNIQUE,
    email TEXT,
    email_encaminhamento TEXT, -- Usado pelo Agente IA para roteamento departamental (orcamento@, suporte@, etc)
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

-- Índices de Performance para Leads (Buscas Rápidas)
CREATE INDEX IF NOT EXISTS idx_leads_telefone ON leads (telefone);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads (status);
CREATE INDEX IF NOT EXISTS idx_leads_created_at ON leads (created_at DESC);


-- 2. TABELA DE MENSAGENS (Histórico do Bot)
-- Guarda o fluxo de comunicação entre Aninha/Diego e o Lead via WhatsApp
CREATE TABLE IF NOT EXISTS mensagens_whatsapp (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telefone TEXT,
    nome_contato TEXT,
    mensagem TEXT,
    tipo TEXT,
    direcao TEXT DEFAULT 'entrada', -- entrada, saida
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Índices de Performance para Mensagens
CREATE INDEX IF NOT EXISTS idx_mensagens_telefone ON mensagens_whatsapp (telefone);


-- 3. TABELA DE AVALIAÇÕES TÉCNICAS (Nunca 'Visitas Técnicas')
-- Registro das inspeções feitas nos condomínios pelos especialistas
CREATE TABLE IF NOT EXISTS avaliacoes_tecnicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    checklist JSONB,
    tecnico_responsavel TEXT,
    data_avaliacao DATE,
    resultado TEXT,
    proposta_gerada BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Índices de Performance para Avaliações
CREATE INDEX IF NOT EXISTS idx_avaliacoes_lead_id ON avaliacoes_tecnicas (lead_id);
CREATE INDEX IF NOT EXISTS idx_avaliacoes_data ON avaliacoes_tecnicas (data_avaliacao);


-- 4. TABELA DE PROPOSTAS
-- Registro dos contratos gerados após a Avaliação Técnica
CREATE TABLE IF NOT EXISTS propostas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id),
    avaliacao_id UUID REFERENCES avaliacoes_tecnicas(id),
    valor_total NUMERIC(15,2),
    recorrencia_mensal NUMERIC(15,2), -- Contratos OPEX
    descricao_servicos TEXT,
    status TEXT DEFAULT 'enviada', -- enviada, em_negociacao, aprovada, recusada
    url_documento TEXT, -- Link pro Google Drive/PDF gerado pelo Arquivista
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Índices de Performance para Propostas
CREATE INDEX IF NOT EXISTS idx_propostas_lead_id ON propostas (lead_id);
CREATE INDEX IF NOT EXISTS idx_propostas_status ON propostas (status);


-- 5. TABELA DE TAREFAS (Background Tasks)
-- Fila de processamento para operações assíncronas do sistema
CREATE TABLE IF NOT EXISTS tarefas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo TEXT,
    descricao TEXT,
    status TEXT DEFAULT 'pendente',
    prioridade INTEGER DEFAULT 1,
    executar_em TIMESTAMPTZ,
    resultado TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Índices de Performance para Tarefas
CREATE INDEX IF NOT EXISTS idx_tarefas_status ON tarefas (status);


-- 6. TABELA DE AUDITORIA (Logs de Fluxo n8n)
-- Rastreador de falhas e execuções do Cérebro
CREATE TABLE IF NOT EXISTS auditoria (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entidade TEXT, -- Lead, OS, WhatsApp
    entidade_id TEXT,
    acao TEXT,
    contexto JSONB,
    timestamp TIMESTAMPTZ DEFAULT now()
);

-- Índices de Performance para Auditoria
CREATE INDEX IF NOT EXISTS idx_auditoria_entidade ON auditoria (entidade, entidade_id);


-- Habilitar Realtime para Dashboard UI
alter publication supabase_realtime add table leads;
alter publication supabase_realtime add table mensagens_whatsapp;
alter publication supabase_realtime add table propostas;
