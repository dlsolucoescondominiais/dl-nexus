## 2025-03-09 - Python Single-Pass Iteration for Data Sets
**Learning:** Multiple generator expressions or comprehensions over the same collection cause redundant N+1 iteration overhead.
**Action:** Always prefer a single `for` loop that performs multiple aggregations at once to reduce O(N) operations.
