## 2026-06-16 - [Fix Blocking Async FastAPI Routes]
**Learning:** I discovered that synchronous blocking operations (like `requests.post` and synchronous OpenAI calls) inside FastAPI `async def` route handlers block the main event loop, causing severe performance bottlenecks under load.
**Action:** I will replace `async def` with standard `def` for these specific route handlers so FastAPI automatically offloads them to an external threadpool.
