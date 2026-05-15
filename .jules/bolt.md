## 2024-05-15 - FastAPI Performance Anti-pattern: Sync I/O in Async Routes
**Learning:** Routes performing synchronous I/O (like requests.post or calling synchronous SDK clients) must be defined with def rather than async def. If declared as async def, these synchronous operations completely halt the server's single-threaded event loop. Using def automatically offloads them to an external thread pool.
**Action:** Always check for sync I/O in FastAPI routes and use def instead of async def if they contain blocking calls.
