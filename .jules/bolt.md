## 2026-03-29 - [Google Drive In-Memory Caching]
**Learning:** The Google Drive API was queried redundantly in a tight loop to check for the existence of the same folder structures for every file processed, hitting rate limits and consuming high IO/Network latency.
**Action:** Use an in-memory dictionary cache globally populated during script execution to store fetched or created 'folder_id's based on unique keys like '{parent_id}_{folder_name}' to intercept API calls.
