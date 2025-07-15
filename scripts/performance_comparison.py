import asyncio
import time
from pathlib import Path
import sys
import os

# Import all our readers
sys.path.append('scripts')
from async_file_reader import AsyncFileReader
from threaded_file_reader import ThreadedFileReader
from hybrid_async_threaded_reader import HybridAsyncThreadedReader
from multiprocess_file_reader import MultiprocessFileReader

async def run_performance_comparison():
    """Compare all different approaches"""
    
    # Create sample files first
    print("Creating sample files for testing...")
    reader = AsyncFileReader()
    reader.create_sample_files(200)  # Create 200 test files
    
    results = {}
    
    print("\n" + "="*60)
    print("PERFORMANCE COMPARISON")
    print("="*60)
    
    # Test 1: Original Async Approach
    print("\n1. Testing Original Async Approach...")
    start_time = time.time()
    async_reader = AsyncFileReader(max_concurrent_files=50)
    await async_reader.read_files_from_directory("sample_files")
    async_time = time.time() - start_time
    results['Async'] = async_time
    
    # Test 2: Pure Threading
    print("\n2. Testing Pure Threading Approach...")
    start_time = time.time()
    threaded_reader = ThreadedFileReader(max_workers=8)
    threaded_reader.read_files_threaded("sample_files")
    threaded_time = time.time() - start_time
    results['Threading'] = threaded_time
    
    # Test 3: Hybrid Async + Threading
    print("\n3. Testing Hybrid Async + Threading...")
    start_time = time.time()
    hybrid_reader = HybridAsyncThreadedReader(max_async_workers=30, max_thread_workers=4)
    await hybrid_reader.read_files_hybrid("sample_files")
    hybrid_time = time.time() - start_time
    results['Hybrid'] = hybrid_time
    
    # Test 4: Multiprocessing
    print("\n4. Testing Multiprocessing Approach...")
    start_time = time.time()
    multiprocess_reader = MultiprocessFileReader(max_processes=4)
    multiprocess_reader.read_files_multiprocess("sample_files")
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
