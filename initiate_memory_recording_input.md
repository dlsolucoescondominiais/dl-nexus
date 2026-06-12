# Learnings from N8N Workflow Testing and Validation
- When testing n8n `telegramTrigger` nodes locally, standard HTTP requests will fail with 404 (or bypass the trigger node logic) because the webhook expects standard Telegram-formatted payloads or operates on polling. To test the downstream logic fully, it's safer to temporarily inject an HTTP webhook (`n8n-nodes-base.webhook`) node connected to the entry normalization node, or run tests directly against the downstream webhook in `002`.
- Supabase table existence can be cleanly verified using the REST API by passing the `apikey` and `Authorization: Bearer` headers with `limit=1` to check for `HTTP 200`.
- Always verify that no temporary test Python scripts containing API keys (like `N8N_API_KEY`) are tracked or staged before committing.
