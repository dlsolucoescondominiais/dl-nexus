## 2024-XX-XX - In-memory cache for Google Drive API folder lookups
**Learning:** When querying the Google Drive API repeatedly for folder existence, an in-memory dictionary cache prevents redundant network calls and rate limiting.
**Action:** Use a global dictionary to store folder IDs by name/parent to avoid redundant API requests during loop iterations.
