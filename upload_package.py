#!/usr/bin/env python3
"""
Upload script for torch-installer package to PyPI.
"""

import subprocess
import sys
import os
import argparse

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False

def check_dist_files():
    """Check if distribution files exist."""
    if not os.path.exists('dist'):
        print("❌ No dist/ directory found. Run build_package.py first.")
        return False
    
    dist_files = os.listdir('dist')
    if not dist_files:
        print("❌ No files in dist/ directory. Run build_package.py first.")
        return False
    
    print("📦 Found distribution files:")
    for file in dist_files:
        print(f"   • {file}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Upload torch-installer to PyPI")
    parser.add_argument("--test", action="store_true", 
                       help="Upload to TestPyPI instead of PyPI")
    parser.add_argument("--skip-build", action="store_true",
                       help="Skip building and just upload existing dist files")
    
    args = parser.parse_args()
    
    print("🚀 Uploading torch-installer package")
    print("=" * 50)
    
    # Build package if not skipping
    if not args.skip_build:
        print("🔨 Building package first...")
        if not run_command("python build_package.py", "Building package"):
            return False
    
    # Check distribution files
    if not check_dist_files():
        return False
    
    # Install/upgrade twine
    if not run_command("pip install --upgrade twine", "Installing/upgrading twine"):
        return False
    
    # Upload to appropriate repository
    if args.test:
        print("🧪 Uploading to TestPyPI...")
        cmd = "python -m twine upload --repository testpypi dist/*"
        print("\n📝 Note: You'll need TestPyPI credentials.")
        print("   Create account at: https://test.pypi.org/account/register/")
        print("   Generate API token at: https://test.pypi.org/manage/account/token/")
    else:
        print("🌍 Uploading to PyPI...")
        cmd = "python -m twine upload dist/*"
        print("\n📝 Note: You'll need PyPI credentials.")
        print("   Create account at: https://pypi.org/account/register/")
        print("   Generate API token at: https://pypi.org/manage/account/token/")
    
    print(f"\n🔧 Running: {cmd}")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        
        if args.test:
            print("\n✅ Package uploaded to TestPyPI successfully!")
            print("🧪 Test installation with:")
            print("   pip install --index-url https://test.pypi.org/simple/ torch-installer")
        else:
            print("\n✅ Package uploaded to PyPI successfully!")
            print("🎉 Users can now install with:")
            print("   pip install torch-installer")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Upload failed with exit code {e.returncode}")
        print("\n💡 Common issues:")
        print("   • Invalid credentials - check your API token")
        print("   • Version already exists - increment version number")
        print("   • Package name conflicts - choose a different name")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)