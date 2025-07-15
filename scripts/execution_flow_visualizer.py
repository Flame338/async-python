import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_execution_flow_diagram():
    """Create a comprehensive execution flow diagram for all approaches"""
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle('Concurrent File Reader - Execution Flow Comparison', fontsize=16, fontweight='bold')
    
    # Color scheme
    colors = {
        'start': '#4CAF50',
        'process': '#2196F3', 
        'decision': '#FF9800',
        'io': '#9C27B0',
        'result': '#F44336',
        'sync': '#607D8B'
    }
    
    # 1. Async I/O Flow
    ax1.set_title('Async I/O Execution Flow', fontsize=14, fontweight='bold')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 12)
    
    # Async flow boxes
    async_boxes = [
        (5, 11, 'File Discovery', colors['start']),
        (5, 9.5, 'Create Coroutines', colors['process']),
        (5, 8, 'Semaphore Control', colors['decision']),
        (5, 6.5, 'Async I/O Operations', colors['io']),
        (5, 5, 'Cooperative Yielding', colors['process']),
        (5, 3.5, 'Results Collection', colors['result']),
        (5, 2, 'Deque Storage', colors['sync'])
    ]
    
    for x, y, text, color in async_boxes:
        box = FancyBboxPatch((x-1.5, y-0.4), 3, 0.8, boxstyle="round,pad=0.1", 
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax1.add_patch(box)
        ax1.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=10)
    
    # Async arrows
    for i in range(len(async_boxes)-1):
        ax1.arrow(5, async_boxes[i][1]-0.5, 0, -0.5, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Side annotations for async
    ax1.text(8.5, 8, 'Max 50-100\nConcurrent', ha='center', va='center', fontsize=9, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.5))
    ax1.text(8.5, 5, 'Non-blocking\nI/O Operations', ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.axis('off')
    
    # 2. Threading Flow
    ax2.set_title('Threading Execution Flow', fontsize=14, fontweight='bold')
    ax2.set_xlim(0, 12)
    ax2.set_ylim(0, 12)
    
    # Threading flow
    thread_main = [
        (3, 11, 'File Discovery', colors['start']),
        (3, 9.5, 'ThreadPool Creation', colors['process']),
        (3, 8, 'Task Distribution', colors['decision']),
        (3, 2, 'Results Collection', colors['result'])
    ]
    
    thread_workers = [
        (9, 8, 'Thread 1', colors['io']),
        (9, 6.5, 'Thread 2', colors['io']),
        (9, 5, 'Thread N', colors['io'])
    ]
    
    # Draw main thread flow
    for x, y, text, color in thread_main:
        box = FancyBboxPatch((x-1, y-0.4), 2, 0.8, boxstyle="round,pad=0.1",
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax2.add_patch(box)
        ax2.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw worker threads
    for x, y, text, color in thread_workers:
        box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, boxstyle="round,pad=0.1",
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax2.add_patch(box)
        ax2.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Threading arrows
    ax2.arrow(3, 10.5, 0, -1, head_width=0.2, head_length=0.1, fc='black', ec='black')
    ax2.arrow(3, 8.5, 0, -1, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Distribution arrows
    for _, y, _, _ in thread_workers:
        ax2.arrow(4, 8, 4, y-8, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
        ax2.arrow(8, y, -4, 2-y, head_width=0.2, head_length=0.1, fc='red', ec='red')
    
    ax2.arrow(3, 7.5, 0, -5, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Threading annotations
    ax2.text(6, 9, 'Parallel\nExecution', ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.5))
    ax2.text(6, 3.5, 'Thread-Safe\nCollection', ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='orange', alpha=0.5))
    
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.axis('off')
    
    # 3. Hybrid Flow
    ax3.set_title('Hybrid Async+Threading Flow', fontsize=14, fontweight='bold')
    ax3.set_xlim(0, 12)
    ax3.set_ylim(0, 12)
    
    # Hybrid flow boxes
    hybrid_boxes = [
        (6, 11, 'File Discovery', colors['start']),
        (6, 9.5, 'Size Analysis', colors['decision']),
        (3, 8, 'Small Files\n(Async)', colors['io']),
        (9, 8, 'Large Files\n(Threading)', colors['process']),
        (3, 6, 'Async Processing', colors['io']),
        (9, 6, 'Thread Processing', colors['process']),
        (6, 4, 'Unified Collection', colors['result']),
        (6, 2.5, 'Final Results', colors['sync'])
    ]
    
    for x, y, text, color in hybrid_boxes:
        width = 2.5 if '\n' in text else 2
        box = FancyBboxPatch((x-width/2, y-0.4), width, 0.8, boxstyle="round,pad=0.1",
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax3.add_patch(box)
        ax3.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Hybrid arrows
    ax3.arrow(6, 10.5, 0, -1, head_width=0.2, head_length=0.1, fc='black', ec='black')
    ax3.arrow(5, 9, -1.5, -0.5, head_width=0.2, head_length=0.1, fc='purple', ec='purple')
    ax3.arrow(7, 9, 1.5, -0.5, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.arrow(3, 7.5, 0, -1, head_width=0.2, head_length=0.1, fc='purple', ec='purple')
    ax3.arrow(9, 7.5, 0, -1, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.arrow(4, 6, 1.5, -1.5, head_width=0.2, head_length=0.1, fc='purple', ec='purple')
    ax3.arrow(8, 6, -1.5, -1.5, head_width=0.2, head_length=0.1, fc='blue', ec='blue')
    ax3.arrow(6, 3.5, 0, -0.5, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Hybrid annotations
    ax3.text(1, 7, 'Size < 10KB', ha='center', va='center', fontsize=8,
             bbox=dict(boxstyle="round,pad=0.2", facecolor='lightgreen', alpha=0.5))
    ax3.text(11, 7, 'Size ≥ 10KB', ha='center', va='center', fontsize=8,
             bbox=dict(boxstyle="round,pad=0.2", facecolor='lightcoral', alpha=0.5))
    
    ax3.set_xticks([])
    ax3.set_yticks([])
    ax3.axis('off')
    
    # 4. Multiprocessing Flow
    ax4.set_title('Multiprocessing Execution Flow', fontsize=14, fontweight='bold')
    ax4.set_xlim(0, 12)
    ax4.set_ylim(0, 12)
    
    # Multiprocessing boxes
    mp_main = [
        (3, 11, 'File Discovery', colors['start']),
        (3, 9.5, 'Process Pool', colors['process']),
        (3, 8, 'Task Distribution', colors['decision']),
        (3, 2, 'IPC Collection', colors['result'])
    ]
    
    mp_processes = [
        (9, 8.5, 'Process 1', colors['io']),
        (9, 6.5, 'Process 2', colors['io']),
        (9, 4.5, 'Process N', colors['io'])
    ]
    
    # Draw main process flow
    for x, y, text, color in mp_main:
        box = FancyBboxPatch((x-1, y-0.4), 2, 0.8, boxstyle="round,pad=0.1",
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax4.add_patch(box)
        ax4.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Draw worker processes
    for x, y, text, color in mp_processes:
        box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6, boxstyle="round,pad=0.1",
                           facecolor=color, alpha=0.7, edgecolor='black')
        ax4.add_patch(box)
        ax4.text(x, y, text, ha='center', va='center', fontweight='bold', fontsize=9)
    
    # Multiprocessing arrows
    ax4.arrow(3, 10.5, 0, -1, head_width=0.2, head_length=0.1, fc='black', ec='black')
    ax4.arrow(3, 8.5, 0, -1, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Distribution and collection arrows
    for _, y, _, _ in mp_processes:
        ax4.arrow(4, 8, 4, y-8, head_width=0.2, head_length=0.1, fc='green', ec='green')
        ax4.arrow(8, y, -4, 2-y, head_width=0.2, head_length=0.1, fc='red', ec='red')
    
    ax4.arrow(3, 7.5, 0, -5, head_width=0.2, head_length=0.1, fc='black', ec='black')
    
    # Multiprocessing annotations
    ax4.text(6, 9.5, 'True Parallel\nExecution', ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='lightgreen', alpha=0.5))
    ax4.text(6, 3.5, 'Inter-Process\nCommunication', ha='center', va='center', fontsize=9,
             bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.5))
    
    ax4.set_xticks([])
    ax4.set_yticks([])
    ax4.axis('off')
    
    plt.tight_layout()
    plt.savefig('execution_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Execution flow diagram saved as 'execution_flow_diagram.png'")

def create_performance_comparison_chart():
    """Create a performance comparison chart"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Performance data (example - actual results may vary)
    approaches = ['Async I/O', 'Threading', 'Hybrid', 'Multiprocessing']
    execution_times = [3.21, 4.12, 2.34, 5.03]
    memory_usage = [8, 64, 36, 40]  # MB
    
    # Execution time comparison
    bars1 = ax1.bar(approaches, execution_times, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'], alpha=0.7)
    ax1.set_title('Execution Time Comparison', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Time (seconds)')
    ax1.set_ylim(0, max(execution_times) * 1.2)
    
    # Add value labels on bars
    for bar, time in zip(bars1, execution_times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{time:.2f}s', ha='center', va='bottom', fontweight='bold')
    
    # Memory usage comparison
    bars2 = ax2.bar(approaches, memory_usage, color=['#4CAF50', '#2196F3', '#FF9800', '#9C27B0'], alpha=0.7)
    ax2.set_title('Memory Usage Comparison', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Memory (MB)')
    ax2.set_ylim(0, max(memory_usage) * 1.2)
    
    # Add value labels on bars
    for bar, memory in zip(bars2, memory_usage):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{memory}MB', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("Performance comparison chart saved as 'performance_comparison.png'")

if __name__ == "__main__":
    print("Creating execution flow diagrams...")
    create_execution_flow_diagram()
    
    print("\nCreating performance comparison charts...")
    create_performance_comparison_chart()
    
    print("\nDiagrams created successfully!")
    print("Files generated:")
    print("- execution_flow_diagram.png")
    print("- performance_comparison.png")
