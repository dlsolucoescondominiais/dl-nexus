## 2024-06-26 - [O(N) Loop Fusion for Dashboard KPIs]
**Learning:** Multiple array traversals using `.filter().length` (like computing counts for `negociacao`, `fechado_ganho`, and `contrato_recorrente` separately) create an O(M*N) bottleneck. This is inefficient as the collection size grows.
**Action:** Replace sequential `.filter().length` aggregations with a single O(N) loop that calculates all required metrics in one pass over the array. This is documented in memory as the "Loop Fusion" pattern.
