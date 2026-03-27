-- ============================================================================
-- DL NEXUS - MIGRATION V5 (POLÍTICAS RLS DE SEGURANÇA B2B)
-- Data: 25 de março de 2026
-- Proprietário: Diogo Luiz de Oliveira (Tecnólogo em Infraestrutura)
-- ============================================================================

-- 1. ATIVAR ROW LEVEL SECURITY NAS TABELAS CRÍTICAS
ALTER TABLE condominios ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE avaliacoes_tecnicas ENABLE ROW LEVEL SECURITY;
ALTER TABLE propostas ENABLE ROW LEVEL SECURITY;

-- ----------------------------------------------------------------------------
-- POLÍTICAS: TÉCNICOS E ADMINS DA DL SOLUÇÕES (ACESSO TOTAL)
-- Assume que os e-mails administrativos terminam em '@dlsolucoescondominiais.com.br'
-- ou que existe uma função is_admin() - para simplificar, usaremos o sufixo de email
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION is_admin_or_tecnico()
RETURNS BOOLEAN AS $$
BEGIN
  RETURN (auth.email() LIKE '%@dlsolucoescondominiais.com.br');
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ----------------------------------------------------------------------------
-- 2. POLÍTICAS PARA CONDOMÍNIOS
-- Síndicos podem ler seu próprio condomínio. Admins leem todos.
-- ----------------------------------------------------------------------------
CREATE POLICY "Admins leem todos os condominios"
  ON condominios FOR ALL
  TO authenticated
  USING (is_admin_or_tecnico());

CREATE POLICY "Sindicos leem apenas seus condominios"
  ON condominios FOR SELECT
  TO authenticated
  USING (id IN (SELECT condominio_id FROM usuarios WHERE usuarios.id = auth.uid()));

-- ----------------------------------------------------------------------------
-- 3. POLÍTICAS PARA LEADS E AVALIAÇÕES TÉCNICAS
-- Visitantes anônimos só podem fazer INSERT (criar novo lead via site/whatsapp).
-- Síndicos logados podem visualizar os leads atrelados ao seu condomínio.
-- ----------------------------------------------------------------------------
CREATE POLICY "Qualquer pessoa pode inserir leads (formulario/bot)"
  ON leads FOR INSERT
  WITH CHECK (true);

CREATE POLICY "Admins controle total dos leads"
  ON leads FOR ALL
  TO authenticated
  USING (is_admin_or_tecnico());

CREATE POLICY "Sindicos leem seus leads e demandas"
  ON leads FOR SELECT
  TO authenticated
  USING (condominio_id IN (SELECT condominio_id FROM usuarios WHERE usuarios.id = auth.uid()));

CREATE POLICY "Admins controle total das avaliacoes"
  ON avaliacoes_tecnicas FOR ALL
  TO authenticated
  USING (is_admin_or_tecnico());

CREATE POLICY "Sindicos leem avaliacoes do seu lead"
  ON avaliacoes_tecnicas FOR SELECT
  TO authenticated
  USING (lead_id IN (SELECT id FROM leads WHERE condominio_id IN (SELECT condominio_id FROM usuarios WHERE usuarios.id = auth.uid())));

-- ----------------------------------------------------------------------------
-- 4. POLÍTICAS PARA PROPOSTAS (DOCUMENTOS CONFIDENCIAIS OPEX)
-- Apenas o síndico daquele condomínio pode ler sua proposta orçamentária.
-- ----------------------------------------------------------------------------
CREATE POLICY "Admins controle total das propostas"
  ON propostas FOR ALL
  TO authenticated
  USING (is_admin_or_tecnico());

CREATE POLICY "Sindicos leem as propostas do seu condominio"
  ON propostas FOR SELECT
  TO authenticated
  USING (condominio_id IN (SELECT condominio_id FROM usuarios WHERE usuarios.id = auth.uid()));

-- Opcional: Síndicos podem ATUALIZAR a proposta (aceitar/recusar)
CREATE POLICY "Sindicos podem aceitar/recusar propostas"
  ON propostas FOR UPDATE
  TO authenticated
  USING (condominio_id IN (SELECT condominio_id FROM usuarios WHERE usuarios.id = auth.uid()))
  WITH CHECK (status IN ('aceita', 'rejeitada', 'visualizada'));
