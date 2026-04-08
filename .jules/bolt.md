## 2024-05-18 - [Optimize Multiple Array Iterations]
**Learning:** Calling `filter().length` multiple times on an array creates hidden bottlenecks in React component renders. It causes N passes over the data array.
**Action:** Consolidate multiple `filter().length` aggregations into a single pass using `Array.prototype.reduce()` to tally metrics simultaneously and reduce O(N) operations.
