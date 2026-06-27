## 2026-06-27 - O(N) Loop Fusion
**Learning:** Found an anti-pattern in the frontend where multiple `.filter(condition).length` passes were used sequentially to count different states in the same array. This causes unnecessary O(N * M) traversal where M is the number of filters.
**Action:** Always prefer O(N) loop fusion (a single `.forEach` or `for` loop) to count multiple metrics simultaneously over a dataset, reducing redundant loop overhead.
