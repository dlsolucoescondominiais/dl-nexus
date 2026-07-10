## 2024-06-11 - [Dashboard Performance]
**Learning:** In real-time dashboards where derived metrics (KPIs) are driven from a primary dataset like `leads` (frequently updated via Supabase Realtime), storing derived metrics in a secondary `useState` and updating it via `.filter().length` chains creates redundant re-renders and O(N*M) iteration overhead.
**Action:** Always compute derived state in real-time consuming React components using `useMemo` with O(N) loop fusion to establish a single source of truth without manual state synchronization.
