#!/usr/bin/env python3
"""
Build script for torch-installer package.
"""

import subprocess
import sys
import os
import shutil


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False


def clean_build():
    """Clean previous build artifacts."""
    print("🧹 Cleaning previous build artifacts...")
    dirs_to_clean = ['build', 'dist', 'torch_installer.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed {dir_name}/")


def main():
    """Main build process."""
    print("🚀 Building torch-installer package")
    print("=" * 50)
    
    # Clean previous builds
    clean_build()
    
    # Install build dependencies
    if not run_command("pip install --upgrade build twine", "Installing build dependencies"):
        return False
    
    # Build the package
    if not run_command("python -m build", "Building package"):
        return False
    
    # Check the built package
    if not run_command("python -m twine check dist/*", "Checking package"):
        return False
    
    print("\n✅ Package built successfully!")
    print("📦 Built files:")
    if os.path.exists('dist'):
        for file in os.listdir('dist'):
            print(f"   • dist/{file}")
    
    print("\n🚀 Next steps:")
    print("   1. Test the package locally: pip install dist/torch_installer-*.whl")
    print("   2. Upload to TestPyPI: python upload_package.py --test")
    print("   3. Upload to PyPI: python upload_package.py")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
