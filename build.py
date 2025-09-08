#!/usr/bin/env python3
"""
Build script for Concurrent File Reader
======================================

Equivalent to a Makefile for this Python project.
Handles setup, testing, and execution.
"""

import os
import sys
import subprocess
from pathlib import Path

class ProjectBuilder:
    """Build system for the project"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.scripts_dir = self.project_root / "scripts"
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = ['aiofiles', 'matplotlib', 'numpy']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package} (missing)")
                missing_packages.append(package)
        
        if missing_packages:
            print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
            subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        
        return len(missing_packages) == 0
    
    def setup_project(self):
        """Setup the project - equivalent to 'make setup'"""
        print("🛠️  Setting up project...")
        
        # Create necessary directories
        directories = ['sample_files', 'output', 'logs']
        for dir_name in directories:
            dir_path = self.project_root / dir_name
            dir_path.mkdir(exist_ok=True)
            print(f"  📁 Created directory: {dir_name}")
        
        # Check dependencies
        self.check_dependencies()
        
        print("✅ Project setup complete!")
    
    def build(self):
        """Build the project - equivalent to 'make build'"""
        print("🔨 Building project...")
        
        # In Python, "building" means checking syntax and imports
        python_files = list(self.project_root.glob("*.py")) + list(self.scripts_dir.glob("*.py"))
        
        for py_file in python_files:
            try:
                # Compile to check syntax
                with open(py_file, 'r') as f:
                    compile(f.read(), py_file, 'exec')
                print(f"  ✅ {py_file.name}")
            except SyntaxError as e:
                print(f"  ❌ {py_file.name}: {e}")
                return False
        
        print("✅ Build successful!")
        return True
    
    def test(self):
        """Run tests - equivalent to 'make test'"""
        print("🧪 Running tests...")
        
        # Simple test: try importing all modules
        test_imports = [
            'scripts.async_file_reader',
            'scripts.threaded_file_reader', 
            'scripts.hybrid_async_threaded_reader',
            'scripts.multiprocess_file_reader'
        ]
        
        for module in test_imports:
            try:
                __import__(module)
                print(f"  ✅ Import test: {module}")
            except ImportError as e:
                print(f"  ❌ Import test: {module} - {e}")
                return False
        
        print("✅ All tests passed!")
        return True
    
    def run(self, args=None):
        """Run the project - equivalent to 'make run'"""
        print("🚀 Running project...")
        
        cmd = [sys.executable, "main.py"]
        if args:
            cmd.extend(args)
        
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Run failed: {e}")
            return False
        
        return True
    
    def clean(self):
        """Clean build artifacts - equivalent to 'make clean'"""
        print("🧹 Cleaning project...")
        
        # Remove generated files
        patterns = ['*.pyc', '__pycache__', '*.png', 'sample_files/*']
        
        for pattern in patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    file_path.unlink()
                    print(f"  🗑️  Removed: {file_path}")
                elif file_path.is_dir() and file_path.name == '__pycache__':
                    import shutil
                    shutil.rmtree(file_path)
                    print(f"  🗑️  Removed directory: {file_path}")
        
        print("✅ Clean complete!")

def main():
    """Main build function"""
    builder = ProjectBuilder()
    
    if len(sys.argv) < 2:
        print("Usage: python build.py [setup|build|test|run|clean]")
        print("\nAvailable commands:")
        print("  setup  - Setup project dependencies and directories")
        print("  build  - Check syntax and compile Python files")
        print("  test   - Run basic import tests")
        print("  run    - Run the main application")
        print("  clean  - Remove generated files")
        return 1
    
    command = sys.argv[1]
    
    if command == "setup":
        builder.setup_project()
    elif command == "build":
        if not builder.build():
            return 1
    elif command == "test":
        if not builder.test():
            return 1
    elif command == "run":
        if not builder.run(sys.argv[2:]):
            return 1
    elif command == "clean":
        builder.clean()
    else:
        print(f"❌ Unknown command: {command}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
