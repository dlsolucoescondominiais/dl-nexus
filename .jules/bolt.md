## 2025-05-12 - Synchronous I/O in FastAPI Async Routes
**Learning:** Defining FastAPI routes with `async def` when the body of the function performs synchronous I/O operations (like `requests.post` or using synchronous clients like OpenAI without async versions) will completely block the single-threaded event loop of the server, destroying concurrency and performance.
**Action:** Always use `def` (instead of `async def`) for route handlers that execute synchronous I/O. FastAPI will automatically offload these routes to an external thread pool, preserving the event loop's responsiveness.
