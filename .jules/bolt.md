## 2026-04-26 - [FastAPI Event Loop Starvation]
 **Learning:** In FastAPI, placing synchronous blocking I/O (like `requests.post`) inside an `async def` route starves the main event loop, significantly degrading concurrent performance.
 **Action:** To resolve this, simply convert `async def` to `def` for routes that must do blocking synchronous calls, which tells FastAPI to automatically offload them to an external thread pool. Avoid using `async def` unless using true async I/O libraries like `httpx` or using `run_in_threadpool` manually.
