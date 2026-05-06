## 2024-05-06 - FastAPI Event Loop Starvation with Sync I/O
**Learning:** Routes performing synchronous I/O (like `requests.post` or synchronous SDK clients like OpenAI) completely halt the single-threaded event loop if defined with `async def`. This is a massive bottleneck.
**Action:** Always define routes that perform synchronous I/O with `def` rather than `async def`. FastAPI will automatically offload them to an external thread pool, preventing event loop starvation.
