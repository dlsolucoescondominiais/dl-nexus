## 2024-05-24 - Frontend Dashboard KPI Optimization
**Learning:** `cat` outputs for source files can be truncated around 1000 characters, leading to dangerous assumptions about code structure. Attempting to plan modifications based on truncated memory without verifying the exact lines using `grep` or paginated tools violates groundedness.
**Action:** When using `read_file` or `cat` to analyze code, always verify the file size first, and rely on targeted `grep` with context lines (e.g., `grep -n -A 15 -B 5`) to reliably read and patch specific logic sections before forming an execution plan.
