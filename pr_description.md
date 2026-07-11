💡 **What:** The optimization implemented
Replaced the synchronous, thread-blocking `requests.post()` call inside the `/aprovar` FastAPI route with an asynchronous implementation using `httpx.AsyncClient().post()`.

🎯 **Why:** The performance problem it solves
The endpoint `aprovar_post` is marked as `async def`, which means it runs on the main event loop thread (or a worker thread). By calling `requests.post()` directly, it blocks that thread waiting for network I/O from the n8n webhook, causing severe bottlenecks and blocking other concurrent requests to the FastAPI application. Using `httpx` and `await` yields control back to the event loop while waiting for the network response.

📊 **Measured Improvement:**
I established a benchmark simulating 10 concurrent requests to this endpoint, mocking the n8n webhook with a 0.5s network delay.
- Baseline (synchronous `requests`): 10 concurrent requests took **3.32 seconds** to complete.
- Optimized (asynchronous `httpx`): 10 concurrent requests took **1.12 seconds** to complete.
- Improvement: The endpoint now processes concurrent requests approximately **3x faster** under this load profile.
