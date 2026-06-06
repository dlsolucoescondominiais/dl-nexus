
## 2024-05-18 - Consolidate Multiple Iterative Aggregation Passes (O(N) Loop Fusion)
**Learning:** In codeblocks dealing with aggregations of lists, using multiple inline generator comprehensions like `sum(1 for l in all_leads if condition)` causes redundant full traversals of the list. In `execution/stitch_integration.py`'s `get_leads_summary` method, `all_leads` was being iterated through four separate times to compute simple sums and counts.
**Action:** Use O(N) loop fusion by grouping multiple metric updates (status counts, categorizations) into a single overarching `for` loop pass. This avoids O(k * N) time complexity where k is the number of distinct metrics you're calculating.
