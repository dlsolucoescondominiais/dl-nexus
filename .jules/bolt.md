## 2024-07-24 - Derived State in Real-Time Supabase Consumers
**Learning:** In React components consuming real-time data via Supabase websockets (like `Dashboard.tsx`), maintaining secondary state (e.g., `kpis`) synchronized via `useState` inside the subscription callback or fetch effect causes redundant re-renders and risks state divergence.
**Action:** Always calculate derived metrics using `useMemo` dependent on the primary dataset. This establishes a single source of truth and eliminates extra render cycles per websocket update.
