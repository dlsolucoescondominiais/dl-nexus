-- ============================================================================
-- DL NEXUS - MIGRATION V7 (SITE INTEGRATION & PERSONA MAPPING)
-- Data: 08 de abril de 2026
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- Objetivo: Suportar integração end-to-end com formulários do site oficial
-- ============================================================================

-- 1. ADIÇÃO DE COLUNAS DE PERSONA E HISTÓRICO DE DORES (PAGOS PELO SITE)
ALTER TABLE leads ADD COLUMN IF NOT EXISTS persona TEXT;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS historico_das_dores TEXT;

-- 2. GARANTIR QUE A ORIGEM 'site' EXISTA NO ENUM (Se aplicável)
-- Nota: O enum origem_lead foi criado na V3 com ('whatsapp', 'telegram', 'email', 'site').
-- Caso usemos strings simples no futuro, aqui garantimos a integridade.

-- 3. LOG DE MUDANÇA
COMMENT ON COLUMN leads.persona IS 'Categoria do lead (sindico, admin, escola) para tom de voz da IA';
COMMENT ON COLUMN leads.historico_das_dores IS 'Transcrição bruta do campo mensagem do site oficial';
