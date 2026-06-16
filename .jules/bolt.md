## 2024-05-19 - Single-Pass Loop Optimization in Data Aggregation
**Learning:** Found multiple iterations over `all_leads` in `get_leads_summary` to tally up statuses and group by categories. This is an O(4N) algorithmic complexity that can be easily reduced to an O(N) single-pass iteration.
**Action:** Replace multiple O(N) generator comprehensions and separate loops with a single unified loop whenever doing multi-dimensional data aggregation in Python backends.
