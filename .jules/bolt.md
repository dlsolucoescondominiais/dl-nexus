## 2024-05-24 - FastAPI Synchronous I/O in Async Routes
**Learning:** Defining routes with `async def` while executing synchronous I/O operations (like `requests.post` or calling synchronous OpenAI clients in AninhaAgent) completely blocks the server's single-threaded event loop, starving other requests.
**Action:** Always use standard `def` for FastAPI routes that perform synchronous network I/O or CPU-bound tasks without `await`. FastAPI automatically offloads `def` endpoints to an external thread pool.

## 2024-05-24 - Single-pass loop aggregation
**Learning:** Performing multiple generator expressions and loops over the same dataset (like `all_leads` in `stitch_integration.py`) leads to O(4N) complexity.
**Action:** Favor single-pass loops to perform multiple aggregations simultaneously over datasets.