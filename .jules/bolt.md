## 2026-07-21 - Derived State Performance in Real-Time Dashboards
**Learning:** In React components consuming real-time data via websockets (like Supabase channels), manually synchronizing secondary state variables (`setKpis` based on `leads`) causes redundant render cycles and visual stuttering during rapid updates.
**Action:** Always use `useMemo` to calculate derived metrics directly from the primary dataset dependency. This establishes a single source of truth and prevents unnecessary re-renders when data streams in quickly.
