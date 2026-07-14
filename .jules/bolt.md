## 2024-05-24 - FastAPI Synchronous Operations
**Learning:** FastAPI route handlers performing synchronous, blocking I/O operations (like `requests.post()` or synchronous `openai` SDK calls) must be declared with standard `def` instead of `async def`. This allows FastAPI to automatically offload execution to an external threadpool, preventing the main event loop from being blocked.
**Action:** Always check network calls in FastAPI endpoints. If using `requests` or synchronous SDKs, use `def`.
