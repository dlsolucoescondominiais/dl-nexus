## 2024-07-17 - [Optimize React Derived State with useMemo]
**Learning:** [In React components consuming real-time data, avoid synchronizing a secondary state for derived metrics. This causes double re-renders. A single loop inside useMemo reduces redundant recalculations and establishes a single source of truth.]
**Action:** [Use useMemo dependent on the primary dataset to calculate derived metrics directly instead of maintaining a secondary useState.]
