-- 1. Criação de Índice para busca rápida de telefones e deduplicação
CREATE INDEX IF NOT EXISTS idx_leads_telefone ON public.leads (telefone);

-- 2. Rotina de Limpeza Automática (LIXO / SPAM) para economizar Storage
-- A função deforma dados com status 'LIXO' criados há mais de 7 dias
CREATE OR REPLACE FUNCTION limpa_leads_lixo_antigos()
RETURNS void AS $$
BEGIN
    DELETE FROM public.leads
    WHERE status = 'LIXO'
    AND created_at < NOW() - INTERVAL '7 days';
END;
$$ LANGUAGE plpgsql;

-- Para rodar esta função automaticamente, é recomendável habilitar o pg_cron no Supabase:
-- CREATE EXTENSION IF NOT EXISTS pg_cron;
-- SELECT cron.schedule('0 3 * * *', $$SELECT limpa_leads_lixo_antigos()$$);
-- Comentado para não forçar a extensão caso o usuário esteja num plano restrito, mas o código está pronto.

-- 3. Função Anti-Deduplicação de Inserção Bruta
-- Evita que um bot mande o mesmo lead 10 vezes em 5 minutos
CREATE OR REPLACE FUNCTION bloqueia_lead_duplicado_recente()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM public.leads
        WHERE telefone = NEW.telefone
        AND mensagem = NEW.mensagem
        AND created_at > NOW() - INTERVAL '15 minutes'
    ) THEN
        RAISE EXCEPTION 'DUPLICIDADE BLOQUEADA: Este lead/mensagem foi inserido nos últimos 15 minutos.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger disparada ANTES do INSERT
DROP TRIGGER IF EXISTS trg_anti_spam_insert ON public.leads;
CREATE TRIGGER trg_anti_spam_insert
BEFORE INSERT ON public.leads
FOR EACH ROW
EXECUTE FUNCTION bloqueia_lead_duplicado_recente();
