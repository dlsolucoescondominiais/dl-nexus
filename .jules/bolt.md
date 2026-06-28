## 2024-06-28 - FastAPI Synchronous I/O Offloading
**Learning:** In FastAPI, declaring an endpoint handler with `async def` when it performs synchronous, blocking I/O operations (like `requests.post()` or synchronous `openai` SDK calls) blocks the main asyncio event loop, severely impacting concurrent performance.
**Action:** When a FastAPI route handler must perform synchronous blocking I/O, declare it with standard `def` instead of `async def`. This instructs FastAPI to automatically offload the execution to an external threadpool, preserving the main thread for concurrent requests.
