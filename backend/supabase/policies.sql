-- =============================================
-- DL NEXUS - ROW LEVEL SECURITY (RLS) POLICIES
-- =============================================

-- Habilitar RLS em todas as tabelas principais
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.mensagens_whatsapp ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.avaliacoes_tecnicas ENABLE ROW LEVEL SECURITY;

-- Política 1: Usuários Anônimos/Públicos (Não podem ler, podem inserir leads limitados via site)
CREATE POLICY "Permitir inserção anônima de Leads (Site)"
ON public.leads
FOR INSERT
TO anon
WITH CHECK (origem = 'site');

-- Política 2: Service Role (API do Python e n8n Webhooks têm acesso total)
CREATE POLICY "Service Role tem acesso total aos Leads"
ON public.leads
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

CREATE POLICY "Service Role tem acesso total as Mensagens"
ON public.mensagens_whatsapp
FOR ALL
TO service_role
USING (true)
WITH CHECK (true);

-- Política 3: Usuários Autenticados (Técnicos logados no Painel React)
-- Técnicos podem ver todos os leads que não são 'perdidos' e podem criar avaliações
CREATE POLICY "Técnicos leem leads ativos"
ON public.leads
FOR SELECT
TO authenticated
USING (status != 'perdido');

CREATE POLICY "Técnicos atualizam leads"
ON public.leads
FOR UPDATE
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "Técnicos leem/escrevem avaliações"
ON public.avaliacoes_tecnicas
FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);

CREATE POLICY "Técnicos leem/escrevem mensagens (Chat)"
ON public.mensagens_whatsapp
FOR ALL
TO authenticated
USING (true)
WITH CHECK (true);
