
## 2024-05-19 - FastAPI Synchronous I/O Blocking Event Loop
**Learning:** In FastAPI, declaring a route with `async def` and then performing synchronous I/O operations (like using `requests.post` or calling synchronous SDKs like `openai.chat.completions.create`) will completely block the main event loop, severely degrading performance and throughput.
**Action:** Always verify if external HTTP calls or heavy computations are synchronous. If you cannot use an async client (like `httpx.AsyncClient`) due to missing dependencies, declare the route with `def` instead of `async def`. FastAPI will automatically offload the synchronous execution to an external thread pool, preserving the event loop's responsiveness.
