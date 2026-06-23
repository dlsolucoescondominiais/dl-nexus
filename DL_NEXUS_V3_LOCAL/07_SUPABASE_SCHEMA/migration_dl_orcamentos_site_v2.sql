-- ═══════════════════════════════════════════
-- MIGRATION: dl_orcamentos_site_v2
-- Motor de Orçamento V2 — DL Nexus
-- Tabela de recepção de leads via Formulário V2
-- ═══════════════════════════════════════════

CREATE TABLE IF NOT EXISTS dl_orcamentos_site_v2 (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  protocolo text NOT NULL UNIQUE,

  -- Origem
  origem text DEFAULT 'site',
  versao_form text DEFAULT 'V2',

  -- Lead
  nome text NOT NULL,
  whatsapp text NOT NULL,
  email text NOT NULL,
  tipo_cliente text NOT NULL,
  nome_empresa_ou_condominio text NOT NULL,
  cnpj text,
  cpf_hash_ou_mascarado text,
  responsavel_aprovacao text,

  -- Localização
  cep text,
  endereco_completo text,
  bairro text NOT NULL,
  cidade text NOT NULL,

  -- Demanda
  servico_interesse text NOT NULL,
  urgencia text NOT NULL DEFAULT 'media',
  descricao text NOT NULL,
  tipo_orcamento text,
  melhor_horario text,

  -- Infraestrutura
  numero_unidades integer,
  numero_blocos integer,
  rateio_permitido boolean DEFAULT false,

  -- Mídia
  midia_urls jsonb DEFAULT '[]'::jsonb,

  -- Consentimento
  consentimento_lgpd boolean NOT NULL DEFAULT false,

  -- Controle
  pendencias jsonb DEFAULT '[]'::jsonb,
  status_orcamento text NOT NULL DEFAULT 'recebido_para_triagem',
  payload_original jsonb,

  -- Timestamps
  criado_em timestamptz DEFAULT now(),
  atualizado_em timestamptz DEFAULT now()
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_orc_v2_status ON dl_orcamentos_site_v2(status_orcamento);
CREATE INDEX IF NOT EXISTS idx_orc_v2_tipo ON dl_orcamentos_site_v2(tipo_cliente);
CREATE INDEX IF NOT EXISTS idx_orc_v2_urgencia ON dl_orcamentos_site_v2(urgencia);
CREATE INDEX IF NOT EXISTS idx_orc_v2_criado ON dl_orcamentos_site_v2(criado_em DESC);

-- RLS (Row Level Security) — ativar futuramente
-- ALTER TABLE dl_orcamentos_site_v2 ENABLE ROW LEVEL SECURITY;

COMMENT ON TABLE dl_orcamentos_site_v2 IS 'Leads de Avaliação Técnica V2 capturados pelo site DL Soluções Condominiais. CPF armazenado apenas mascarado.';
COMMENT ON COLUMN dl_orcamentos_site_v2.cpf_hash_ou_mascarado IS 'CPF mascarado (ex: 123.***.789-01). Nunca armazenar CPF pleno nesta tabela.';
COMMENT ON COLUMN dl_orcamentos_site_v2.rateio_permitido IS 'true apenas se tipo_cliente=condominio E numero_unidades preenchido. Caso contrário, bloquear cálculo de valor por unidade.';
