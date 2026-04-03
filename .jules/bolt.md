## 2025-05-18 - [Google Drive N+1 API Calls Cache]
**Learning:** During batch processing of files via Google Drive API, repeated existence checks for parent and child folders using `service.files().list(q="name='...' and ...").execute()` lead to significant N+1 query bottlenecks and potential rate-limiting.
**Action:** Implement an in-memory dictionary cache (e.g. `_folder_id_cache = {}`) keyed by `(parent_id, folder_name)` within functions like `obter_ou_criar_pasta` to short-circuit redundant network queries and drastically improve performance.
