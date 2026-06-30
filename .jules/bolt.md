## YYYY-MM-DD - [Title]
**Learning:** [Insight]
**Action:** [How to apply next time]
## 2024-06-30 - O(N) Loop Fusion for KPIs
**Learning:** In React components like `Dashboard.tsx`, computing multiple metrics (like KPIs) using separate `.filter().length` calls results in redundant array traversals (O(3N) instead of O(N)). This is an anti-pattern when working with large datasets, especially real-time metrics.
**Action:** Consolidate multiple iterative aggregation passes into a single loop pass (O(N) loop fusion) using `reduce` when computing multiple metrics on the same collection.
