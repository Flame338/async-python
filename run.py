#!/usr/bin/env python3
"""
Simple launcher script - equivalent to a minimal main.c
=======================================================

This is the simplest entry point, similar to:

#include <stdio.h>
int main() {
    printf("Starting Concurrent File Reader...\n");
    // Run the main application
    return 0;
}
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Simple main function - like C main()"""
    print("🚀 Starting Concurrent File Reader...")
    print("=" * 50)
    
    # Check if main.py exists
    main_script = Path("main.py")
    if not main_script.exists():
        print("❌ Error: main.py not found!")
        return 1
    
    try:
        # Run the main application
        result = subprocess.run([sys.executable, "main.py"] + sys.argv[1:], 
                              check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running main application: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user.")
        return 0

if __name__ == "__main__":
    sys.exit(main())
