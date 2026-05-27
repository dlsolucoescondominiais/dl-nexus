## 2024-04-28 - Optimizing React Array Reductions
**Learning:** When aggregating multiple metrics from an array in React components, using multiple `.filter().length` calls iterates over the entire array multiple times (O(N*M) where M is the number of filters).
**Action:** Always use a single `.reduce()` pass over the array with a fallback initialization object to calculate multiple metrics simultaneously in O(N) time. Ensure fallbacks handle undefined arrays cleanly like `(data || []).reduce(...)`.
