## 2024-05-14 - [Drive API Rate Limit Mitigation]
**Learning:** The Python scripts interacting with Google Drive API (`agente_zelador.py`, etc) can hit rate limits by repeatedly querying for folder existence via `obter_ou_criar_pasta()`.
**Action:** Implement an in-memory dictionary cache to store folder IDs by their `parent_id` and `nome_pasta` to prevent redundant network calls when processing multiple files.
