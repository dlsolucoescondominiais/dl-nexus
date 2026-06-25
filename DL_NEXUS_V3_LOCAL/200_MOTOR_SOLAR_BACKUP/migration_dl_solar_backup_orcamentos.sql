CREATE TABLE IF NOT EXISTS dl_solar_orcamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_nome TEXT NOT NULL,
    tipo_cliente TEXT NOT NULL,
    endereco TEXT,
    bairro TEXT,
    cidade TEXT,
    responsavel TEXT,
    whatsapp TEXT,
    email TEXT,
    consumo_mensal_kwh NUMERIC,
    status TEXT DEFAULT 'recebido',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_dl_solar_orcamentos_status ON dl_solar_orcamentos(status);

CREATE TABLE IF NOT EXISTS dl_solar_cargas_criticas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id),
    descricao TEXT,
    potencia_w NUMERIC,
    horas_uso NUMERIC,
    quantidade INTEGER,
    prioridade INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dl_solar_equipamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    modelo TEXT NOT NULL,
    tipo TEXT NOT NULL,
    fabricante TEXT DEFAULT 'SolaXPower',
    fornecedor TEXT DEFAULT 'Corsolar',
    potencia_nominal_kw NUMERIC,
    custo_base NUMERIC,
    ativo BOOLEAN DEFAULT true
);

CREATE TABLE IF NOT EXISTS dl_solar_orcamento_versoes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id),
    versao INTEGER NOT NULL,
    dados_completos JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dl_solar_aprendizado (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id),
    analise_agente TEXT,
    sugestao_melhoria TEXT,
    aplicado BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
