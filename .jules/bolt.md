## 2024-05-02 - [Replace Blocking Requests with httpx in FastAPI]
 **Learning:** Using synchronous `requests.post` inside an `async def` FastAPI route completely blocks the asyncio event loop for the duration of the request, causing severe latency for concurrent background tasks.
 **Action:** Always use `httpx.AsyncClient` inside `async with` for HTTP requests within `async def` routes to maintain event loop responsiveness.
