## 2024-05-24 - O(N) loop fusion for computing multiple metrics

**Learning:** It's common to compute multiple summary statistics or metrics over a single collection (like calculating 'novos', 'triados', 'por_servico', and 'por_porte' over a list of leads). Writing multiple separate list comprehensions or loops (e.g., using `sum(1 for ...)` or generator expressions) results in traversing the data multiple times, which scales poorly (O(K*N) where K is the number of metrics).

**Action:** Consolidate multiple aggregation passes into a single O(N) loop traversal whenever computing multiple metrics on the same dataset. Keep track of metrics using simple counters and dictionaries populated in a single pass.
