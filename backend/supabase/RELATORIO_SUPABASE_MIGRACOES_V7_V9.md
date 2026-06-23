# Relatório de Diagnóstico e Migrações Supabase (V7 / V9) — DL Nexus

**Data:** 2026-06-23  
**Status do Diagnóstico:** 🔴 BLOQUEADO LOCALMENTE (Erro de DNS / Rede)

---

## 1. Diagnóstico de Conexão Local

Executamos o script de diagnóstico de banco de dados (`scripts/check_supabase.js`) a partir do ambiente de execução do terminal. O resultado foi o seguinte erro de resolução de nomes:

```text
[*] Conectando ao Supabase para verificar tabelas...
[-] Erro ao verificar tabelas: Error: getaddrinfo ENOTFOUND db.nejdtvkpiclagsnfljsz.supabase.co
    at GetAddrInfoReqWrap.onlookupall [as oncomplete] (node:dns:122:26) {
  errno: -3008,
  code: 'ENOTFOUND',
  syscall: 'getaddrinfo',
  hostname: 'db.nejdtvkpiclagsnfljsz.supabase.co'
}
[*] Conexão encerrada.
```

### Análise Técnica:
Este erro indica que o DNS do ambiente local onde o agente opera não resolve domínios de bancos externos do Supabase (`supabase.co`), o que é padrão em ambientes isolados por sandboxes de rede ou firewalls. 

Como consequência, as migrações automáticas via scripts Node/Python locais estão bloqueadas. **O deploy do banco deve ser efetuado através do fallback manual no console do Supabase.**

---

## 2. Fallback Manual: Aplicação no SQL Editor

Para aplicar as migrações V7 e V9 no seu ambiente do Supabase:
1. Acesse o [Painel do Supabase](https://supabase.com).
2. Selecione o projeto `nejdtvkpiclagsnfljsz` (DL Nexus).
3. No menu lateral, acesse **SQL Editor** e clique em **New query**.
4. Copie o bloco SQL consolidado abaixo, cole no editor e clique em **Run**.

### SQL Consolidado e Idempotente (V7 + V9)

```sql
-- =========================================================================
-- MIGRAÇÃO V7: Tabela de Log de Publicações Digitais (Idempotente & Não-Destrutiva)
-- =========================================================================

CREATE TABLE IF NOT EXISTS dl_social_publicacoes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    semana_ref VARCHAR(50),
    data_planejada DATE,
    origem_conteudo VARCHAR(100),
    fonte_tipo VARCHAR(100),
    fonte_nome VARCHAR(255),
    fonte_url TEXT,
    fonte_data_publicacao DATE,
    fonte_data_consulta TIMESTAMP WITH TIME ZONE,
    produto_dl VARCHAR(100),
    publico_alvo VARCHAR(255),
    tema VARCHAR(255),
    resumo_fonte TEXT,
    comentario_tecnico_dl TEXT,
    texto_base TEXT,
    legenda_instagram TEXT,
    legenda_facebook TEXT,
    texto_google_business TEXT,
    roteiro_tiktok TEXT,
    texto_linkedin TEXT,
    hashtags JSONB DEFAULT '[]'::jsonb,
    image_url TEXT,
    video_url TEXT,
    status_revisao VARCHAR(50) DEFAULT 'rascunho_planejado',
    status_global VARCHAR(50) DEFAULT 'rascunho_planejado',
    bloqueios JSONB DEFAULT '[]'::jsonb,
    status_instagram VARCHAR(50) DEFAULT 'pendente',
    status_facebook VARCHAR(50) DEFAULT 'pendente',
    status_google_business VARCHAR(50) DEFAULT 'pendente',
    status_tiktok VARCHAR(50) DEFAULT 'pendente',
    status_linkedin VARCHAR(50) DEFAULT 'pendente',
    url_instagram TEXT,
    url_facebook TEXT,
    url_google_business TEXT,
    url_tiktok TEXT,
    url_linkedin TEXT,
    erros JSONB DEFAULT '{}'::jsonb,
    tentativas JSONB DEFAULT '{}'::jsonb,
    publicado_em JSONB DEFAULT '{}'::jsonb,
    relatorio_enviado BOOLEAN DEFAULT FALSE
);

-- Habilitar Row Level Security (RLS) se não estiver ativo
ALTER TABLE dl_social_publicacoes ENABLE ROW LEVEL SECURITY;

-- Políticas de Acesso
DROP POLICY IF EXISTS "Allow all operations for authenticated users" ON dl_social_publicacoes;
CREATE POLICY "Allow all operations for authenticated users" 
ON dl_social_publicacoes FOR ALL TO authenticated USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "Allow public read access" ON dl_social_publicacoes;
CREATE POLICY "Allow public read access" 
ON dl_social_publicacoes FOR SELECT TO public USING (true);


-- =========================================================================
-- MIGRAÇÃO V9: SDR Social (Instagram Direct + Facebook Messenger)
-- =========================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TABELA: dl_social_conversas
CREATE TABLE IF NOT EXISTS dl_social_conversas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    canal_origem VARCHAR(50) NOT NULL,
    sender_id VARCHAR(100) NOT NULL,
    page_id VARCHAR(100),
    instagram_business_account_id VARCHAR(100),
    nome_contato VARCHAR(255),
    username VARCHAR(255),
    telefone VARCHAR(50),
    email VARCHAR(255),
    tipo_cliente VARCHAR(100),
    nome_condominio_empresa VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255) DEFAULT 'Rio de Janeiro',
    servico_interesse TEXT,
    urgencia VARCHAR(50),
    status_conversa VARCHAR(50) DEFAULT 'ativa',
    etapa_funil VARCHAR(100) DEFAULT 'recepcao',
    lead_score INTEGER DEFAULT 0,
    responsavel_humano VARCHAR(255),
    precisa_humano BOOLEAN DEFAULT FALSE,
    ultimo_resumo TEXT,
    tags JSONB DEFAULT '[]'::jsonb,
    raw_profile JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT uq_social_conversa_canal_sender UNIQUE (canal_origem, sender_id)
);

CREATE INDEX IF NOT EXISTS idx_social_conv_canal_sender ON dl_social_conversas(canal_origem, sender_id);
CREATE INDEX IF NOT EXISTS idx_social_conv_status ON dl_social_conversas(status_conversa);
CREATE INDEX IF NOT EXISTS idx_social_conv_etapa ON dl_social_conversas(etapa_funil);
CREATE INDEX IF NOT EXISTS idx_social_conv_created ON dl_social_conversas(created_at DESC);

-- TABELA: dl_social_mensagens
CREATE TABLE IF NOT EXISTS dl_social_mensagens (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    conversa_id UUID REFERENCES dl_social_conversas(id) ON DELETE SET NULL,
    canal_origem VARCHAR(50) NOT NULL,
    sender_id VARCHAR(100),
    direction VARCHAR(20) NOT NULL DEFAULT 'inbound',
    message_id VARCHAR(255),
    texto TEXT,
    tipo_mensagem VARCHAR(50) DEFAULT 'text',
    raw_event JSONB DEFAULT '{}'::jsonb,
    status_processamento VARCHAR(50) DEFAULT 'recebido'
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_social_msg_dedup
    ON dl_social_mensagens(canal_origem, message_id)
    WHERE message_id IS NOT NULL AND message_id != '';

CREATE INDEX IF NOT EXISTS idx_social_msg_conversa ON dl_social_mensagens(conversa_id);
CREATE INDEX IF NOT EXISTS idx_social_msg_canal_sender ON dl_social_mensagens(canal_origem, sender_id);
CREATE INDEX IF NOT EXISTS idx_social_msg_created ON dl_social_mensagens(created_at DESC);

-- TABELA: dl_social_leads
CREATE TABLE IF NOT EXISTS dl_social_leads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    conversa_id UUID REFERENCES dl_social_conversas(id) ON DELETE SET NULL,
    canal_origem VARCHAR(50),
    nome VARCHAR(255),
    username VARCHAR(255),
    telefone VARCHAR(50),
    email VARCHAR(255),
    tipo_cliente VARCHAR(100),
    nome_condominio_empresa VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255) DEFAULT 'Rio de Janeiro',
    servico_interesse TEXT,
    urgencia VARCHAR(50),
    dor_principal TEXT,
    cargo_decisor VARCHAR(255),
    lead_score INTEGER DEFAULT 0,
    status_lead VARCHAR(50) DEFAULT 'novo',
    proxima_acao TEXT,
    data_preferida_avaliacao VARCHAR(255),
    observacoes TEXT,
    origem_ia VARCHAR(100) DEFAULT 'aninha_sdr_social'
);

CREATE INDEX IF NOT EXISTS idx_social_lead_status ON dl_social_leads(status_lead);
CREATE INDEX IF NOT EXISTS idx_social_lead_score ON dl_social_leads(lead_score DESC);
CREATE INDEX IF NOT EXISTS idx_social_lead_canal ON dl_social_leads(canal_origem);
CREATE INDEX IF NOT EXISTS idx_social_lead_conversa ON dl_social_leads(conversa_id);
CREATE INDEX IF NOT EXISTS idx_social_lead_created ON dl_social_leads(created_at DESC);

-- RLS
ALTER TABLE dl_social_conversas ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_social_mensagens ENABLE ROW LEVEL SECURITY;
ALTER TABLE dl_social_leads ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "service_full_access_social_conversas" ON dl_social_conversas;
DROP POLICY IF EXISTS "service_full_access_social_mensagens" ON dl_social_mensagens;
DROP POLICY IF EXISTS "service_full_access_social_leads" ON dl_social_leads;

CREATE POLICY "service_full_access_social_conversas" ON dl_social_conversas FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_social_mensagens" ON dl_social_mensagens FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "service_full_access_social_leads" ON dl_social_leads FOR ALL USING (true) WITH CHECK (true);

-- Trigger updated_at para conversas
CREATE OR REPLACE FUNCTION update_social_conversas_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_social_conversas_updated_at ON dl_social_conversas;
CREATE TRIGGER trg_social_conversas_updated_at
    BEFORE UPDATE ON dl_social_conversas
    FOR EACH ROW EXECUTE FUNCTION update_social_conversas_updated_at();
```

---

## 3. Storage Público no Supabase (dl-meta-assets-public)

Para que as publicações no Instagram pelo n8n Cloud funcionem de forma 100% confiável, é estritamente obrigatório termos um repositório público de imagens acessível via URL HTTPS. 
O Instagram Graph API exige que o endpoint `/media` receba uma URL pública válida (ele não aceita uploads de binários diretos ou links privados do Google Drive).

### Ação no Supabase:
1. No painel do Supabase, acesse **Storage**.
2. Clique em **New bucket**.
3. Defina o nome como: `dl-meta-assets-public`.
4. **IMPORTANTE:** Ative a opção **Public bucket** (isso garante acesso público a todas as imagens via URL direta sem autenticação).
5. Defina a política de acesso (Policies) no Storage para permitir que a API Key (Service Role) do n8n possa inserir (`INSERT`) e ler (`SELECT`) arquivos no bucket.

### Integração no n8n:
A URL pública estável gerada pelo Supabase segue a seguinte estrutura:
`https://nejdtvkpiclagsnfljsz.supabase.co/storage/v1/object/public/dl-meta-assets-public/caminho_da_imagem.jpg`

Esta URL será atribuída ao campo `image_url_publica_meta` no payload final do workflow 151 antes de disparar o publicador 081.

---

## 4. Pendências e Próximos Passos
1. O usuário deve copiar e rodar o SQL acima no painel do Supabase.
2. O usuário deve criar o bucket `dl-meta-assets-public` no painel do Supabase Storage.
3. Configurar as seguintes variáveis no n8n Cloud relacionadas ao Storage:
   - `PUBLIC_ASSET_STORAGE_PROVIDER=supabase`
   - `SUPABASE_STORAGE_BUCKET_PUBLIC=dl-meta-assets-public`
   - `SUPABASE_PUBLIC_ASSET_BASE_URL=https://nejdtvkpiclagsnfljsz.supabase.co/storage/v1/object/public/dl-meta-assets-public`
