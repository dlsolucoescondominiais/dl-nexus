-- =============================================
-- DL NEXUS - ESQUEMA DE BANCO DE DADOS (SUPABASE) - V2 (AMPLIAÇÃO)
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- =============================================

-- Aqui entra a V2 do banco de dados B2B OPEX.
-- (Preenchido em interações futuras baseadas na demanda de ampliação do portal de Síndicos)
-- Por enquanto, este script isola futuras quebras do sistema base.

CREATE TABLE IF NOT EXISTS portal_sindico_documentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    condominio_id UUID REFERENCES leads(id),
    url_art TEXT,
    url_contrato TEXT,
    validade_ltcat DATE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Habilitar Realtime para a nova funcionalidade de portal
alter publication supabase_realtime add table portal_sindico_documentos;
