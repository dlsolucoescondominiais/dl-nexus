CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE leads (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    nome_contato VARCHAR(255) NOT NULL,
    nome_condominio VARCHAR(255),
    telefone VARCHAR(20),
    email VARCHAR(255),
    tipo_imovel VARCHAR(50), -- Condomínio, Colégio, etc.
    num_unidades INT,
    tipo_servico TEXT, -- Redes, Solar, Elétrica, etc.
    status VARCHAR(50) DEFAULT 'novo',
    mensagem TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
