-- Fase 1 MVP DL Orçamento - Schema Supabase PostgreSQL

-- 1. usuarios_perfis
CREATE TABLE IF NOT EXISTS usuarios_perfis (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    nome TEXT NOT NULL,
    cargo TEXT,
    email TEXT UNIQUE NOT NULL,
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 2. clientes
CREATE TABLE IF NOT EXISTS clientes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome TEXT NOT NULL,
    cnpj_cpf TEXT,
    telefone TEXT,
    email TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 3. locais_atendimento
CREATE TABLE IF NOT EXISTS locais_atendimento (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID REFERENCES clientes(id) ON DELETE CASCADE,
    tipo_local TEXT CHECK (tipo_local IN ('condominio', 'empresa', 'colegio', 'restaurante', 'lanchonete', 'administradora', 'outro')) NOT NULL,
    nome TEXT NOT NULL,
    cnpj_cpf TEXT,
    endereco TEXT,
    bairro TEXT,
    cidade TEXT,
    uf TEXT,
    responsavel_nome TEXT,
    responsavel_telefone TEXT,
    responsavel_email TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 4. servicos_catalogo
CREATE TABLE IF NOT EXISTS servicos_catalogo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome TEXT NOT NULL,
    descricao TEXT,
    ativo BOOLEAN DEFAULT true,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Inserir serviços iniciais
INSERT INTO servicos_catalogo (nome, descricao) VALUES
('DL Guardião', 'CFTV e segurança eletrônica'),
('DL Fortress', 'Controle de acesso, portaria autônoma e gestão de acesso'),
('DL Acqua', 'Automação e monitoramento técnico de bombas, cisternas e caixas d''água'),
('Gatekeeper', 'Automação de portões e acessos'),
('DL Volt', 'Elétrica predial e automação'),
('DL EcoVolt Solar', 'Energia solar'),
('DL VoltCharge', 'Infraestrutura para carregadores veiculares'),
('DL Alerta', 'Prevenção de incêndio'),
('DL Partner', 'Manutenção recorrente, histórico de atendimento e tempo de resposta para chamados'),
('Mult•Grill Express', 'Suporte técnico DL - chapas, grills e fritadeiras profissionais')
ON CONFLICT DO NOTHING;

-- 5. avaliacoes_tecnicas
CREATE TABLE IF NOT EXISTS avaliacoes_tecnicas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    cliente_id UUID REFERENCES clientes(id),
    local_id UUID REFERENCES locais_atendimento(id),
    servico_id UUID REFERENCES servicos_catalogo(id),
    origem_lead TEXT,
    canal_entrada TEXT,
    status TEXT CHECK (status IN ('novo', 'em_triagem', 'agendada', 'em_analise', 'aguardando_cliente', 'orcamento_em_preparo', 'orcamento_enviado', 'aprovado', 'recusado', 'cancelado')) DEFAULT 'novo',
    prioridade TEXT DEFAULT 'normal',
    descricao_inicial TEXT,
    observacoes_tecnicas TEXT,
    url_pasta_drive TEXT,
    data_agendada TIMESTAMP WITH TIME ZONE,
    data_realizada TIMESTAMP WITH TIME ZONE,
    responsavel_tecnico UUID REFERENCES usuarios_perfis(id),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 6. orcamentos
CREATE TABLE IF NOT EXISTS orcamentos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    avaliacao_tecnica_id UUID REFERENCES avaliacoes_tecnicas(id),
    cliente_id UUID REFERENCES clientes(id),
    local_id UUID REFERENCES locais_atendimento(id),
    codigo_orcamento TEXT UNIQUE,
    titulo TEXT NOT NULL,
    status TEXT DEFAULT 'rascunho',
    validade_dias INTEGER DEFAULT 15,
    prazo_execucao TEXT,
    garantia TEXT,
    observacoes_cliente TEXT,
    observacoes_internas TEXT,
    valor_material DECIMAL(10,2) DEFAULT 0,
    valor_mao_obra DECIMAL(10,2) DEFAULT 0,
    valor_deslocamento DECIMAL(10,2) DEFAULT 0,
    valor_avaliacao_tecnica DECIMAL(10,2) DEFAULT 0,
    valor_custos_indiretos DECIMAL(10,2) DEFAULT 0,
    valor_impostos DECIMAL(10,2) DEFAULT 0,
    margem_percentual DECIMAL(5,2) DEFAULT 0,
    desconto_percentual DECIMAL(5,2) DEFAULT 0,
    valor_total DECIMAL(10,2) DEFAULT 0,
    forma_pagamento TEXT,
    versao_cliente_html TEXT,
    versao_interna_html TEXT,
    pdf_url TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 7. orcamento_itens
CREATE TABLE IF NOT EXISTS orcamento_itens (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orcamento_id UUID REFERENCES orcamentos(id) ON DELETE CASCADE,
    tipo_item TEXT CHECK (tipo_item IN ('material', 'mao_obra', 'deslocamento', 'avaliacao_tecnica', 'imposto', 'desconto', 'custo_indireto', 'equipamento', 'servico')) NOT NULL,
    categoria TEXT,
    descricao TEXT NOT NULL,
    quantidade DECIMAL(10,2) DEFAULT 1,
    unidade TEXT,
    custo_unitario DECIMAL(10,2) DEFAULT 0,
    preco_unitario DECIMAL(10,2) DEFAULT 0,
    subtotal_custo DECIMAL(10,2) DEFAULT 0,
    subtotal_venda DECIMAL(10,2) DEFAULT 0,
    fornecedor TEXT,
    observacao_interna TEXT,
    visivel_cliente BOOLEAN DEFAULT true,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 8. orcamento_anexos
CREATE TABLE IF NOT EXISTS orcamento_anexos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    avaliacao_tecnica_id UUID REFERENCES avaliacoes_tecnicas(id) ON DELETE CASCADE,
    orcamento_id UUID REFERENCES orcamentos(id) ON DELETE CASCADE,
    tipo_anexo TEXT CHECK (tipo_anexo IN ('foto', 'video', 'pdf', 'documento', 'audio', 'planilha')) NOT NULL,
    nome_arquivo TEXT NOT NULL,
    url_arquivo TEXT NOT NULL,
    origem TEXT CHECK (origem IN ('site', 'whatsapp', 'drive', 'upload_manual', 'n8n')) NOT NULL,
    observacao TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 9. orcamento_eventos
CREATE TABLE IF NOT EXISTS orcamento_eventos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    orcamento_id UUID REFERENCES orcamentos(id) ON DELETE CASCADE,
    usuario_id UUID REFERENCES usuarios_perfis(id),
    tipo_evento TEXT NOT NULL,
    descricao TEXT NOT NULL,
    dados_json JSONB,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 10. fornecedores
CREATE TABLE IF NOT EXISTS fornecedores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome TEXT NOT NULL,
    cnpj_cpf TEXT,
    contato TEXT,
    telefone TEXT,
    email TEXT,
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 11. materiais_catalogo
CREATE TABLE IF NOT EXISTS materiais_catalogo (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome TEXT NOT NULL,
    descricao TEXT,
    categoria TEXT,
    unidade TEXT,
    custo_base DECIMAL(10,2) DEFAULT 0,
    fornecedor_id UUID REFERENCES fornecedores(id),
    criado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- 12. configuracoes_precificacao
CREATE TABLE IF NOT EXISTS configuracoes_precificacao (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chave TEXT UNIQUE NOT NULL,
    valor JSONB NOT NULL,
    descricao TEXT,
    atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Configurações iniciais
INSERT INTO configuracoes_precificacao (chave, valor, descricao) VALUES
('margem_padrao', '{"valor": 30}', 'Margem de lucro padrão em %'),
('imposto_padrao', '{"valor": 15}', 'Imposto padrão em %')
ON CONFLICT DO NOTHING;
