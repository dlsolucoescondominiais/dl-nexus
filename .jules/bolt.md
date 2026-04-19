## 2026-04-19 - [React Array Aggregation Optimization]
**Learning:** In React components (like the Dashboard), calculating multiple metrics by chaining `filter().length` operations over an array creates an N+1 traversal problem in the client's memory. Even worse, if the array is large, this blocks the main thread during render.
**Action:** Always favor a single `reduce` pass over arrays to calculate multiple metrics simultaneously in O(N) time instead of executing multiple separate O(N) `filter().length` operations, especially when hydrating dashboards from Supabase/Realtime.
