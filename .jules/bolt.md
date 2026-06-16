
## 2024-05-18 - FastAPI Sync I/O blocking
**Learning:** Sync I/O in async FastAPI routes blocks the event loop.
**Action:** Change async def to def for routes with sync I/O.
