import concurrent.futures
import threading
import time
import requests
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
import queue

@dataclass
class UrlResult:
    url: str
    status_code: int
    response_size: int
    fetch_time: float
    content_preview: str
    thread_id: str
    error: str = None

class ThreadedUrlFetcher:
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self.results_stack = deque()
        self.total_requests = 0
        self.processed_requests = 0
        self.lock = threading.Lock()  # For thread-safe operations
        
    def fetch_url_sync(self, url: str) -> UrlResult:
        """Synchronous URL fetching function for threading"""
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
            response_size = len(content.encode('utf-8'))
            content_preview = content[:1000] + "..." if len(content) > 1000 else content
            
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
            error=error_message
        )
        
        # Thread-safe progress update
        with self.lock:
            self.processed_requests += 1
            status_icon = "✓" if not error_message else "✗"
            print(f"{status_icon} [{thread_id}] Fetched {url} (Status: {status_code}, Size: {response_size} bytes) in {fetch_time:.3f}s - Progress: {self.processed_requests}/{self.total_requests}")
        
        return result
    
    def fetch_urls_threaded(self, urls: List[str]) -> None:
        """Fetch URLs using multiple threads"""
        self.total_requests = len(urls)
        print(f"Found {self.total_requests} URLs to fetch with {self.max_workers} threads...")
        
        if self.total_requests == 0:
            print("No URLs provided!")
            return
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_url = {executor.submit(self.fetch_url_sync, url): url 
                            for url in urls}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_url):
                result = future.result()
                self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed fetching {len(urls)} URLs in {total_time:.2f} seconds using {self.max_workers} threads!")
        print(f"Average time per URL: {total_time/len(urls):.3f} seconds")
