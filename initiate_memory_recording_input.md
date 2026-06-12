# Learnings from N8N Workflow Synchronization and Deployment

## Technical Lessons
- When working with n8n workflows across environments, it is crucial to first verify if the local files match the active production versions via API (`GET /workflows`). In this case, the local files in `backend/n8n/workflows` were outdated versions compared to the active ones in the cloud.
- To safely deploy back a workflow via API (`PUT /workflows/{id}`), it's important to strip read-only metadata fields (`id`, `createdAt`, `updatedAt`, `meta`, `pinData`, `versionId`, `triggerCount`, `workflowPublishHistory`, `authors`, `tags`, etc.) and send only allowed keys (`name`, `nodes`, `connections`, `settings`, `staticData`).
- When parsing JSON from LLMs in n8n `Code` nodes, standardizing robust fallbacks (e.g., catching parse errors and validating required keys like `resposta_cliente`) is critical to prevent pipeline crashes.

## Repository Knowledge
- `deploy_telegram_bot.py` uses `ssl.CERT_NONE` locally because of self-signed or Cloudflare proxy certificates on `n8n.dlsolucoescondominiais.com.br`. This is a technical risk to track.
- For secure repository commits, always `sed` or redact API keys (like Google Gemini and Supabase JWT tokens) that are stored inside exported n8n workflow `.json` files.
