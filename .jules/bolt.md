## 2023-11-20 - Derived Metrics in Real-time React Components
**Learning:** In React components that consume real-time data (like Supabase websockets), maintaining a secondary `useState` for derived metrics (like KPIs) that is manually synchronized inside fetch effects causes unnecessary re-renders and potential state desynchronization.
**Action:** Always use `useMemo` to calculate derived metrics directly from the primary dataset state. This establishes a single source of truth and automatically prevents redundant component re-renders when the primary data updates.
