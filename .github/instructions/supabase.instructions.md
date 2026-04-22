---
description: "Regras para queries Supabase, migrações SQL e segurança RLS"
applyTo: "backend/supabase/**,**/*.sql,**/lib/supabase*.{ts,js}"
---

# Instruções: Supabase / PostgreSQL — DL Nexus

## Schema Padrão

Toda nova tabela DEVE seguir este template base:

```sql
CREATE TABLE public.nome_tabela (
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
  created_at  TIMESTAMPTZ NOT NULL    DEFAULT NOW(),
  updated_at  TIMESTAMPTZ NOT NULL    DEFAULT NOW()
  -- ... colunas específicas ...
);

-- Trigger de updated_at (obrigatório)
CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON public.nome_tabela
  FOR EACH ROW EXECUTE FUNCTION public.handle_updated_at();

-- RLS (obrigatório — nunca deixar tabela sem política)
ALTER TABLE public.nome_tabela ENABLE ROW LEVEL SECURITY;
```

## Tabelas Principais DL Nexus

| Tabela | Descrição |
|--------|-----------|
| `leads` | Prospects B2B (síndicos, administradoras) |
| `avaliacoes_tecnicas` | Agendamentos de Avaliação Técnica |
| `projetos` | Portfolio de projetos executados |
| `clientes` | Contratantes ativos |
| `orcamentos` | Propostas comerciais geradas |

## Queries TypeScript (Supabase Client)

```typescript
// ✅ CORRETO — sempre listar colunas, nunca SELECT *
const { data, error } = await supabase
  .from('leads')
  .select('id, nome, email, servico_interesse, score, created_at')
  .eq('status', 'novo')
  .order('created_at', { ascending: false });

if (error) throw new Error(`Falha ao buscar leads: ${error.message}`);

// ❌ ERRADO
const { data } = await supabase.from('leads').select('*');
```

## RLS Policies (padrão)

```sql
-- Leitura: apenas usuários autenticados da organização
CREATE POLICY "leads_select_autenticados"
  ON public.leads FOR SELECT
  TO authenticated
  USING (auth.role() = 'authenticated');

-- Inserção: permitida via service_role (n8n/API) e authenticated
CREATE POLICY "leads_insert_api"
  ON public.leads FOR INSERT
  TO authenticated, service_role
  WITH CHECK (true);
```

## Migrações

- Nomear: `YYYY-MM-DD_descricao_da_migracao.sql`
- Sempre incluir `-- Rollback:` comentado no topo
- Nunca usar `DROP TABLE` sem backup documentado
- Testar em Supabase local (`supabase start`) antes de aplicar em produção
