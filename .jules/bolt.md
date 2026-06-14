## 2024-06-14 - FastAPI Sync vs Async Route Anti-Pattern
**Learning:** Using `async def` for FastAPI routes that perform blocking synchronous operations (like `requests.post()` or synchronous `openai` SDK calls) blocks the main event loop, severely degrading performance.
**Action:** Always declare FastAPI routes with standard `def` instead of `async def` when they contain synchronous, blocking I/O operations. This allows FastAPI to automatically offload the execution to an external threadpool.
