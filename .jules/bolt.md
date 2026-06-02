## 2026-06-02 - O(N) Loop Fusion for Aggregations
**Learning:** Found an anti-pattern in `get_leads_summary` where multiple `sum(1 for ...)` generators and `for` loops were used to iterate over the same dataset (`all_leads`) multiple times to calculate different metrics (`novos`, `triados`, `servicos`, `portes`). This caused unnecessary O(4N) complexity overhead.
**Action:** Replaced multiple loop passes with a single O(N) loop to compute all metrics simultaneously, reducing iteration overhead and improving execution speed for large datasets.
