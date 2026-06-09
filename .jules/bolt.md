## 2024-06-09 - [FastAPI Async Def Blocking Event Loop]
**Learning:** In FastAPI, synchronous blocking I/O (like `requests.post()` or synchronous `openai` SDK calls) inside an `async def` route handler blocks the main event loop, severely degrading performance under load.
**Action:** Declare route handlers that perform synchronous I/O with standard `def` instead of `async def` so FastAPI automatically offloads execution to an external threadpool.
