## 2024-07-20 - Derived State Opt for Real-Time Supabase Sync
**Learning:** In React components consuming real-time data from Supabase (e.g., via `postgres_changes`), manually synchronizing secondary `useState` hooks for derived metrics (like KPI aggregations) on every data fetch causes unnecessary re-renders and risks state desynchronization.
**Action:** Always calculate derived metrics using `useMemo` dependent on the primary dataset. This establishes a single source of truth and prevents redundant renders when the primary state updates.
