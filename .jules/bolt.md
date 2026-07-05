## 2024-05-18 - [Loop Fusion Optimization in Python]
**Learning:** Found an anti-pattern of using multiple `sum(1 for ...)` generators or multiple `for` loops to compute various metrics over the same dataset. This results in O(K*N) performance, traversing a potentially large list multiple times.
**Action:** Consolidate these iterative aggregation passes into a single loop pass (loop fusion). This turns O(K*N) into O(N), vastly improving performance and removing redundant list traversals.
