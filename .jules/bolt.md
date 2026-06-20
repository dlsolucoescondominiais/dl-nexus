
## 2024-05-18 - [Optimize Stitch deployment API calls]
**Learning:** Sequential, synchronous API calls bound by `time.sleep()` rate-limits cause massive performance bottlenecks. When rate limits allow, I/O bound operations should be parallelized.
**Action:** Replaced the sequential for loop and `time.sleep(10)` rate limiting in `execution/deploy_site_stitch.py` with `concurrent.futures.ThreadPoolExecutor(max_workers=5)` to perform API requests concurrently. This eliminates the sleep delay and reduces the script's execution time linearly based on the number of workers, transforming 4.9s mockup wait times to 0.1s.
