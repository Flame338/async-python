import multiprocessing as mp
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
    process_id: int
    error: str = None

class MultiprocessFileReader:
    def __init__(self, max_processes: int = None):
        self.max_processes = max_processes or mp.cpu_count()
        self.results_stack = deque()
        self.total_files = 0
        
    @staticmethod
    def read_file_worker(file_path: Path) -> FileResult:
        """Worker function for multiprocessing"""
        process_id = os.getpid()
        start_time = time.time()
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                
                # CPU-intensive processing (this benefits from true parallelism)
                word_count = len(content.split())
                char_count = len(content)
                processed_content = f"[Words: {word_count}, Chars: {char_count}] {content}"
                
                file_size = file_path.stat().st_size
                read_time = time.time() - start_time
                
                result = FileResult(
                    filename=str(file_path),
                    content=processed_content[:1000] + "..." if len(processed_content) > 1000 else processed_content,
                    size=file_size,
                    read_time=read_time,
                    process_id=process_id
                )
                
                print(f"✓ [PID-{process_id}] Processed {file_path.name} ({file_size} bytes) in {read_time:.3f}s")
                return result
                
        except Exception as e:
            read_time = time.time() - start_time
            result = FileResult(
                filename=str(file_path),
                content="",
                size=0,
                read_time=read_time,
                process_id=process_id,
                error=str(e)
            )
            
            print(f"✗ [PID-{process_id}] Error processing {file_path.name}: {e}")
            return result
    
    def read_files_multiprocess(self, directory_path: str, file_extensions: List[str] = None) -> None:
        """Read files using multiple processes"""
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
        print(f"Found {self.total_files} files to process with {self.max_processes} processes...")
        
        if self.total_files == 0:
            print("No files found!")
            return
        
        start_time = time.time()
        
        # Use multiprocessing Pool
        with mp.Pool(processes=self.max_processes) as pool:
            results = pool.map(self.read_file_worker, files_to_read)
        
        # Store results
        for result in results:
            self.results_stack.append(result)
        
        total_time = time.time() - start_time
        print(f"\n🎉 Completed multiprocess processing of {len(files_to_read)} files in {total_time:.2f} seconds!")
        print(f"Average time per file: {total_time/len(files_to_read):.3f} seconds")
        print(f"Used {self.max_processes} processes")
