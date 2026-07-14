## 2024-05-14 - Playwright Vite Routing
**Learning:** When using Playwright to test a local Vite React application, relying on `file:///path/to/dist/index.html` often fails with `net::ERR_FILE_NOT_FOUND` or blank screens because asset paths and client-side routing (React Router) expect an HTTP server context.
**Action:** Always start the dev server (`npm run dev`) on a background process and explicitly navigate Playwright to the correct HTTP route (e.g., `http://localhost:5174/dashboard-tecnico`), avoiding root paths if they trigger redirects.
