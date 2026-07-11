🧹 [Extract shared n8n_request utility function]

🎯 **What:**
The codebase contained widespread duplication of the `n8n_request` function and `.env` parsing logic across numerous scripts (e.g., `disparar_agora.py`, `sync_master_nexus.py`, `scripts/deploy_aninha_atendimento.py`). This duplicated logic was extracted into a central, shared `n8n_utils.py` module containing `load_n8n_config` and `n8n_request`.

💡 **Why:**
Centralizing the API request logic significantly improves maintainability. Future changes to how the system communicates with n8n (e.g., adding retries, logging, or changing the SSL context) can now be implemented in a single place (`n8n_utils.py`) rather than being manually updated across 20+ distinct files. It also reduces the boilerplate at the top of every script.

✅ **Verification:**
- Syntactic and logical validation was performed across the refactored files to ensure global variables (`UPLOAD_DIR`, `REPORTS_DIR`, `WF_FILE`, etc.) were not accidentally removed.
- Handled subdirectory imports (e.g., `scripts/`) correctly by appending to `sys.path`.
- Supported optional `timeout` kwargs to prevent regressions in specific scripts that originally defined timeouts.
- Wrote and executed unit tests (`test_n8n_utils.py`) for the new utility functions which all pass.

✨ **Result:**
Removed hundreds of lines of duplicated boilerplate code across the repository. The n8n interaction logic is now modularized, tested, and easier to maintain globally.
