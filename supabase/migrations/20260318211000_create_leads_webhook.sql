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
  -- Replace 'process-lead' with your actual function name if it differs
  PERFORM net.http_post(
      url := current_setting('custom.edge_function_url', true) || '/process-lead',
      headers := jsonb_build_object(
          'Content-Type', 'application/json',
          'Authorization', 'Bearer ' || current_setting('custom.edge_function_anon_key', true)
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
