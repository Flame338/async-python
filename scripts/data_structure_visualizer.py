import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle
import numpy as np

def create_data_structure_diagram():
    """Create a comprehensive data structure and memory layout diagram"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    fig.suptitle('Data Structures and Memory Layout Comparison', fontsize=16, fontweight='bold')
    
    # 1. Async I/O Data Structures
    ax1.set_title('Async I/O - Memory Layout', fontsize=12, fontweight='bold')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    
    # Event loop
    event_loop = Rectangle((1, 8), 8, 1.5, facecolor='lightblue', edgecolor='black', linewidth=2)
    ax1.add_patch(event_loop)
    ax1.text(5, 8.75, 'Event Loop (Single Thread)', ha='center', va='center', fontweight='bold')
    
    # Semaphore
    semaphore = Rectangle((1, 6.5), 3, 1, facecolor='orange', edgecolor='black')
    ax1.add_patch(semaphore)
    ax1.text(2.5, 7, 'Semaphore\n(Max: 50)', ha='center', va='center', fontsize=9)
    
    # Coroutines
    for i in range(5):
        coroutine = Rectangle((5 + i*0.8, 6.5), 0.7, 1, facecolor='lightgreen', edgecolor='black')
        ax1.add_patch(coroutine)
        ax1.text(5.35 + i*0.8, 7, f'C{i+1}', ha='center', va='center', fontsize=8)
    
    # Results deque
    deque_box = Rectangle((1, 4.5), 8, 1.5, facecolor='lightyellow', edgecolor='black')
    ax1.add_patch(deque_box)
    ax1.text(5, 5.25, 'Results Deque (Thread-Safe, O(1) operations)', ha='center', va='center', fontweight='bold')
    
    # Memory usage annotation
    ax1.text(5, 3, 'Memory per coroutine: ~8KB\nTotal concurrent: 50-100\nTotal memory: ~400KB-800KB', 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor='black'))
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.axis('off')
    
    # 2. Threading Data Structures
    ax2.set_title('Threading - Memory Layout', fontsize=12, fontweight='bold')
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    
    # Main thread
    main_thread = Rectangle((1, 8.5), 8, 1, facecolor='lightcoral', edgecolor='black', linewidth=2)
    ax2.add_patch(main_thread)
    ax2.text(5, 9, 'Main Thread (Coordinator)', ha='center', va='center', fontweight='bold')
    
    # Worker threads
    thread_colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink']
    for i in range(4):
        thread = Rectangle((1 + i*2, 6.5), 1.8, 1.5, facecolor=thread_colors[i], edgecolor='black')
        ax2.add_patch(thread)
        ax2.text(1.9 + i*2, 7.25, f'Thread {i+1}\n8MB Stack', ha='center', va='center', fontsize=9)
    
    # Thread-safe queue
    queue_box = Rectangle((1, 4.5), 8, 1, facecolor='orange', edgecolor='black')
    ax2.add_patch(queue_box)
    ax2.text(5, 5, 'Thread-Safe Queue (Lock Protected)', ha='center', va='center', fontweight='bold')
    
    # Lock visualization
    lock = Circle((5, 3), 0.5, facecolor='red', edgecolor='black')
    ax2.add_patch(lock)
    ax2.text(5, 3, 'Lock', ha='center', va='center', fontweight='bold', color='white')
    
    # Memory usage annotation
    ax2.text(5, 1.5, 'Memory per thread: ~8MB\nThread count: 4-8\nTotal memory: ~32MB-64MB', 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor='black'))
    
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis('off')
    
    # 3. Hybrid Data Structures
    ax3.set_title('Hybrid - Adaptive Memory Layout', fontsize=12, fontweight='bold')
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    
    # Event loop + thread pool
    hybrid_main = Rectangle((1, 8.5), 8, 1, facecolor='purple', alpha=0.7, edgecolor='black', linewidth=2)
    ax3.add_patch(hybrid_main)
    ax3.text(5, 9, 'Event Loop + ThreadPoolExecutor', ha='center', va='center', fontweight='bold', color='white')
    
    # Async section
    async_section = Rectangle((1, 6.5), 3.5, 1.5, facecolor='lightblue', edgecolor='black')
    ax3.add_patch(async_section)
    ax3.text(2.75, 7.25, 'Async Processing\n(Small Files)', ha='center', va='center', fontsize=9)
    
    # Threading section
    thread_section = Rectangle((5.5, 6.5), 3.5, 1.5, facecolor='lightgreen', edgecolor='black')
    ax3.add_patch(thread_section)
    ax3.text(7.25, 7.25, 'Thread Processing\n(Large Files)', ha='center', va='center', fontsize=9)
    
    # Decision logic
    decision = Rectangle((3.5, 5), 3, 1, facecolor='yellow', edgecolor='black')
    ax3.add_patch(decision)
    ax3.text(5, 5.5, 'Size-Based Routing\n(< 10KB → Async)', ha='center', va='center', fontsize=9)
    
    # Unified results
    unified_results = Rectangle((1, 3), 8, 1, facecolor='lightcoral', edgecolor='black')
    ax3.add_patch(unified_results)
    ax3.text(5, 3.5, 'Unified Results Collection', ha='center', va='center', fontweight='bold')
    
    # Memory usage annotation
    ax3.text(5, 1.5, 'Adaptive memory usage\nSmall files: ~8KB each\nLarge files: ~8MB thread\nOptimal resource utilization', 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor='black'))
    
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.axis('off')
    
    # 4. Multiprocessing Data Structures
    ax4.set_title('Multiprocessing - Isolated Memory Spaces', fontsize=12, fontweight='bold')
    ax4.set_xlim(0, 10)
    ax4.set_ylim(0, 10)
    
    # Main process
    main_process = Rectangle((1, 8.5), 8, 1, facecolor='darkblue', alpha=0.8, edgecolor='black', linewidth=2)
    ax4.add_patch(main_process)
    ax4.text(5, 9, 'Main Process (Coordinator)', ha='center', va='center', fontweight='bold', color='white')
    
    # Worker processes
    process_colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightpink']
    for i in range(4):
        process = Rectangle((0.5 + i*2.25, 6), 2, 2, facecolor=process_colors[i], edgecolor='black', linewidth=2)
        ax4.add_patch(process)
        ax4.text(1.5 + i*2.25, 7, f'Process {i+1}\nPID: {1000+i}\n~10MB Memory', ha='center', va='center', fontsize=8)
    
    # IPC mechanism
    ipc_box = Rectangle((1, 4), 8, 1, facecolor='orange', edgecolor='black')
    ax4.add_patch(ipc_box)
    ax4.text(5, 4.5, 'Inter-Process Communication (Serialization)', ha='center', va='center', fontweight='bold')
    
    # Memory isolation visualization
    for i in range(4):
        isolation = Rectangle((0.3 + i*2.25, 5.8), 2.4, 2.4, fill=False, edgecolor='red', linewidth=3, linestyle='--')
        ax4.add_patch(isolation)
    
    ax4.text(5, 2.5, 'Memory per process: ~10MB+\nProcess count: CPU cores (4)\nTotal memory: ~40MB+\nTrue parallelism (No GIL)', 
             ha='center', va='center', fontsize=10,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='white', edgecolor='black'))
    
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig('data_structure_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Data structure diagram saved as 'data_structure_diagram.png'")

def create_concurrency_model_comparison():
    """Create a detailed concurrency model comparison"""
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_title('Concurrency Models - Detailed Comparison', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 16)
    
    # Create comparison table
    models = ['Async I/O', 'Threading', 'Hybrid', 'Multiprocessing']
    characteristics = [
        'Concurrency Type',
        'Memory per Unit',
        'CPU Utilization', 
        'I/O Efficiency',
        'Scalability',
        'Complexity',
        'Best Use Case'
    ]
    
    data = [
        ['Cooperative', 'Preemptive', 'Both', 'Parallel'],
        ['~8KB/coroutine', '~8MB/thread', 'Variable', '~10MB+/process'],
        ['Single-threaded', 'Multi-threaded (GIL)', 'Optimal', 'Multi-core'],
        ['Excellent', 'Good', 'Excellent', 'Good'],
        ['High', 'Medium', 'High', 'Medium'],
        ['Low', 'Medium', 'High', 'Medium'],
        ['Many small files', 'Mixed I/O+CPU', 'Production', 'CPU-intensive']
    ]
    
    # Create table
    cell_height = 1.8
    cell_width = 2.8
    
    # Headers
    for i, model in enumerate(models):
        header = Rectangle((1 + i*cell_width, 14), cell_width, cell_height, 
                          facecolor='darkblue', alpha=0.8, edgecolor='black')
        ax.add_patch(header)
        ax.text(1 + i*cell_width + cell_width/2, 14 + cell_height/2, model, 
                ha='center', va='center', fontweight='bold', color='white', fontsize=10)
    
    # Row labels
    colors = ['lightblue', 'lightgreen', 'lightyellow', 'lightcoral', 'lightpink', 'lightgray', 'orange']
    for i, char in enumerate(characteristics):
        label = Rectangle((0, 12.2 - i*cell_height), 1, cell_height, 
                         facecolor='gray', alpha=0.8, edgecolor='black')
        ax.add_patch(label)
        ax.text(0.5, 12.2 - i*cell_height + cell_height/2, char, 
                ha='center', va='center', fontweight='bold', color='white', fontsize=9, rotation=0)
    
    # Data cells
    for i, row in enumerate(data):
        for j, cell_data in enumerate(row):
            cell = Rectangle((1 + j*cell_width, 12.2 - i*cell_height), cell_width, cell_height,
                           facecolor=colors[i], alpha=0.7, edgecolor='black')
            ax.add_patch(cell)
            ax.text(1 + j*cell_width + cell_width/2, 12.2 - i*cell_height + cell_height/2, 
                   cell_data, ha='center', va='center', fontsize=9, fontweight='bold')
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('concurrency_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Concurrency model comparison saved as 'concurrency_model_comparison.png'")

if __name__ == "__main__":
    print("Creating data structure diagrams...")
    create_data_structure_diagram()
    
    print("\nCreating concurrency model comparison...")
    create_concurrency_model_comparison()
    
    print("\nDiagrams created successfully!")
    print("Files generated:")
    print("- data_structure_diagram.png")
    print("- concurrency_model_comparison.png")
