## 2024-05-18 - [FastAPI Async Def Performance Anti-Pattern]
**Learning:** Defining routes that perform synchronous I/O (like `requests.post` or synchronous SDK clients) with `async def` halts the server's single-threaded event loop in FastAPI.
**Action:** Always use `def` instead of `async def` for routes that perform synchronous network I/O, so FastAPI offloads them to an external thread pool.
