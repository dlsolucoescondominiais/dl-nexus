-- =============================================
-- DL SOLUÇÕES CONDOMINIAIS — MIGRAÇÃO V8
-- Tabela de Auditoria de Sincronização
-- Data: 2026-04-23
-- Autor: Antigravity Sync Engine
-- =============================================
-- 
-- Esta migração cria a infraestrutura de auditoria
-- para a sincronização entre:
--   - n8n (automação WhatsApp/leads)
--   - Jules (GitHub AI + Inquisidor Técnico n8n)
--   - Antigravity (geração de skills/marketing)
--   - Supabase (banco de dados central)
-- =============================================

-- ===================
-- TABELA: dl_sync_log
-- Log de todas as operações de sincronização
-- ===================
CREATE TABLE IF NOT EXISTS dl_sync_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- Componente que executou a operação
    componente VARCHAR(50) NOT NULL 
        CHECK (componente IN ('n8n', 'jules_codigo', 'jules_inquisidor', 'antigravity', 'supabase', 'github_actions')),
    
    -- Tipo de ação executada
    acao VARCHAR(50) NOT NULL 
        CHECK (acao IN ('pull', 'push', 'deploy', 'migration', 'validate', 'export_git', 'workflow_update', 'security_scan')),
    
    -- Detalhes da operação em formato JSON
    detalhes JSONB DEFAULT '{}',
    
    -- Status da operação
    status VARCHAR(20) DEFAULT 'ok' 
        CHECK (status IN ('ok', 'erro', 'pendente', 'bloqueado')),
    
    -- Mensagem de erro (se aplicável)
    erro_mensagem TEXT,
    
    -- Quem disparou (humano, cron, webhook, etc.)
    disparado_por VARCHAR(100) DEFAULT 'sistema',
    
    -- IP ou identificador da origem
    origem VARCHAR(255),
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Índices para consultas de auditoria
CREATE INDEX idx_sync_log_componente ON dl_sync_log(componente);
CREATE INDEX idx_sync_log_acao ON dl_sync_log(acao);
CREATE INDEX idx_sync_log_status ON dl_sync_log(status);
CREATE INDEX idx_sync_log_created ON dl_sync_log(created_at DESC);

-- RLS (obrigatório por política DL Nexus)
ALTER TABLE dl_sync_log ENABLE ROW LEVEL SECURITY;

-- Política: service_role tem acesso total (n8n, scripts, etc.)
CREATE POLICY "service_full_access_sync_log" 
    ON dl_sync_log 
    FOR ALL 
    USING (true) 
    WITH CHECK (true);

-- ===================
-- TABELA: dl_agent_registry
-- Registro de todos os agentes do ecossistema
-- ===================
CREATE TABLE IF NOT EXISTS dl_agent_registry (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    
    -- Identificação do agente
    nome VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL 
        CHECK (tipo IN ('ia_atendimento', 'ia_codigo', 'ia_inquisidor', 'ia_marketing', 'ia_orcamento', 'humano')),
    
    -- Configuração
    canal_principal VARCHAR(50),  -- 'whatsapp', 'github', 'ide', 'email'
    workflow_n8n VARCHAR(100),    -- ID ou nome do workflow associado
    modelo_ia VARCHAR(100),       -- 'gemini-flash', 'claude-sonnet', 'gpt-4o', etc.
    
    -- Status operacional
    ativo BOOLEAN DEFAULT true,
    ultima_execucao TIMESTAMPTZ,
    total_execucoes BIGINT DEFAULT 0,
    
    -- Metadados
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS
ALTER TABLE dl_agent_registry ENABLE ROW LEVEL SECURITY;

CREATE POLICY "service_full_access_agent_registry" 
    ON dl_agent_registry 
    FOR ALL 
    USING (true) 
    WITH CHECK (true);

-- Trigger para updated_at automático
CREATE TRIGGER agent_registry_updated_at
    BEFORE UPDATE ON dl_agent_registry
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ===================
-- DADOS INICIAIS: Registrar todos os agentes
-- ===================
INSERT INTO dl_agent_registry (nome, tipo, canal_principal, workflow_n8n, modelo_ia, ativo) VALUES
    ('Aninha', 'ia_atendimento', 'whatsapp', '002_roteador_aninha', 'gemini-flash + claude-sonnet', true),
    ('Jules Inquisidor', 'ia_inquisidor', 'whatsapp', '004_roteador_agentes_especializados', 'gpt-4o', true),
    ('Jules Código', 'ia_codigo', 'github', NULL, 'google-jules', true),
    ('Antigravity', 'ia_marketing', 'ide', NULL, 'gemini-pro', true),
    ('Agente de Orçamentos', 'ia_orcamento', 'ide', NULL, 'gemini-pro', true),
    ('Diogo Luiz', 'humano', 'whatsapp', '003_roteador_diego', NULL, true)
ON CONFLICT (nome) DO NOTHING;

-- ===================
-- VIEW: Painel de Saúde dos Agentes
-- ===================
CREATE OR REPLACE VIEW vw_agent_health AS
SELECT 
    ar.nome,
    ar.tipo,
    ar.canal_principal,
    ar.ativo,
    ar.ultima_execucao,
    ar.total_execucoes,
    COALESCE(
        (SELECT COUNT(*) FROM dl_sync_log sl 
         WHERE sl.componente = ar.nome 
         AND sl.created_at > NOW() - INTERVAL '24 hours'),
        0
    ) AS operacoes_24h,
    COALESCE(
        (SELECT COUNT(*) FROM dl_sync_log sl 
         WHERE sl.componente = ar.nome 
         AND sl.status = 'erro' 
         AND sl.created_at > NOW() - INTERVAL '24 hours'),
        0
    ) AS erros_24h
FROM dl_agent_registry ar
ORDER BY ar.nome;
