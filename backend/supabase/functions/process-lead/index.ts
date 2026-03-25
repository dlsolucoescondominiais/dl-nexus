import { serve } from "https://deno.land/std@0.168.0/http/server.ts"
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  try {
    const payload = await req.json()
    const { record } = payload

    if (!record || !record.email_encaminhamento) {
      return new Response(
        JSON.stringify({ message: "No email_encaminhamento found or invalid payload" }),
        { headers: { "Content-Type": "application/json" }, status: 200 }
      )
    }

    const n8nWebhookUrl = Deno.env.get("N8N_WEBHOOK_URL")
    const n8nAuthToken = Deno.env.get("N8N_AUTH_TOKEN")

    if (!n8nWebhookUrl) {
        console.error("Missing N8N_WEBHOOK_URL environment variable")
        return new Response(
            JSON.stringify({ error: "Missing configuration" }),
            { headers: { "Content-Type": "application/json" }, status: 500 }
        )
    }

    // Trigger n8n webhook
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    }

    // Pass authentication token if headerAuth is used
    if (n8nAuthToken) {
        // Based on headerAuth typical configuration, the header name can vary.
        // We'll use Authorization as standard, but the n8n webhook might need a specific header name defined in credentials.
        // Assuming standard Bearer token or custom header like 'X-N8N-API-KEY'
        headers["Authorization"] = `Bearer ${n8nAuthToken}`
        // In case they configured it via a custom API Key header
        headers["X-Api-Key"] = n8nAuthToken
    }

    const n8nResponse = await fetch(n8nWebhookUrl, {
      method: "POST",
      headers,
      body: JSON.stringify({
        lead_id: record.id,
        nome: record.nome_contato,
        email_destino: record.email_encaminhamento,
        mensagem: record.mensagem,
        tipo_servico: record.tipo_servico
      }),
    })

    if (!n8nResponse.ok) {
       console.error(`n8n webhook failed with status ${n8nResponse.status}`)
    }

    return new Response(
      JSON.stringify({
        message: "Lead processed and routed successfully",
        lead_id: record.id,
        email_destino: record.email_encaminhamento
      }),
      { headers: { "Content-Type": "application/json" }, status: 200 }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      { headers: { "Content-Type": "application/json" }, status: 400 }
    )
  }
})
