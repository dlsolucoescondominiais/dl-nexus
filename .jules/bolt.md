## 2024-06-18 - Loop Fusion Optimization in Leads Summary
**Learning:** Avoid using multiple list comprehensions or generators (`sum(1 for ...)`) and multiple iteration loops over the same large dataset (e.g. leads). This results in O(k*N) complexity.
**Action:** Consolidate multiple iterative aggregation passes into a single loop pass (O(N) loop fusion) when computing multiple metrics on the same collection.
