## 2024-07-10 - Dashboard Real-time Derived State KPI Optimization

**Learning:** When using Supabase real-time subscriptions, manually synchronizing a secondary derived state (`setKpis`) based on the primary fetched data (`leads`) creates an unnecessary render cycle. It also creates a race condition where the UI briefly renders with stale derived data if the state updates don't hit the render tree exactly simultaneously. This is a common performance anti-pattern in React apps consuming websockets/real-time streams.

**Action:** Always use `useMemo` for any UI metric, count, or calculation that can be derived deterministically from the primary dataset (`leads`). This creates a single source of truth and completely eliminates the redundant re-render triggered by the secondary `setState`.
