## 2026-06-07 - O(N) Loop Fusion in List Aggregation
**Learning:** The codebase previously contained multiple separate iterations over the same collection (`all_leads`) to compute different summary metrics (e.g., using `sum(1 for ...)` generators and subsequent `for` loops). This is an O(K*N) performance anti-pattern.
**Action:** Implemented O(N) loop fusion by consolidating the status counts and grouped counting into a single iteration pass, reducing the computational overhead and improving execution efficiency for large list operations.
