## 2024-06-25 - Avoid Multiple O(N) Passes for Aggregation
**Learning:** In Python, performing multiple list comprehensions or loops over the same dataset to aggregate different metrics (e.g., counting statuses and grouping by categories) results in O(k*N) complexity. For large datasets, this becomes a bottleneck.
**Action:** Combine multiple aggregations into a single pass (O(N)) using a single loop, especially when iterating over large lists like records from a database.
