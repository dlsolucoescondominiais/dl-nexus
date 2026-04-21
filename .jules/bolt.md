## 2026-04-21 - [FastAPI Middleware for Compliance]
**Learning:** Intercepting and modifying JSON response bodies in FastAPI to enforce strict business compliance rules (e.g., swapping specific terms or blocking content) is effectively achieved using `Starlette`'s `BaseHTTPMiddleware` and iterating over the response body stream.
**Action:** Use this pattern whenever you need to centrally enforce output rules without touching individual agent prompt definitions.
