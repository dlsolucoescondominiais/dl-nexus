-- =============================================
-- DL SOLUÇÕES CONDOMINIAIS — ECOVOLT MIGRATION
-- Módulo: 200_MOTOR_SOLAR_BACKUP_DL_ECOVOLT
-- Data: 2026-06-24
-- Status: Homologação Local (Idempotente)
-- =============================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==========================================
-- TABELA: dl_solar_orcamentos
-- Cadastro mestre de orçamentos e dimensionamentos
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_solar_orcamentos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    protocolo VARCHAR(100) UNIQUE NOT NULL,
    cliente VARCHAR(255) NOT NULL,
    tipo_cliente VARCHAR(100) NOT NULL, -- condominio, residencia, empresa, escola, laboratorio, restaurante, comercio
    status VARCHAR(50) DEFAULT 'recebido', -- recebido, dados_insuficientes, calculado_preliminar, bloqueado_killcritic, aprovado_para_proposta, proposta_gerada, pdf_gerado, enviado_cliente, em_negociacao, fechado, perdido, aprendizado_pendente, aprendizado_aplicado
    objetivo VARCHAR(100), -- economia, backup, híbrido, off-grid parcial, contingência
    
    -- Dados elétricos e conta
    consumo_mensal_kwh NUMERIC,
    valor_conta NUMERIC,
    tensao VARCHAR(50), -- 127, 220, 380, 127/220, 220/380
    tipo_ligacao VARCHAR(50), -- mono, bi, trifasico
    disjuntor_geral VARCHAR(100),
    padrao_entrada VARCHAR(255),
    aterramento BOOLEAN DEFAULT FALSE,
    dr_dps BOOLEAN DEFAULT FALSE,
    quadro_cargas_criticas BOOLEAN DEFAULT FALSE,
    distancia_inversor_quadro NUMERIC,
    distancia_baterias_quadro NUMERIC,
    
    -- Dados solares e infraestrutura
    area_disponivel NUMERIC,
    tipo_telhado_laje VARCHAR(100),
    sombreamento VARCHAR(100),
    orientacao VARCHAR(100),
    inclinacao VARCHAR(100),
    local_inversor VARCHAR(255),
    local_baterias VARCHAR(255),
    ventilacao BOOLEAN DEFAULT FALSE,
    
    -- Cálculos de dimensionamento de Backup
    autonomia_horas NUMERIC,
    energia_critica_kwh NUMERIC, -- kWh necessários acumulados por dia
    bateria_util_kwh NUMERIC,    -- kWh úteis dimensionados
    bateria_nominal_kwh NUMERIC, -- kWh nominais considerando DoD e eficiência
    bateria_capacidade_descarga_kw NUMERIC, -- Potência de descarga contínua necessária
    potencia_critica_kw NUMERIC, -- Soma de todas as cargas críticas
    potencia_critica_simultanea_kw NUMERIC, -- Soma das simultâneas
    potencia_inversor_minima_kw NUMERIC,
    inversor_sugerido VARCHAR(255),
    sistema_solar_kwp NUMERIC,  -- Potência solar preliminar
    
    -- Financeiro e riscos
    valor_estimado NUMERIC,
    custos_estimados NUMERIC,
    margem NUMERIC,
    risco_killcritic VARCHAR(50) DEFAULT 'baixo', -- baixo, medio, alto
    
    criado_em TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solar_orc_protocolo ON dl_solar_orcamentos(protocolo);
CREATE INDEX IF NOT EXISTS idx_solar_orc_status ON dl_solar_orcamentos(status);
CREATE INDEX IF NOT EXISTS idx_solar_orc_tipo ON dl_solar_orcamentos(tipo_cliente);
CREATE INDEX IF NOT EXISTS idx_solar_orc_created ON dl_solar_orcamentos(criado_em DESC);

-- ==========================================
-- TABELA: dl_solar_cargas_criticas
-- Detalhamento de cargas para dimensionamento de backup
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_solar_cargas_criticas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id) ON DELETE CASCADE,
    nome_carga VARCHAR(255) NOT NULL,
    potencia_w NUMERIC NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 1,
    horas_uso NUMERIC NOT NULL DEFAULT 1,
    simultanea BOOLEAN DEFAULT TRUE,
    motor BOOLEAN DEFAULT FALSE,
    pico_partida VARCHAR(255), -- tipo de partida (direta, soft, inversor), corrente/potência partida
    prioridade INTEGER DEFAULT 1,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solar_cargas_orc ON dl_solar_cargas_criticas(orcamento_id);

-- ==========================================
-- TABELA: dl_solar_equipamentos
-- Catálogo de referência SolaX e Triple Power (Corsolar)
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_solar_equipamentos (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    fornecedor VARCHAR(255) DEFAULT 'Corsolar',
    marca VARCHAR(255) DEFAULT 'SolaXPower',
    modelo VARCHAR(255) NOT NULL,
    tipo VARCHAR(100) NOT NULL, -- inversor_hibrido, bateria_litio, modulo_solar, acessorio
    potencia NUMERIC, -- kW para inversores
    capacidade_kwh NUMERIC, -- kWh para baterias
    custo NUMERIC DEFAULT NULL, -- Preço real pendente de validação
    preco_maximo_compra NUMERIC DEFAULT NULL,
    compatibilidade TEXT,
    status VARCHAR(50) DEFAULT 'pendente_validacao', -- pendente_validacao, ativo
    fonte_preco VARCHAR(255) DEFAULT 'estimado_validar',
    ativo BOOLEAN DEFAULT TRUE,
    atualizado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solar_equip_tipo ON dl_solar_equipamentos(tipo);
CREATE INDEX IF NOT EXISTS idx_solar_equip_modelo ON dl_solar_equipamentos(modelo);

-- ==========================================
-- TABELA: dl_solar_orcamento_versoes
-- Histórico evolutivo de versões do orçamento (V1 a V6)
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_solar_orcamento_versoes (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id) ON DELETE CASCADE,
    versao VARCHAR(50) NOT NULL, -- V1_gerada, V2_corrigida_killcritic, V3_ajustada_humano, V4_enviada_cliente, V5_pos_negociacao, V6_fechada_perdida
    markdown_cliente TEXT,
    markdown_interno TEXT,
    json_calculo JSONB DEFAULT '{}'::jsonb,
    motivo_regeneracao TEXT,
    aprovado_killcritic BOOLEAN DEFAULT FALSE,
    status_killcritic VARCHAR(50) DEFAULT 'BLOQUEADO', -- APROVADO, APROVADO_COM_RESSALVAS, BLOQUEADO
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solar_vers_orc ON dl_solar_orcamento_versoes(orcamento_id);
CREATE INDEX IF NOT EXISTS idx_solar_vers_tag ON dl_solar_orcamento_versoes(versao);

-- ==========================================
-- TABELA: dl_solar_aprendizado
-- Log de aprendizado evolutivo para regeneração
-- ==========================================
CREATE TABLE IF NOT EXISTS dl_solar_aprendizado (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    orcamento_id UUID REFERENCES dl_solar_orcamentos(id) ON DELETE CASCADE,
    erro_detectado TEXT,
    ajuste_feito TEXT,
    impacto TEXT,
    recomendacao_futura TEXT,
    aplicar_regra BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_solar_apr_orc ON dl_solar_aprendizado(orcamento_id);

-- ==========================================
-- Row Level Security (RLS)
-- ==========================================
ALTER TABLE dl_solar_orcamentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_solar_cargas_criticas ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_solar_equipamentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_solar_orcamento_versoes ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_solar_aprendizado ENABLE ROW LEVEL SECURITY;

-- Políticas de acesso livre para Service Role do n8n (Idempotentes)
DROP POLICY IF EXISTS "service_full_access_solar_orcamentos" ON dl_solar_orcamentos;
CREATE POLICY "service_full_access_solar_orcamentos" ON dl_solar_orcamentos FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_full_access_solar_cargas" ON dl_solar_cargas_criticas;
CREATE POLICY "service_full_access_solar_cargas" ON dl_solar_cargas_criticas FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_full_access_solar_equipamentos" ON dl_solar_equipamentos;
CREATE POLICY "service_full_access_solar_equipamentos" ON dl_solar_equipamentos FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_full_access_solar_versoes" ON dl_solar_orcamento_versoes;
CREATE POLICY "service_full_access_solar_versoes" ON dl_solar_orcamento_versoes FOR ALL USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "service_full_access_solar_aprendizado" ON dl_solar_aprendizado;
CREATE POLICY "service_full_access_solar_aprendizado" ON dl_solar_aprendizado FOR ALL USING (true) WITH CHECK (true);

-- ==========================================
-- Trigger para updated_at automático em dl_solar_orcamentos
-- ==========================================
CREATE OR REPLACE FUNCTION update_solar_orcamentos_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_solar_orcamentos_updated_at ON dl_solar_orcamentos;
CREATE TRIGGER trg_solar_orcamentos_updated_at
    BEFORE UPDATE ON dl_solar_orcamentos
    FOR EACH ROW EXECUTE FUNCTION update_solar_orcamentos_updated_at();

-- ==========================================
-- PRÉ-CARREGAMENTO DE EQUIPAMENTOS SolaX/Corsolar (Referência inicial pendente validação)
-- ==========================================
INSERT INTO dl_solar_equipamentos (modelo, tipo, potencia, capacidade_kwh, compatibilidade, status, fonte_preco)
VALUES
    ('SolaX X3-Hybrid 10.0-D', 'inversor_hibrido', 10.0, NULL, 'Baterias Triple Power LFP', 'pendente_validacao', 'estimado_validar'),
    ('SolaX X3-Hybrid 15.0-D', 'inversor_hibrido', 15.0, NULL, 'Baterias Triple Power LFP', 'pendente_validacao', 'estimado_validar'),
    ('SolaX X1-Hybrid 5.0-D', 'inversor_hibrido', 5.0, NULL, 'Baterias Triple Power LFP', 'pendente_validacao', 'estimado_validar'),
    ('Triple Power T-BAT H 5.8 (LFP)', 'bateria_litio', NULL, 5.8, 'SolaX X1/X3 Hybrid', 'pendente_validacao', 'estimado_validar'),
    ('Triple Power T-BAT H 11.5 (LFP)', 'bateria_litio', NULL, 11.5, 'SolaX X3 Hybrid', 'pendente_validacao', 'estimado_validar')
ON CONFLICT DO NOTHING;
