## 2026-04-16 - Single-pass loop optimization in React KPIs
**Learning:** React component data aggregations frequently use multiple `filter().length` arrays which causes O(N*M) passes over the state data when calculating KPIs. Combining these into a single `reduce()` pass provides immediate CPU relief during render/data loading phases, particularly when processing large Supabase realtime payloads.
**Action:** Always scan for consecutive `.filter()` operations on the same data array and refactor them into a single `.reduce()` that tallies all required metrics simultaneously.
