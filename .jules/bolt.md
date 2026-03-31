## 2024-05-24 - [Google Drive API Lookup Cache]
**Learning:** Checking for folder existence inside loops without a cache causes N+1 problems with Google Drive API (`list()`), resulting in rate limiting or severe performance degradation.
**Action:** Implemented an in-memory dictionary cache `_folder_id_cache` keyed by `(parent_id, folder_name)` in `obter_ou_criar_pasta` to eliminate redundant network calls and improve speed.
