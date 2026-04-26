## 2024-04-26 - Single-pass Data Aggregation O(N) Loop
**Learning:** Found multiple iterations on data sets using generator expressions combined with loops causing unnecessary O(N*4) time complexity in SupabaseClient.get_leads_summary.
**Action:** Consolidate multiple aggregations into a single-pass O(N) loop to drastically reduce looping overhead and improve API responsiveness during scale up.
