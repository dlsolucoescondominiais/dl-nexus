## 2024-05-24 - FastAPI Sync Blocking Anti-Pattern
**Learning:** Using `async def` in FastAPI route handlers that execute synchronous, blocking I/O (like `requests.post` or synchronous OpenAI SDK calls) will stall the main event loop. This leads to severe performance degradation as concurrent requests cannot be processed.
**Action:** Always use standard `def` for route handlers that perform blocking I/O operations, allowing FastAPI to automatically offload execution to an external threadpool.
