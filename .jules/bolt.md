# Learnings
- When updating N8N webhooks to use `headerAuth`, ensure that any calling services (like Supabase Edge Functions) also include the corresponding auth headers (e.g., `Authorization: Bearer <token>`).
- Always check that temporary automation scripts created during replanning or step execution (like `patch_webhooks.py`) are deleted before finalizing the changes.
- In Python projects utilizing `google.genai` where the API key is retrieved via `.env`, ensure tests are mocked using `unittest.mock.patch` to avoid relying on actual API keys.
