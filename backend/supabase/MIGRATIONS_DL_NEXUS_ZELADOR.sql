-- =========================================================================
-- MIGRATION: Agente Zelador Google Drive
-- =========================================================================

-- Tabela de Inventário
create table if not exists drive_zelador_inventory (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  updated_at timestamptz default now(),

  file_id text not null unique,
  file_name text,
  file_extension text,
  mime_type text,
  file_size bigint,

  drive_source text default 'google_drive',
  current_folder_id text,
  current_folder_name text,
  current_path text,

  owner_email text,
  web_view_link text,

  md5_checksum text,
  created_time timestamptz,
  modified_time timestamptz,

  categoria_detectada text,
  categoria_sugerida text,
  pasta_destino_sugerida text,
  pasta_destino_id text,

  confianca numeric default 0,
  motivo_classificacao text,
  risco text default 'baixo',

  duplicado_suspeito boolean default false,
  duplicado_de_file_id text,
  precisa_revisao_humana boolean default false,

  acao_sugerida text default 'classificar',
  acao_aprovada text,
  status text default 'novo',

  processado_por text,
  erro text,
  observacao text
);

-- Tabela de Pastas Permitidas (Allowlist)
create table if not exists drive_zelador_allowed_folders (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),

  folder_key text not null unique,
  folder_name text not null,
  folder_id text not null unique,

  categoria text,
  ativo boolean default true,
  prioridade int default 100,
  observacao text
);

-- Inserção de dados modelo (Os IDs devem ser atualizados em Produção)
insert into drive_zelador_allowed_folders
(folder_key, folder_name, folder_id, categoria, prioridade)
values
('INBOX_SMARTPHONE', '00_INBOX_SMARTPHONE', 'ID_DA_PASTA_INBOX', 'inbox', 10),
('AUDIOS', '01. ÁUDIOS', 'ID_DA_PASTA_AUDIOS', 'audio', 20),
('CONTRATOS_DOCUMENTOS', '02. CONTRATOS E DOCUMENTOS', 'ID_DA_PASTA_DOCS', 'documentos', 30),
('FOTOS_VIDEOS', '03. FOTOS E VÍDEOS', 'ID_DA_PASTA_MIDIA', 'midia', 40),
('TRIAGEM_HUMANA', '04. TRIAGEM_REVISAO_HUMANA', 'ID_DA_PASTA_TRIAGEM', 'triagem', 999),
('CENTRAL_MEMORIA', '05. CENTRAL DE MEMÓRIA', 'ID_DA_PASTA_MEMORIA', 'memoria', 50),
('FOOD_SERVICE_MULTGRILL', 'FOOD_SERVICE_MULTGRILL', 'ID_DA_PASTA_MULTGRILL', 'food_service', 60),
('CONDOMINIOS_COLEGIOS', 'CONDOMINIOS_COLEGIOS', 'ID_DA_PASTA_CONDOMINIOS', 'condominios_colegios', 70),
('FINANCEIRO', 'FINANCEIRO', 'ID_DA_PASTA_FINANCEIRO', 'financeiro', 80),
('FORNECEDORES', 'FORNECEDORES', 'ID_DA_PASTA_FORNECEDORES', 'fornecedores', 90)
ON CONFLICT (folder_key) DO NOTHING;

-- Tabela de Regras Ajustáveis
create table if not exists drive_zelador_rules (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz default now(),
  updated_at timestamptz default now(),

  rule_name text not null,
  rule_type text not null,
  condition_text text not null,
  target_category text not null,
  target_folder_key text not null,

  confidence_weight numeric default 0.8,
  active boolean default false,
  suggested_by text,
  approved_by text,
  approval_status text default 'pending',

  notes text
);
