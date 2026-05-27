## 2024-05-14 - O(N) Loop Fusion for leads summary
**Learning:** Found an inefficiency in `execution/stitch_integration.py` where iterating over lists of leads caused four O(N) operations. Combining iterative steps over a collection into a single pass is an important pattern to follow to prevent unnecessary calculations.
**Action:** When calculating multiple counts and groupings over the same list data structure, use loop fusion to calculate all metrics in a single O(N) pass.
