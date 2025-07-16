import asyncio
import aiohttp
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
import json

@dataclass
class UrlResult:
    url: str
    status_code: int
    response_size: int
    fetch_time: float
    content_preview: str
    error: str = None

class AsyncUrlFetcher:
    def __init__(self, max_concurrent_requests: int = 50):
        self.max_concurrent_requests = max_concurrent_requests
        self.results_stack = deque()  # Using deque as our stack/bucket
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.total_requests = 0
        self.processed_requests = 0
        
    async def fetch_url_async(self, session: aiohttp.ClientSession, url: str) -> UrlResult:
        """Asynchronously fetch a single URL"""
        async with self.semaphore:  # Limit concurrent HTTP requests
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
                error=error_message
            )
            
            self.processed_requests += 1
            status_icon = "✓" if not error_message else "✗"
            print(f"{status_icon} Fetched {url} (Status: {status_code}, Size: {response_size} bytes) in {fetch_time:.3f}s - Progress: {self.processed_requests}/{self.total_requests}")
            return result

    async def fetch_urls_from_list(self, urls: List[str]) -> None:
        """Fetch all URLs from a list concurrently"""
        self.total_requests = len(urls)
        print(f"Found {self.total_requests} URLs to fetch...")
        
        if self.total_requests == 0:
            print("No URLs provided!")
            return
        
        start_time = time.time()
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url_async(session, url) for url in urls]
            results = await asyncio.gather(*tasks, return_exceptions=True)
        
        total_time = time.time() - start_time
        
        # Add results to our stack
        for result in results:
            if isinstance(result, UrlResult):
                self.results_stack.append(result)
        
        print(f"\n🎉 Completed fetching {len(results)} URLs in {total_time:.2f} seconds!")
        print(f"Average time per URL: {total_time/len(results):.3f} seconds")
        
    def generate_sample_urls(self, count: int = 100) -> List[str]:
        """Generate sample URLs for testing"""
        sample_urls = []
        base_urls = [
            "https://www.example.com",
            "https://www.google.com",
            "https://www.github.com",
            "https://www.python.org",
            "https://www.wikipedia.org",
        ]
        
        print(f"Generating {count} sample URLs...")
        for i in range(count):
            # Mix in some valid and potentially invalid/slow URLs
            if i % 10 == 0: # Simulate a 404
                sample_urls.append(f"https://httpbin.org/status/404?q={i}")
            elif i % 15 == 0: # Simulate a slow response
                sample_urls.append(f"https://httpbin.org/delay/2?q={i}")
            else:
                sample_urls.append(f"{base_urls[i % len(base_urls)]}/page/{i}")
        
        print(f"Generated {len(sample_urls)} sample URLs.")
        return sample_urls
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get a summary of the results"""
        if not self.results_stack:
            return {"message": "No URLs have been processed yet"}
        
        successful_fetches = [r for r in self.results_stack if r.error is None]
        failed_fetches = [r for r in self.results_stack if r.error is not None]
        
        total_response_size = sum(r.response_size for r in successful_fetches)
        avg_fetch_time = sum(r.fetch_time for r in self.results_stack) / len(self.results_stack)
        
        status_codes = [r.status_code for r in self.results_stack if r.status_code != 0] # Exclude 0 for network errors
        
        return {
            "total_requests": len(self.results_stack),
            "successful_fetches": len(successful_fetches),
            "failed_fetches": len(failed_fetches),
            "total_response_size_bytes": total_response_size,
            "total_response_size_mb": round(total_response_size / (1024 * 1024), 2),
            "average_fetch_time": round(avg_fetch_time, 3),
            "status_codes": sorted(list(set(status_codes)))
        }
    
    def get_recent_results(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent results from the stack"""
        recent = list(self.results_stack)[-count:] if len(self.results_stack) >= count else list(self.results_stack)
        return [
            {
                "url": r.url,
                "status_code": r.status_code,
                "response_size": r.response_size,
                "fetch_time": r.fetch_time,
                "content_preview": r.content_preview[:200] + "..." if len(r.content_preview) > 200 else r.content_preview,
                "error": r.error
            }
            for r in reversed(recent)  # Most recent first
        ]

# Main execution function
async def main():
    fetcher = AsyncUrlFetcher(max_concurrent_requests=50)
    
    print("=== Async URL Fetcher Demo ===\n")
    
    # Generate sample URLs for demonstration
    sample_urls = fetcher.generate_sample_urls(100)
    
    # Fetch URLs
    await fetcher.fetch_urls_from_list(sample_urls)
    
    # Display results summary
    print("\n=== Results Summary ===")
    summary = fetcher.get_results_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n=== Recent URLs (Last 10) ===")
    recent_results = fetcher.get_recent_results(10)
    for i, result in enumerate(recent_results, 1):
        status = "✓" if not result["error"] else "✗"
        print(f"{i}. {status} {result['url']} (Status: {result['status_code']}, Size: {result['response_size']} bytes, {result['fetch_time']:.3f}s)")
        if result["error"]:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Preview: {result['content_preview'][:100]}...")
    
    return fetcher

# Run the async main function
if __name__ == "__main__":
    fetcher_instance = asyncio.run(main())
