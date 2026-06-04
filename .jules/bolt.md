## 2026-06-04 - [FastAPI Route Handlers with Blocking I/O]
**Learning:** In FastAPI, declaring route handlers with `async def` that perform synchronous, blocking I/O operations (like `requests.post()` or synchronous `openai` SDK calls) blocks the main event loop and degrades performance.
**Action:** Always declare route handlers performing blocking I/O with standard `def`. This allows FastAPI to automatically offload execution to an external threadpool, preventing the main event loop from being blocked.
