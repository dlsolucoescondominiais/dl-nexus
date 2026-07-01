## 2026-07-01 - Webhook Authentication Security

**Learning:** When developing API endpoints (like webhooks for n8n) that rely on environment variables for authentication (`process.env.N8N_WEBHOOK_SECRET`), falling back to a hardcoded string if the environment variable is missing creates a functional authentication bypass in production.

**Action:** Always strictly validate the presence of the environment variable. If it's missing, log a critical configuration error and return a 500 Internal Server Error, ensuring the endpoint fails closed rather than failing open with a default hardcoded secret.
