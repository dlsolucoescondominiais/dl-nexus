## 2024-04-10 - [React Frontend] Array Aggregation Bottlenecks
**Learning:** React components (like Dashboard.tsx) calculating multiple KPIs from a single data source often mistakenly use multiple `filter().length` passes, leading to O(kN) time complexity and redundant intermediate array allocations which causes memory pressure during re-renders.
**Action:** Always replace multiple `filter().length` or chained map/filter operations with a single-pass `reduce()` when deriving multiple summary metrics (KPIs) from the same list of objects.
