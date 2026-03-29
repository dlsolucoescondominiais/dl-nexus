-- 1. Cria a tabela de propostas (caso não exista, para garantir que as políticas funcionem)
CREATE TABLE IF NOT EXISTS public.propostas (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    lead_id UUID REFERENCES public.leads(id),
    condominio_user_id UUID REFERENCES auth.users(id), -- ID do síndico na auth table
    tipo_servico VARCHAR(50),
    texto_proposta TEXT,
    valor_total NUMERIC(10, 2),
    status VARCHAR(50) DEFAULT 'enviada',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Ativar RLS na tabela de propostas
ALTER TABLE public.propostas ENABLE ROW LEVEL SECURITY;

-- 3. Política 1: Administrador (Diogo/Técnicos) pode ver e modificar TUDO
-- Assumimos que a role 'admin' pode vir via Claims JWT personalizados
CREATE POLICY "Admin ve tudo" ON public.propostas
FOR ALL USING (
  auth.jwt() ->> 'role' = 'admin'
);

-- 4. Política 2: Síndico só vê a proposta do próprio condomínio (amarrado pelo ID de usuário)
CREATE POLICY "Sindico ve apenas seu condominio" ON public.propostas
FOR SELECT USING (
  auth.uid() = condominio_user_id
);
