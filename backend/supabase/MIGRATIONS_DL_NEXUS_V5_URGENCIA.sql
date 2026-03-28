-- =============================================
-- DL NEXUS - MIGRATION V5 - URGENCIA E CATEGORIA
-- =============================================

-- Criação do tipo ENUM para urgência, se não existir
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nivel_urgencia') THEN
        CREATE TYPE nivel_urgencia AS ENUM ('baixa', 'media', 'alta', 'critica');
    END IF;
END $$;

-- Criação do tipo ENUM para categoria de serviço, se não existir
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'tipo_categoria_servico') THEN
        CREATE TYPE tipo_categoria_servico AS ENUM ('eletrica', 'solar', 'incendio', 'seguranca', 'mobilidade', 'automacao');
    END IF;
END $$;

-- Adiciona as colunas na tabela 'leads' (sem quebrar dados existentes)
ALTER TABLE leads
ADD COLUMN IF NOT EXISTS urgencia nivel_urgencia DEFAULT 'baixa',
ADD COLUMN IF NOT EXISTS categoria_servico tipo_categoria_servico;

-- Atualiza dados legados baseados em colunas antigas (Opcional, mas recomendado para consistência)
UPDATE leads
SET categoria_servico = 'eletrica' WHERE tipo_servico = 'ELETRICO' AND categoria_servico IS NULL;
UPDATE leads
SET categoria_servico = 'solar' WHERE tipo_servico = 'SOLAR' AND categoria_servico IS NULL;
UPDATE leads
SET categoria_servico = 'seguranca' WHERE tipo_servico = 'SEGURANCA' AND categoria_servico IS NULL;
UPDATE leads
SET categoria_servico = 'incendio' WHERE tipo_servico = 'INCENDIO' AND categoria_servico IS NULL;
UPDATE leads
SET categoria_servico = 'mobilidade' WHERE tipo_servico = 'MOBILIDADE' AND categoria_servico IS NULL;
UPDATE leads
SET categoria_servico = 'automacao' WHERE tipo_servico = 'AUTOMACAO' AND categoria_servico IS NULL;
