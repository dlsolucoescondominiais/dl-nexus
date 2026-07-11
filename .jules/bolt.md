## 2024-05-18 - Fix hardcoded N8N API Keys

**Learning:** Hardcoded API keys pose a severe security risk and were found in `import_091_092_n8n.py` and `import_social_media_n8n.py`. Additionally, the file `.env` was being manually parsed in `deploy_all_workflows.py`, which is generally discouraged in favor of `os.getenv` or `python-dotenv`.

**Action:** Replaced hardcoded JWT keys with `os.getenv("N8N_API_KEY", "")` and implemented a safe fallback checking `os.getenv()` before falling back to manual `.env` file parsing in `deploy_all_workflows.py`.
