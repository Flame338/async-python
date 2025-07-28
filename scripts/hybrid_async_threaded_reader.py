import asyncio
import aiofiles
import concurrent.futures
import threading
import time
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque

@dataclass
class FileResult:
    filename: str
    content: str
    size: int
    read_time: float
    thread_id: str
    worker_type: str  # 'async' or 'thread'
    error: str = None

class HybridAsyncThreadedReader:
    def __init__(self, max_async_workers: int = 50, max_thread_workers: int = 4):
        self.max_async_workers = max_async_workers
        self.max_thread_workers = max_thread_workers
        self.results_stack = deque()
        self.total_files = 0
        self.processed_files = 0
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_async_workers)
        
    async def read_file_async(self, file_path: Path) -> FileResult:
        """Async file reading (for I/O bound operations)"""
        async with self.semaphore:
            thread_id = threading.current_thread().name
            start_time = time.time()
            
            try:
                async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = await file.read()
                    file_size = file_path.stat().st_size
                    read_time = time.time() - start_time
                    
                    result = FileResult(
                        filename=str(file_path),
                        content=content[:1000] + "..." if len(content) > 1000 else content,
                        size=file_size,
                        read_time=read_time,
                        thread_id=thread_id,
                        worker_type='async'
                    )
                    
                    async with self.lock:
                        self.processed_files += 1
                        print(f"✓ [ASYNC-{thread_id}] Read {file_path.name} ({file_size} bytes) in {read_time:.3f}s")
                    
                    return result
                    
            except Exception as e:
                read_time = time.time() - start_time
                result = FileResult(
                    filename=str(file_path),
                    content="",
                    size=0,
                    read_time=read_time,
                    thread_id=thread_id,
                    worker_type='async',
                    error=str(e)
                )
                
                async with self.lock:
                    self.processed_files += 1
                    print(f"✗ [ASYNC-{thread_id}] Error reading {file_path.name}: {e}")
                
                return result
    
    def read_file_sync(self, file_path: Path) -> FileResult:
        """Sync file reading (for CPU-intensive processing)"""
        thread_id = threading.current_thread().name
        start_time = time.time()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
                # Simulate CPU-intensive processing
                # (e.g., text analysis, parsing, etc.)
                processed_content = content.upper()  # Example processing
                
                file_size = file_path.stat().st_size
                read_time = time.time() - start_time
                
                result = FileResult(
                    filename=str(file_path),
                    content=processed_content[:1000] + "..." if len(processed_content) > 1000 else processed_content,
                    size=file_size,
                    read_time=read_time,
                    thread_id=thread_id,
                    worker_type='thread'
                )
                
                print(f"✓ [THREAD-{thread_id}] Processed {file_path.name} ({file_size} bytes) in {read_time:.3f}s")
                return result
                
        except Exception as e:
            read_time = time.time() - start_time
            result = FileResult(
                filename=str(file_path),
                content="",
                size=0,
                read_time=read_time,
                thread_id=thread_id,
                worker_type='thread',
                error=str(e)
            )
            
            print(f"✗ [THREAD-{thread_id}] Error processing {file_path.name}: {e}")
            return result
    
    async def read_files_hybrid(self, directory_path: str, file_extensions: List[str] = None) -> None:
        """Hybrid approach: async for I/O, threads for CPU-intensive tasks"""
        if file_extensions is None:
            file_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', '.md', '.csv']
        
        directory = Path(directory_path)
        if not directory.exists():
            print(f"Directory {directory_path} does not exist!")
            return
        
        # Collect all files
        files_to_read = []
        for ext in file_extensions:
            files_to_read.extend(directory.rglob(f"*{ext}"))
        
        self.total_files = len(files_to_read)
        print(f"Found {self.total_files} files to process with hybrid async+threading approach...")
        
        if self.total_files == 0:
            print("No files found!")
            return
        
        start_time = time.time()
        
        # Split files between async and threaded processing
        # Small files -> async, large files -> threads
        async_files = [f for f in files_to_read if f.stat().st_size < 10000]  # < 10KB
        thread_files = [f for f in files_to_read if f.stat().st_size >= 10000]  # >= 10KB
        
        print(f"Async processing: {len(async_files)} files")
        print(f"Thread processing: {len(thread_files)} files")
        
        # Create tasks for both approaches
        async_tasks = [self.read_file_async(file_path) for file_path in async_files]
        
        # Use thread pool for CPU-intensive tasks
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_thread_workers) as executor:
            thread_tasks = [
                loop.run_in_executor(executor, self.read_file_sync, file_path)
                for file_path in thread_files
            ]
            
            # Run both async and threaded tasks concurrently
            all_tasks = async_tasks + thread_tasks
            results = await asyncio.gather(*all_tasks, return_exceptions=True)
        
        # Store results
        for result in results:
            if isinstance(result, FileResult):
                self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed hybrid processing of {len(files_to_read)} files in {total_time:.2f} seconds!")
        print(f"Average time per file: {total_time/len(files_to_read):.3f} seconds")
