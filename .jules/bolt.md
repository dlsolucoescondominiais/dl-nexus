## 2025-05-18 - [In-Memory Folder ID Cache for Drive API]
**Learning:** In Google Drive API automation scripts like `agente_zelador.py` and `agente_arquivista.py`, repeatedly querying for folder existence via `obter_ou_criar_pasta` causes a severe N+1 query problem, hitting rate limits and massively degrading performance during batch processing.
**Action:** Implemented a global in-memory dictionary cache `_folder_id_cache` keyed by `(parent_id, folder_name)` inside the `obter_ou_criar_pasta` function to instantly resolve known folder IDs and skip redundant network calls.
