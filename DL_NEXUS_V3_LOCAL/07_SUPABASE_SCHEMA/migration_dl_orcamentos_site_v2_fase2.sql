-- ═══════════════════════════════════════════
-- MIGRATION: ALTER_dl_orcamentos_site_v2_fase2
-- ═══════════════════════════════════════════

ALTER TABLE dl_orcamentos_site_v2
ADD COLUMN IF NOT EXISTS perfil_classificado text,
ADD COLUMN IF NOT EXISTS linha_dl text,
ADD COLUMN IF NOT EXISTS markdown_orcamento text,
ADD COLUMN IF NOT EXISTS status_killcritic text;

COMMENT ON COLUMN dl_orcamentos_site_v2.perfil_classificado IS 'Classificação de perfil gerada pelo workflow 061 (ex: condominio, pessoa_fisica, pj_restaurante).';
COMMENT ON COLUMN dl_orcamentos_site_v2.linha_dl IS 'Linha de serviço DL sugerida pelo classificador (ex: DL Guardião, DL Express).';
COMMENT ON COLUMN dl_orcamentos_site_v2.markdown_orcamento IS 'Rascunho de orçamento gerado em Markdown pelo workflow 063.';
COMMENT ON COLUMN dl_orcamentos_site_v2.status_killcritic IS 'Status de revisão automatizada do KILLCRITIC (workflow 064).';
