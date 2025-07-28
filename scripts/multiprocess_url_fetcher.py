import multiprocessing as mp
import time
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
import queue
import os

@dataclass
class UrlResult:
    url: str
    status_code: int
    response_size: int
    fetch_time: float
    content_preview: str
    process_id: int
    error: str = None

class MultiprocessUrlFetcher:
    def __init__(self, max_processes: int = None):
        self.max_processes = max_processes or mp.cpu_count()
        self.results_stack = deque()
        self.total_requests = 0
        
    @staticmethod
    def fetch_url_worker(url: str) -> UrlResult:
        """Worker function for multiprocessing to fetch and process a URL"""
        process_id = os.getpid()
        start_time = time.time()
        status_code = 0
        response_size = 0
        content_preview = ""
        error_message = None
        
        try:
            response = requests.get(url, timeout=10)
            status_code = response.status_code
            content = response.text
            
            # Simulate CPU-intensive processing (e.g., parsing HTML, NLP)
            # This benefits from true parallelism across processes
            processed_content = content.lower() # Example processing
            
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
            process_id=process_id,
            error=error_message
        )
        
        status_icon = "✓" if not error_message else "✗"
        print(f"{status_icon} [PID-{process_id}] Processed {url} (Status: {status_code}) in {fetch_time:.3f}s")
        return result
    
    def fetch_urls_multiprocess(self, urls: List[str]) -> None:
        """Fetch URLs using multiple processes"""
        self.total_requests = len(urls)
        print(f"Found {self.total_requests} URLs to fetch with {self.max_processes} processes...")
        
        if self.total_requests == 0:
            print("No URLs provided!")
            return
        
        start_time = time.time()
        
        # Use multiprocessing Pool
        with mp.Pool(processes=self.max_processes) as pool:
            results = pool.map(self.fetch_url_worker, urls)
        
        # Store results
        for result in results:
            self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed multiprocess fetching of {len(urls)} URLs in {total_time:.2f} seconds!")
        print(f"Average time per URL: {total_time/len(urls):.3f} seconds")
        print(f"Used {self.max_processes} processes")
