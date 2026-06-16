## 2024-04-15 - React Reduce vs Filter length Array Optimization
**Learning:** In React components aggregating large metrics (like dashboards), multiple chained `array.filter(condition).length` operations create hidden O(3N) bottlenecks and allocate multiple intermediate arrays.
**Action:** Always combine multi-metric aggregations into a single `array.reduce()` pass to maintain O(N) complexity and prevent memory thrashing. Ensure fallback initialization objects are provided to safely handle undefined arrays.
