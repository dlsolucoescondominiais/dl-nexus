
## 2024-06-21 - FastAPI Threadpool Offloading for Sync IO
**Learning:** Route handlers performing synchronous, blocking I/O operations (like `requests.post()` or synchronous `openai` SDK calls) must be declared with standard `def` instead of `async def`. If declared as `async def`, they block the main event loop. Declaring them as `def` allows FastAPI to automatically offload execution to an external threadpool.
**Action:** Always verify if a FastAPI route contains blocking I/O. If it does and isn't using async libraries, drop the `async` keyword to leverage FastAPI's built-in threadpool optimization.
