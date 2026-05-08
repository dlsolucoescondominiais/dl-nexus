
## 2026-05-08 - [Aninha Lead Processing Workflow]
 **Learning:** When doing synchronous I/O operations with external APIs (like OpenAI and Supabase) inside a FastAPI route, declaring the route as `def` instead of `async def` offloads the operations to an external thread pool, preventing blocking of the main event loop.
 **Action:** Ensure any route hitting synchronous clients (e.g. `openai.chat.completions.create` or standard `requests`) is declared as `def` unless async clients like `httpx` or `async_openai` are used.
