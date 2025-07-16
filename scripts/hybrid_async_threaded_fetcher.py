import asyncio
import aiohttp
import concurrent.futures
import threading
import time
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque

@dataclass
class UrlResult:
    url: str
    status_code: int
    response_size: int
    fetch_time: float
    thread_id: str
    worker_type: str  # 'async' or 'thread'
    error: str = None

class HybridAsyncThreadedFetcher:
    def __init__(self, max_async_workers: int = 30, max_thread_workers: int = 4):
        self.max_async_workers = max_async_workers
        self.max_thread_workers = max_thread_workers
        self.results_stack = deque()
        self.total_requests = 0
        self.processed_requests = 0
        self.lock = asyncio.Lock() # For async-safe progress updates
        self.semaphore = asyncio.Semaphore(max_async_workers)
        
    async def fetch_url_async(self, session: aiohttp.ClientSession, url: str) -> UrlResult:
        """Async URL fetching (for I/O bound operations)"""
        async with self.semaphore:
            thread_id = threading.current_thread().name
            start_time = time.time()
            status_code = 0
            response_size = 0
            content_preview = ""
            error_message = None
            
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    status_code = response.status
                    content = await response.text()
                    response_size = len(content.encode('utf-8'))
                    content_preview = content[:1000] + "..." if len(content) > 1000 else content
                    
                    if status_code >= 400:
                        error_message = f"HTTP Error: {status_code}"
                        
            except aiohttp.ClientError as e:
                error_message = f"Network Error: {e}"
            except asyncio.TimeoutError:
                error_message = "Timeout Error"
            except Exception as e:
                error_message = f"Unexpected Error: {e}"
            
            fetch_time = time.time() - start_time
            
            result = UrlResult(
                url=url,
                status_code=status_code,
                response_size=response_size,
                fetch_time=fetch_time,
                content_preview=content_preview,
                thread_id=thread_id,
                worker_type='async',
                error=error_message
            )
            
            async with self.lock:
                self.processed_requests += 1
                status_icon = "✓" if not error_message else "✗"
                print(f"{status_icon} [ASYNC-{thread_id}] Fetched {url} (Status: {status_code}) in {fetch_time:.3f}s")
            
            return result
    
    def fetch_url_sync(self, url: str) -> UrlResult:
        """Sync URL fetching (for CPU-intensive processing of response)"""
        thread_id = threading.current_thread().name
        start_time = time.time()
        status_code = 0
        response_size = 0
        content_preview = ""
        error_message = None
        
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            content = response.text
            
            # Simulate CPU-intensive processing of the response
            processed_content = content.upper() # Example processing
            
            response_size = len(processed_content.encode('utf-8'))
            content_preview = processed_content[:1000] + "..." if len(processed_content) > 1000 else processed_content
            
            if status_code >= 400:
                error_message = f"HTTP Error: {status_code}"
                
        except requests.exceptions.RequestException as e:
            error_message = f"Network Error: {e}"
        except Exception as e:
            error_message = f"Unexpected Error: {e}"
        
        fetch_time = time.time() - start_time
        
        result = UrlResult(
            url=url,
            status_code=status_code,
            response_size=response_size,
            fetch_time=fetch_time,
            content_preview=content_preview,
            thread_id=thread_id,
            worker_type='thread',
            error=error_message
        )
        
        status_icon = "✓" if not error_message else "✗"
        print(f"{status_icon} [THREAD-{thread_id}] Processed {url} (Status: {status_code}) in {fetch_time:.3f}s")
        return result
    
    async def fetch_urls_hybrid(self, urls: List[str]) -> None:
        """Hybrid approach: async for simple fetches, threads for CPU-intensive response processing"""
        self.total_requests = len(urls)
        print(f"Found {self.total_requests} URLs to fetch with hybrid async+threading approach...")
        
        if self.total_requests == 0:
            print("No URLs provided!")
            return
        
        start_time = time.time()
        
        # Split URLs between async and threaded processing
        # For simplicity, we'll alternate or use a simple heuristic.
        # In a real scenario, this might be based on expected response size or complexity.
        async_urls = [url for i, url in enumerate(urls) if i % 2 == 0] # Even indices for async
        thread_urls = [url for i, url in enumerate(urls) if i % 2 != 0] # Odd indices for thread
        
        print(f"Async fetching: {len(async_urls)} URLs")
        print(f"Thread processing: {len(thread_urls)} URLs")
        
        # Create tasks for both approaches
        async with aiohttp.ClientSession() as session:
            async_tasks = [self.fetch_url_async(session, url) for url in async_urls]
        
        # Use thread pool for CPU-intensive tasks
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread_workers) as executor:
            thread_tasks = [
                loop.run_in_executor(executor, self.fetch_url_sync, url)
                for url in thread_urls
            ]
            
            # Run both async and threaded tasks concurrently
            all_tasks = async_tasks + thread_tasks
            results = await asyncio.gather(*all_tasks, return_exceptions=True)
        
        # Store results
        for result in results:
            if isinstance(result, UrlResult):
                self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed hybrid processing of {len(urls)} URLs in {total_time:.2f} seconds!")
        print(f"Average time per URL: {total_time/len(urls):.3f} seconds")
