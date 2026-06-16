## 2025-03-01 - [O(N) Optimization in get_leads_summary]
**Learning:** Performing multiple iterations (O(4N)) over a large dataset retrieved from external sources like Supabase can cause a significant performance bottleneck. Memory states highlight this specifically.
**Action:** Always combine counting and grouping into a single-pass loop (O(N)) when dealing with list collections or large datasets fetched from APIs.
