import asyncio
import time
import sys
import os

# Import all our fetchers
sys.path.append('scripts')
from async_url_fetcher import AsyncUrlFetcher
from threaded_url_fetcher import ThreadedUrlFetcher
from hybrid_async_threaded_fetcher import HybridAsyncThreadedFetcher
from multiprocess_url_fetcher import MultiprocessUrlFetcher

async def run_performance_comparison():
    """Compare all different approaches for URL fetching"""
    
    # Generate sample URLs first
    print("Generating sample URLs for testing...")
    fetcher_instance = AsyncUrlFetcher() # Use one instance to generate URLs
    sample_urls = fetcher_instance.generate_sample_urls(200) # Generate 200 test URLs
    
    results = {}
    
    print("\n" + "="*60)
    print("URL FETCHING PERFORMANCE COMPARISON")
    print("="*60)
    
    # Test 1: Original Async Approach
    print("\n1. Testing Async URL Fetching Approach...")
    start_time = time.time()
    async_fetcher = AsyncUrlFetcher(max_concurrent_requests=50)
    await async_fetcher.fetch_urls_from_list(sample_urls)
    async_time = time.time() - start_time
    results['Async'] = async_time
    
    # Test 2: Pure Threading
    print("\n2. Testing Pure Threading URL Fetching Approach...")
    start_time = time.time()
    threaded_fetcher = ThreadedUrlFetcher(max_workers=8)
    threaded_fetcher.fetch_urls_threaded(sample_urls)
    threaded_time = time.time() - start_time
    results['Threading'] = threaded_time
    
    # Test 3: Hybrid Async + Threading
    print("\n3. Testing Hybrid Async + Threading URL Fetching...")
    start_time = time.time()
    hybrid_fetcher = HybridAsyncThreadedFetcher(max_async_workers=30, max_thread_workers=4)
    await hybrid_fetcher.fetch_urls_hybrid(sample_urls)
    hybrid_time = time.time() - start_time
    results['Hybrid'] = hybrid_time
    
    # Test 4: Multiprocessing
    print("\n4. Testing Multiprocessing URL Fetching Approach...")
    start_time = time.time()
    multiprocess_fetcher = MultiprocessUrlFetcher(max_processes=4)
    multiprocess_fetcher.fetch_urls_multiprocess(sample_urls)
    multiprocess_time = time.time() - start_time
    results['Multiprocessing'] = multiprocess_time
    
    # Display results
    print("\n" + "="*60)
    print("PERFORMANCE RESULTS")
    print("="*60)
    
    sorted_results = sorted(results.items(), key=lambda x: x[1])
    
    for i, (method, time_taken) in enumerate(sorted_results, 1):
        speedup = results['Async'] / time_taken if time_taken > 0 else 0
        print(f"{i}. {method:15} : {time_taken:.2f}s (Speedup: {speedup:.2f}x)")
    
    print(f"\nFastest method: {sorted_results[0][0]}")
    print(f"Slowest method: {sorted_results[-1][0]}")

if __name__ == "__main__":
    asyncio.run(run_performance_comparison())
