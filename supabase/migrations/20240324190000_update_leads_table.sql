-- Create the pg_net extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_net;

CREATE TABLE IF NOT EXISTS leads (
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

-- Drop the trigger if it exists
DROP TRIGGER IF EXISTS trigger_new_lead ON leads;

-- Drop the function if it exists
DROP FUNCTION IF EXISTS public.handle_new_lead();

-- Create the webhook function
CREATE OR REPLACE FUNCTION public.handle_new_lead()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
  -- We call the Supabase Edge Function directly using the native HTTP extension
  -- Using a more robust COALESCE to fallback to the known URL if custom settings fail
  PERFORM net.http_post(
      url := COALESCE(
          current_setting('custom.edge_function_url', true),
          'https://nejdtvkpiclagsnfljsz.supabase.co/functions/v1'
      ) || '/process-lead',
      headers := jsonb_build_object(
          'Content-Type', 'application/json',
          'Authorization', 'Bearer ' || current_setting('app.settings.anon_key', true)
      ),
      body := jsonb_build_object(
          'type', TG_OP,
          'table', TG_TABLE_NAME,
          'schema', TG_TABLE_SCHEMA,
          'record', row_to_json(NEW),
          'old_record', row_to_json(OLD)
      )
  );

  RETURN NEW;
END;
$$;

-- Create the trigger
CREATE TRIGGER trigger_new_lead
AFTER INSERT ON leads
FOR EACH ROW
EXECUTE FUNCTION public.handle_new_lead();
