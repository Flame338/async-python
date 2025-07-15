import asyncio
import aiofiles
import os
import time
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
from collections import deque
import json

@dataclass
class FileResult:
    filename: str
    content: str
    size: int
    read_time: float
    error: str = None

class AsyncFileReader:
    def __init__(self, max_concurrent_files: int = 100):
        self.max_concurrent_files = max_concurrent_files
        self.results_stack = deque()  # Using deque as our stack/bucket
        self.semaphore = asyncio.Semaphore(max_concurrent_files)
        self.total_files = 0
        self.processed_files = 0
        
    async def read_file_async(self, file_path: Path) -> FileResult:
        """Asynchronously read a single file"""
        async with self.semaphore:  # Limit concurrent file operations
            start_time = time.time()
            try:
                async with aiofiles.open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = await file.read()
                    file_size = file_path.stat().st_size
                    read_time = time.time() - start_time
                    
                    result = FileResult(
                        filename=str(file_path),
                        content=content[:1000] + "..." if len(content) > 1000 else content,  # Truncate for display
                        size=file_size,
                        read_time=read_time
                    )
                    
                    self.processed_files += 1
                    print(f"✓ Read {file_path.name} ({file_size} bytes) in {read_time:.3f}s - Progress: {self.processed_files}/{self.total_files}")
                    return result
                    
            except Exception as e:
                read_time = time.time() - start_time
                result = FileResult(
                    filename=str(file_path),
                    content="",
                    size=0,
                    read_time=read_time,
                    error=str(e)
                )
                self.processed_files += 1
                print(f"✗ Error reading {file_path.name}: {e} - Progress: {self.processed_files}/{self.total_files}")
                return result

    async def read_files_from_directory(self, directory_path: str, file_extensions: List[str] = None) -> None:
        """Read all files from a directory and its subdirectories"""
        if file_extensions is None:
            file_extensions = ['.txt', '.py', '.js', '.html', '.css', '.json', '.md', '.csv']
        
        directory = Path(directory_path)
        if not directory.exists():
            print(f"Directory {directory_path} does not exist!")
            return
        
        # Collect all files to process
        files_to_read = []
        for ext in file_extensions:
            files_to_read.extend(directory.rglob(f"*{ext}"))
        
        self.total_files = len(files_to_read)
        print(f"Found {self.total_files} files to process...")
        
        if self.total_files == 0:
            print("No files found with the specified extensions!")
            return
        
        # Create tasks for all files
        tasks = [self.read_file_async(file_path) for file_path in files_to_read]
        
        # Execute all tasks concurrently
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        total_time = time.time() - start_time
        
        # Add results to our stack
        for result in results:
            if isinstance(result, FileResult):
                self.results_stack.append(result)
        
        print(f"\n🎉 Completed reading {len(results)} files in {total_time:.2f} seconds!")
        print(f"Average time per file: {total_time/len(results):.3f} seconds")
        
    def create_sample_files(self, count: int = 50) -> None:
        """Create sample files for testing"""
        sample_dir = Path("sample_files")
        sample_dir.mkdir(exist_ok=True)
        
        print(f"Creating {count} sample files...")
        
        for i in range(count):
            file_path = sample_dir / f"sample_{i:03d}.txt"
            with open(file_path, 'w') as f:
                content = f"""Sample File {i}
This is a test file created for demonstration purposes.
File number: {i}
Content length: {'x' * (i * 10)}
Random data: {os.urandom(16).hex()}
"""
                f.write(content)
        
        # Create some different file types
        for ext, content_template in [
            ('.json', '{"id": %d, "name": "file_%d", "data": [1, 2, 3, 4, 5]}'),
            ('.py', '# Python file %d\nprint("Hello from file %d")\ndata = [i for i in range(10)]'),
            ('.html', '<html><head><title>File %d</title></head><body><h1>File %d</h1></body></html>'),
        ]:
            for i in range(10):
                file_path = sample_dir / f"sample_{i:03d}{ext}"
                with open(file_path, 'w') as f:
                    f.write(content_template % (i, i))
        
        print(f"Created sample files in {sample_dir}")
    
    def get_results_summary(self) -> Dict[str, Any]:
        """Get a summary of the results"""
        if not self.results_stack:
            return {"message": "No files have been processed yet"}
        
        successful_reads = [r for r in self.results_stack if r.error is None]
        failed_reads = [r for r in self.results_stack if r.error is not None]
        
        total_size = sum(r.size for r in successful_reads)
        avg_read_time = sum(r.read_time for r in self.results_stack) / len(self.results_stack)
        
        return {
            "total_files": len(self.results_stack),
            "successful_reads": len(successful_reads),
            "failed_reads": len(failed_reads),
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "average_read_time": round(avg_read_time, 3),
            "file_extensions": list(set(Path(r.filename).suffix for r in self.results_stack))
        }
    
    def get_recent_results(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent results from the stack"""
        recent = list(self.results_stack)[-count:] if len(self.results_stack) >= count else list(self.results_stack)
        return [
            {
                "filename": r.filename,
                "size": r.size,
                "read_time": r.read_time,
                "content_preview": r.content[:200] + "..." if len(r.content) > 200 else r.content,
                "error": r.error
            }
            for r in reversed(recent)  # Most recent first
        ]

# Main execution function
async def main():
    reader = AsyncFileReader(max_concurrent_files=50)
    
    print("=== Async File Reader Demo ===\n")
    
    # Create sample files for demonstration
    reader.create_sample_files(100)
    
    # Read files from the sample directory
    await reader.read_files_from_directory("sample_files")
    
    # Display results summary
    print("\n=== Results Summary ===")
    summary = reader.get_results_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n=== Recent Files (Last 10) ===")
    recent_results = reader.get_recent_results(10)
    for i, result in enumerate(recent_results, 1):
        status = "✓" if not result["error"] else "✗"
        print(f"{i}. {status} {Path(result['filename']).name} ({result['size']} bytes, {result['read_time']:.3f}s)")
        if result["error"]:
            print(f"   Error: {result['error']}")
        else:
            print(f"   Preview: {result['content_preview'][:100]}...")
    
    return reader

# Run the async main function
if __name__ == "__main__":
    reader_instance = asyncio.run(main())
