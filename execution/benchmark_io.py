import asyncio
import time

async def simulate_network_request(duration=0.05):
    """Simulates a network request like a Google Drive API call."""
    await asyncio.sleep(duration)

async def run_sequential(num_requests=100):
    start_time = time.time()
    for _ in range(num_requests):
        await simulate_network_request()
    end_time = time.time()
    return end_time - start_time

async def run_batched(num_requests=100, batch_size=100):
    # Simulating batching where one request is sent that takes slightly longer
    # but does the work of 'batch_size' individual requests.
    start_time = time.time()
    num_batches = (num_requests + batch_size - 1) // batch_size
    for _ in range(num_batches):
        # A batched request might take a bit longer than a single one
        await simulate_network_request(0.1)
    end_time = time.time()
    return end_time - start_time

async def main():
    num_requests = 100
    print(f"Simulating {num_requests} API requests...")

    seq_time = await run_sequential(num_requests)
    print(f"Sequential Time: {seq_time:.2f}s")

    batch_time = await run_batched(num_requests)
    print(f"Batched Time: {batch_time:.2f}s")

    improvement = ((seq_time - batch_time) / seq_time) * 100
    print(f"Improvement: {improvement:.2f}%")

if __name__ == '__main__':
    asyncio.run(main())
