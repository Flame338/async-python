#!/usr/bin/env python3
"""
Main Entry Point for Concurrent File Reader Project
==================================================

This is the equivalent of main.c for this Python project.
It provides a unified interface to run all different concurrency approaches
and demonstrates the complete functionality of the system.

Usage:
    python main.py                    # Interactive menu
    python main.py --async            # Run async approach only
    python main.py --threading        # Run threading approach only  
    python main.py --hybrid           # Run hybrid approach only
    python main.py --multiprocess     # Run multiprocessing approach only
    python main.py --compare          # Run performance comparison
    python main.py --demo             # Run full demonstration
"""

import asyncio
import argparse
import sys
import time
from pathlib import Path
from typing import Optional

# Import all our concurrent file readers
from scripts.async_file_reader import AsyncFileReader
from scripts.threaded_file_reader import ThreadedFileReader
from scripts.hybrid_async_threaded_reader import HybridAsyncThreadedReader
from scripts.multiprocess_file_reader import MultiprocessFileReader

class ConcurrentFileReaderMain:
    """
    Main application class - equivalent to main() function in C
    Orchestrates all different concurrency approaches
    """
    
    def __init__(self):
        self.sample_dir = "sample_files"
        self.file_count = 100
        
    def print_banner(self):
        """Print application banner - like a C program header"""
        print("=" * 70)
        print("🚀 CONCURRENT FILE READER - PYTHON CONCURRENCY SHOWCASE")
        print("=" * 70)
        print("Demonstrating 4 different approaches to concurrent file processing:")
        print("1. Async I/O (Cooperative Concurrency)")
        print("2. Threading (Preemptive Multitasking)")  
        print("3. Hybrid (Async + Threading)")
        print("4. Multiprocessing (True Parallelism)")
        print("=" * 70)
        print()

    def setup_sample_files(self, count: int = None) -> bool:
        """Setup sample files for testing - like initialization in main()"""
        if count is None:
            count = self.file_count
            
        print(f"📁 Setting up {count} sample files...")
        try:
            # Use AsyncFileReader's file creation method
            reader = AsyncFileReader()
            reader.create_sample_files(count)
            print(f"✅ Successfully created {count} sample files in '{self.sample_dir}/'")
            return True
        except Exception as e:
            print(f"❌ Error creating sample files: {e}")
            return False

    async def run_async_approach(self) -> dict:
        """Run the async I/O approach"""
        print("\n🔄 Running Async I/O Approach...")
        print("-" * 50)
        
        start_time = time.time()
        reader = AsyncFileReader(max_concurrent_files=50)
        await reader.read_files_from_directory(self.sample_dir)
        execution_time = time.time() - start_time
        
        summary = reader.get_results_summary()
        summary['execution_time'] = execution_time
        summary['approach'] = 'Async I/O'
        
        self.print_results_summary(summary)
        return summary

    def run_threading_approach(self) -> dict:
        """Run the threading approach"""
        print("\n🧵 Running Threading Approach...")
        print("-" * 50)
        
        start_time = time.time()
        reader = ThreadedFileReader(max_workers=8)
        reader.read_files_threaded(self.sample_dir)
        execution_time = time.time() - start_time
        
        summary = reader.get_results_summary()
        summary['execution_time'] = execution_time
        summary['approach'] = 'Threading'
        
        self.print_results_summary(summary)
        return summary

    async def run_hybrid_approach(self) -> dict:
        """Run the hybrid approach"""
        print("\n🔀 Running Hybrid Approach...")
        print("-" * 50)
        
        start_time = time.time()
        reader = HybridAsyncThreadedReader(max_async_workers=30, max_thread_workers=4)
        await reader.read_files_hybrid(self.sample_dir)
        execution_time = time.time() - start_time
        
        summary = reader.get_results_summary()
        summary['execution_time'] = execution_time
        summary['approach'] = 'Hybrid'
        
        self.print_results_summary(summary)
        return summary

    def run_multiprocess_approach(self) -> dict:
        """Run the multiprocessing approach"""
        print("\n⚡ Running Multiprocessing Approach...")
        print("-" * 50)
        
        start_time = time.time()
        reader = MultiprocessFileReader(max_processes=4)
        reader.read_files_multiprocess(self.sample_dir)
        execution_time = time.time() - start_time
        
        summary = reader.get_results_summary()
        summary['execution_time'] = execution_time
        summary['approach'] = 'Multiprocessing'
        
        self.print_results_summary(summary)
        return summary

    def print_results_summary(self, summary: dict):
        """Print formatted results summary"""
        print(f"\n📊 Results Summary for {summary['approach']}:")
        print(f"   ⏱️  Execution Time: {summary['execution_time']:.2f} seconds")
        print(f"   📁 Total Files: {summary['total_files']}")
        print(f"   ✅ Successful: {summary['successful_reads']}")
        print(f"   ❌ Failed: {summary['failed_reads']}")
        print(f"   💾 Total Size: {summary['total_size_mb']} MB")
        print(f"   ⚡ Avg Time/File: {summary['average_read_time']:.3f}s")
        print(f"   📄 File Types: {', '.join(summary['file_extensions'])}")

    async def run_performance_comparison(self):
        """Run comprehensive performance comparison - main benchmark function"""
        print("\n🏁 PERFORMANCE COMPARISON")
        print("=" * 70)
        
        if not self.setup_sample_files(200):  # More files for better comparison
            return
        
        results = {}
        
        # Run all approaches
        results['async'] = await self.run_async_approach()
        results['threading'] = self.run_threading_approach()
        results['hybrid'] = await self.run_hybrid_approach()
        results['multiprocess'] = self.run_multiprocess_approach()
        
        # Print comparison table
        self.print_performance_comparison(results)

    def print_performance_comparison(self, results: dict):
        """Print formatted performance comparison table"""
        print("\n🏆 FINAL PERFORMANCE COMPARISON")
        print("=" * 70)
        
        # Sort by execution time
        sorted_results = sorted(results.items(), key=lambda x: x[1]['execution_time'])
        
        print(f"{'Rank':<4} {'Approach':<15} {'Time (s)':<10} {'Speedup':<10} {'Memory Est.':<12}")
        print("-" * 70)
        
        baseline_time = results['async']['execution_time']  # Use async as baseline
        
        for i, (approach, data) in enumerate(sorted_results, 1):
            speedup = baseline_time / data['execution_time']
            
            # Estimate memory usage
            memory_estimates = {
                'async': '~400KB',
                'threading': '~64MB', 
                'hybrid': '~32MB',
                'multiprocess': '~40MB'
            }
            
            memory = memory_estimates.get(approach, 'Unknown')
            
            print(f"{i:<4} {data['approach']:<15} {data['execution_time']:<10.2f} "
                  f"{speedup:<10.2f}x {memory:<12}")
        
        print("-" * 70)
        print(f"🥇 Winner: {sorted_results[0][1]['approach']} "
              f"({sorted_results[0][1]['execution_time']:.2f}s)")

    def interactive_menu(self):
        """Interactive menu system - like a C program menu"""
        while True:
            print("\n📋 INTERACTIVE MENU")
            print("=" * 30)
            print("1. Run Async I/O approach")
            print("2. Run Threading approach") 
            print("3. Run Hybrid approach")
            print("4. Run Multiprocessing approach")
            print("5. Run Performance Comparison")
            print("6. Setup Sample Files")
            print("7. Run Full Demo")
            print("0. Exit")
            print("-" * 30)
            
            try:
                choice = input("Enter your choice (0-7): ").strip()
                
                if choice == '0':
                    print("👋 Goodbye!")
                    break
                elif choice == '1':
                    asyncio.run(self.run_async_approach())
                elif choice == '2':
                    self.run_threading_approach()
                elif choice == '3':
                    asyncio.run(self.run_hybrid_approach())
                elif choice == '4':
                    self.run_multiprocess_approach()
                elif choice == '5':
                    asyncio.run(self.run_performance_comparison())
                elif choice == '6':
                    count = input("Enter number of files to create (default 100): ").strip()
                    count = int(count) if count.isdigit() else 100
                    self.setup_sample_files(count)
                elif choice == '7':
                    asyncio.run(self.run_full_demo())
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted by user. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    async def run_full_demo(self):
        """Run complete demonstration of all features"""
        print("\n🎬 FULL DEMONSTRATION")
        print("=" * 70)
        print("This will demonstrate all concurrency approaches with detailed analysis.")
        
        # Setup
        if not self.setup_sample_files(150):
            return
        
        # Run each approach with detailed output
        print("\n📚 Educational walkthrough of each approach:")
        
        # Async I/O with explanation
        print("\n1️⃣ ASYNC I/O - Cooperative Concurrency")
        print("   • Uses single thread with event loop")
        print("   • Excellent for I/O-bound operations")
        print("   • Memory efficient (~8KB per coroutine)")
        await self.run_async_approach()
        
        input("\nPress Enter to continue to Threading approach...")
        
        # Threading with explanation  
        print("\n2️⃣ THREADING - Preemptive Multitasking")
        print("   • Uses multiple OS threads")
        print("   • Good for mixed I/O and CPU work")
        print("   • Higher memory usage (~8MB per thread)")
        self.run_threading_approach()
        
        input("\nPress Enter to continue to Hybrid approach...")
        
        # Hybrid with explanation
        print("\n3️⃣ HYBRID - Best of Both Worlds")
        print("   • Combines async and threading")
        print("   • Routes work based on file characteristics")
        print("   • Optimal resource utilization")
        await self.run_hybrid_approach()
        
        input("\nPress Enter to continue to Multiprocessing approach...")
        
        # Multiprocessing with explanation
        print("\n4️⃣ MULTIPROCESSING - True Parallelism")
        print("   • Uses separate processes")
        print("   • No GIL limitations")
        print("   • Best for CPU-intensive work")
        self.run_multiprocess_approach()
        
        print("\n🎉 Full demonstration completed!")
        print("Check the generated files and performance metrics above.")

def create_argument_parser() -> argparse.ArgumentParser:
    """Create command line argument parser - like argc/argv in C"""
    parser = argparse.ArgumentParser(
        description="Concurrent File Reader - Python Concurrency Showcase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Interactive menu
  python main.py --async            # Run async approach only
  python main.py --compare          # Performance comparison
  python main.py --demo             # Full demonstration
        """
    )
    
    parser.add_argument('--async', action='store_true',
                       help='Run async I/O approach only')
    parser.add_argument('--threading', action='store_true',
                       help='Run threading approach only')
    parser.add_argument('--hybrid', action='store_true',
                       help='Run hybrid approach only')
    parser.add_argument('--multiprocess', action='store_true',
                       help='Run multiprocessing approach only')
    parser.add_argument('--compare', action='store_true',
                       help='Run performance comparison')
    parser.add_argument('--demo', action='store_true',
                       help='Run full demonstration')
    parser.add_argument('--files', type=int, default=100,
                       help='Number of sample files to create (default: 100)')
    parser.add_argument('--setup-only', action='store_true',
                       help='Only setup sample files and exit')
    
    return parser

async def main():
    """
    Main function - equivalent to int main(int argc, char *argv[]) in C
    This is the primary entry point for the entire application
    """
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Create main application instance
    app = ConcurrentFileReaderMain()
    app.file_count = args.files
    
    # Print banner
    app.print_banner()
    
    try:
        # Handle command line arguments
        if args.setup_only:
            app.setup_sample_files(args.files)
            return
        
        if args.async:
            app.setup_sample_files()
            await app.run_async_approach()
        elif args.threading:
            app.setup_sample_files()
            app.run_threading_approach()
        elif args.hybrid:
            app.setup_sample_files()
            await app.run_hybrid_approach()
        elif args.multiprocess:
            app.setup_sample_files()
            app.run_multiprocess_approach()
        elif args.compare:
            await app.run_performance_comparison()
        elif args.demo:
            await app.run_full_demo()
        else:
            # No arguments provided - run interactive menu
            app.interactive_menu()
            
    except KeyboardInterrupt:
        print("\n\n👋 Program interrupted by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

# This is the equivalent of int main() in C
if __name__ == "__main__":
    """
    Program entry point - equivalent to:
    
    int main(int argc, char *argv[]) {
        // Application logic here
        return 0;
    }
    """
    asyncio.run(main())
