## 2024-07-18 - Derived State Performance Pattern with useMemo
**Learning:** In React components consuming real-time data (like Supabase websockets), maintaining a secondary `useState` for derived metrics (e.g., KPIs derived from a list of leads) creates redundant re-renders and risks state synchronization bugs.
**Action:** Always calculate derived metrics using `useMemo` dependent on the primary dataset. This establishes a single source of truth and prevents unnecessary re-renders when the primary data updates.
