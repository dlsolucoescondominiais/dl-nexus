-- ==============================================================================
-- DL NEXUS V3 - MOTOR DE ORÇAMENTOS VIVO
-- SCRIPT DE SETUP SUPABASE
-- Data: 2026-05-31
-- Objetivo: Criar tabelas de catálogos dinâmicos e aprendizado contínuo das IAs
-- ==============================================================================

-- 1. Tabela: portfolio_servicos
CREATE TABLE IF NOT EXISTS public.portfolio_servicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_linha VARCHAR(100) NOT NULL,
    nome_comercial VARCHAR(200) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 2. Tabela: submodulos_servicos
CREATE TABLE IF NOT EXISTS public.submodulos_servicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    portfolio_id UUID REFERENCES public.portfolio_servicos(id) ON DELETE CASCADE,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 3. Tabela: campos_tecnicos
CREATE TABLE IF NOT EXISTS public.campos_tecnicos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id) ON DELETE CASCADE,
    nome_campo VARCHAR(150) NOT NULL,
    tipo_campo VARCHAR(50) NOT NULL, -- text, number, select, boolean
    obrigatorio BOOLEAN DEFAULT TRUE,
    ajuda TEXT,
    unidade VARCHAR(30)
);

-- 4. Tabela: regras_validacao
CREATE TABLE IF NOT EXISTS public.regras_validacao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id) ON DELETE CASCADE,
    regra TEXT NOT NULL,
    severidade VARCHAR(50) NOT NULL, -- ALTA, MEDIA, BAIXA
    mensagem_cliente TEXT,
    mensagem_interna TEXT
);

-- 5. Tabela: materiais_padrao
CREATE TABLE IF NOT EXISTS public.materiais_padrao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id) ON DELETE CASCADE,
    nome_material VARCHAR(200) NOT NULL,
    unidade VARCHAR(30),
    quantidade_base NUMERIC,
    preco_maximo NUMERIC(10,2),
    marca_preferida VARCHAR(100),
    aparece_cliente BOOLEAN DEFAULT FALSE,
    aparece_interno BOOLEAN DEFAULT TRUE
);

-- 6. Tabela: mao_obra_padrao
CREATE TABLE IF NOT EXISTS public.mao_obra_padrao (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id) ON DELETE CASCADE,
    nome_servico VARCHAR(200) NOT NULL,
    valor_base NUMERIC(10,2),
    unidade VARCHAR(50),
    criterio_calculo TEXT
);

-- 7. Tabela: precos_maximos_compra
CREATE TABLE IF NOT EXISTS public.precos_maximos_compra (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome_item VARCHAR(255) NOT NULL,
    valor NUMERIC(10,2) NOT NULL,
    fornecedor_referencia VARCHAR(200),
    data_atualizacao TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- 8. Tabela: contratos_partner
CREATE TABLE IF NOT EXISTS public.contratos_partner (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    modalidade VARCHAR(100) NOT NULL, -- Basic, Master, Prime
    valor_mensal_base NUMERIC(10,2),
    sla_horas INTEGER,
    descricao TEXT
);

-- 9. Tabela: propostas_modelo
CREATE TABLE IF NOT EXISTS public.propostas_modelo (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id) ON DELETE CASCADE,
    nome_modelo VARCHAR(200),
    template_markdown TEXT,
    ativo BOOLEAN DEFAULT TRUE
);

-- 10. Tabela: orcamentos_reais (Aprendizado)
CREATE TABLE IF NOT EXISTS public.orcamentos_reais (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente VARCHAR(255) NOT NULL,
    endereco TEXT,
    portfolio_id UUID REFERENCES public.portfolio_servicos(id),
    submodulo_id UUID REFERENCES public.submodulos_servicos(id),
    payload_json JSONB,
    proposta_cliente TEXT,
    proposta_interna TEXT,
    valor_total NUMERIC(15,2),
    status VARCHAR(50) DEFAULT 'ENVIADO',
    aprovado BOOLEAN DEFAULT FALSE,
    data TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- ==============================================================================
-- INSERÇÕES DE MOCK (FASE 1: DL Volt e DL Guardião)
-- ==============================================================================

-- Inserindo Linhas de Portfólio
INSERT INTO public.portfolio_servicos (nome_linha, nome_comercial, descricao)
VALUES 
    ('DL Volt', 'DL Volt — Elétrica e Automação', 'Retrofit elétrico, quadros e infraestrutura'),
    ('DL Guardião', 'DL Guardião — CFTV e Segurança Eletrônica', 'Câmeras, NVR e infra de segurança');

-- (Demais catálogos e submódulos devem ser alimentados via painel do Supabase)
