import concurrent.futures
import threading
import time
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
import queue

@dataclass
class FileResult:
    filename: str
    content: str
    size: int
    read_time: float
    thread_id: str
    error: str = None

class ThreadedFileReader:
    def __init__(self, max_workers: int = 8, max_concurrent_files: int = 100):
        self.max_workers = max_workers
        self.max_concurrent_files = max_concurrent_files
        self.results_queue = queue.Queue()  # Thread-safe queue
        self.results_stack = deque()
        self.total_files = 0
        self.processed_files = 0
        self.lock = threading.Lock()  # For thread-safe operations
        
    def read_file_sync(self, file_path: Path) -> FileResult:
        """Synchronous file reading function for threading"""
        thread_id = threading.current_thread().name
        start_time = time.time()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                file_size = file_path.stat().st_size
                read_time = time.time() - start_time
                
                result = FileResult(
                    filename=str(file_path),
                    content=content[:1000] + "..." if len(content) > 1000 else content,
                    size=file_size,
                    read_time=read_time,
                    thread_id=thread_id
                )
                
                # Thread-safe progress update
                with self.lock:
                    self.processed_files += 1
                    print(f"✓ [{thread_id}] Read {file_path.name} ({file_size} bytes) in {read_time:.3f}s - Progress: {self.processed_files}/{self.total_files}")
                
                return result
                
        except Exception as e:
            read_time = time.time() - start_time
            result = FileResult(
                filename=str(file_path),
                content="",
                size=0,
                read_time=read_time,
                thread_id=thread_id,
                error=str(e)
            )
            
            with self.lock:
                self.processed_files += 1
                print(f"✗ [{thread_id}] Error reading {file_path.name}: {e} - Progress: {self.processed_files}/{self.total_files}")
            
            return result
    
    def read_files_threaded(self, directory_path: str, file_extensions: List[str] = None) -> None:
        """Read files using multiple threads"""
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
        print(f"Found {self.total_files} files to process with {self.max_workers} threads...")
        
        if self.total_files == 0:
            print("No files found!")
            return
        
        start_time = time.time()
        
        # Use ThreadPoolExecutor for parallel processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_file = {executor.submit(self.read_file_sync, file_path): file_path 
                            for file_path in files_to_read}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                result = future.result()
                self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed reading {len(files_to_read)} files in {total_time:.2f} seconds using {self.max_workers} threads!")
        print(f"Average time per file: {total_time/len(files_to_read):.3f} seconds")
