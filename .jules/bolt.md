## 2024-05-04 - Optimize List Aggregation Performance

**Learning:** Python iterations with list comprehensions and generators for aggregation functions (e.g. `sum(1 for x in xs)`, `len(xs)`, etc.) when done sequentially add up to multiple complete passes over a potentially large dataset. The `get_leads_summary` function inside `execution/stitch_integration.py` iterated the data four distinct times to calculate total length, filter based on 'novo', filter based on 'triado', group by service, and group by size. This created O(4N) complexity, adding redundant processing when manipulating arrays retrieved from APIs.

**Action:** Consolidate multiple iterative aggregations and filters over a dataset into a single-pass `for` loop iteration (O(N)). Although list comprehensions and generator functions might appear cleaner, when a dataset must be filtered or grouped by multiple different criteria, a single `for` loop with tallying variables performs better.
