-- ============================================================================
-- DL NEXUS - MIGRATION V6 (ENTERPRISE OPEX & DL COMMANDER)
-- Data: 25 de março de 2026
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- NOVOS TIPOS ENUMERADOS (PIPELINE E TRIAGEM GRANULAR)
-- ----------------------------------------------------------------------------
DO $$ BEGIN
    CREATE TYPE tipo_cliente_dl AS ENUM ('condominio', 'escola', 'lead_frio', 'lead_quente', 'manutencao_recorrente', 'contrato_mensal', 'perdido', 'concorrencia', 'sem_perfil');
    CREATE TYPE servico_tecnico_dl AS ENUM ('emergencia_eletrica', 'incendio_alarme', 'energia_solar', 'infra_rede', 'seguranca_eletronica', 'controle_acesso', 'portaria_remota', 'carregador_veicular');
    CREATE TYPE pipeline_stage_dl AS ENUM ('novo_lead', 'triagem_ia', 'avaliacao_agendada', 'proposta_enviada', 'negociacao', 'fechado_ganho', 'fechado_perdido', 'pos_venda', 'contrato_recorrente', 'renovacao');
    CREATE TYPE modelo_ia AS ENUM ('gemini_flash', 'claude_35_sonnet', 'gpt_4o', 'gpt_4o_mini', 'fallback_padrao');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- ----------------------------------------------------------------------------
-- 1. ATUALIZAÇÃO DA TABELA DE LEADS (MÁQUINA DE PIPELINE COMERCIAL)
-- ----------------------------------------------------------------------------
-- Como a tabela 'leads' já existe desde a V3, vamos usar ALTER TABLE
-- para garantir a evolução do banco sem dropar dados.

ALTER TABLE leads ADD COLUMN IF NOT EXISTS empresa_condominio VARCHAR(255);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS tipo_cliente tipo_cliente_dl;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS regiao VARCHAR(100); -- (Sul, Sudoeste, Oeste, Norte)
ALTER TABLE leads ADD COLUMN IF NOT EXISTS servico_desejado servico_tecnico_dl;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS urgencia VARCHAR(50);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS resumo_conversa TEXT;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS ia_responsavel modelo_ia;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS score_comercial INTEGER CHECK (score_comercial >= 0 AND score_comercial <= 100);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS score_tecnico INTEGER CHECK (score_tecnico >= 0 AND score_tecnico <= 100);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS pipeline_stage pipeline_stage_dl DEFAULT 'novo_lead';
ALTER TABLE leads ADD COLUMN IF NOT EXISTS ultima_interacao TIMESTAMPTZ DEFAULT now();
ALTER TABLE leads ADD COLUMN IF NOT EXISTS proximo_followup TIMESTAMPTZ;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS responsavel_interno VARCHAR(100);

-- Criação de Índices para o Dashboard DL Commander
CREATE INDEX IF NOT EXISTS idx_leads_pipeline_stage ON leads(pipeline_stage);
CREATE INDEX IF NOT EXISTS idx_leads_regiao ON leads(regiao);
CREATE INDEX IF NOT EXISTS idx_leads_ultima_interacao ON leads(ultima_interacao DESC);

-- ----------------------------------------------------------------------------
-- 2. METADADOS DE TELEMETRIA NA TABELA DE MENSAGENS (CONTROLE DE CUSTOS IA)
-- ----------------------------------------------------------------------------
ALTER TABLE mensagens_whatsapp ADD COLUMN IF NOT EXISTS ia_utilizada modelo_ia;
ALTER TABLE mensagens_whatsapp ADD COLUMN IF NOT EXISTS tempo_resposta_ms INTEGER;
ALTER TABLE mensagens_whatsapp ADD COLUMN IF NOT EXISTS custo_estimado_usd NUMERIC(10,5);
ALTER TABLE mensagens_whatsapp ADD COLUMN IF NOT EXISTS score_confianca_ia NUMERIC(5,2);
ALTER TABLE mensagens_whatsapp ADD COLUMN IF NOT EXISTS motivo_roteamento TEXT;

-- ----------------------------------------------------------------------------
-- 3. GATILHO PARA ATUALIZAR 'ultima_interacao' DO LEAD AO RECEBER MENSAGEM
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION trigger_update_lead_interaction()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE leads
    SET ultima_interacao = NEW.criado_em
    WHERE telefone = NEW.telefone;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_lead_interaction ON mensagens_whatsapp;
CREATE TRIGGER update_lead_interaction
AFTER INSERT ON mensagens_whatsapp
FOR EACH ROW
EXECUTE FUNCTION trigger_update_lead_interaction();

-- ----------------------------------------------------------------------------
-- 4. TABELA DE FILA DE ERROS (DL FALLBACK SYSTEM)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dl_erros_criticos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    modulo VARCHAR(100) NOT NULL, -- 'webhook_n8n', 'supabase_api', 'meta_whatsapp'
    payload_original JSONB,
    mensagem_erro TEXT,
    resolvido BOOLEAN DEFAULT FALSE,
    criado_em TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_dl_erros_resolvido ON dl_erros_criticos(resolvido);

-- ----------------------------------------------------------------------------
-- CORREÇÃO DE AUDITORIA: Adicionando colunas pendentes
-- ----------------------------------------------------------------------------
ALTER TABLE leads ADD COLUMN IF NOT EXISTS valor_estimado NUMERIC(15,2);
