## 2024-06-25 - React Derived State Performance
**Learning:** In React components consuming real-time data, calculating derived metrics using `useMemo` dependent on the primary dataset instead of manually synchronizing a secondary `useState` prevents redundant re-renders and establishes a single source of truth.
**Action:** Always derive computable metrics directly from primary state using `useMemo` rather than maintaining redundant state objects, especially in real-time or high-frequency update scenarios.
