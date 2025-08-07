#!/usr/bin/env python3
"""
Complete release script for torch-installer v1.0.3
Handles GitHub tagging and PyPI publishing
"""

import subprocess
import sys
import os
import argparse

def run_command(cmd, description, capture_output=False):
    """Run a command and handle errors."""
    print(f"🔧 {description}...")
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
            print(f"✅ {description} completed successfully")
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=True)
            print(f"✅ {description} completed successfully")
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if capture_output and e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_git_status():
    """Check if git working directory is clean."""
    print("🔍 Checking git status...")
    try:
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️ Git working directory is not clean:")
            print(result.stdout)
            response = input("Continue anyway? (y/N): ")
            return response.lower() == 'y'
        else:
            print("✅ Git working directory is clean")
            return True
    except subprocess.CalledProcessError:
        print("❌ Failed to check git status")
        return False

def create_git_tag(version):
    """Create and push git tag."""
    tag_name = f"v{version}"
    
    # Check if tag already exists
    try:
        subprocess.run(f"git rev-parse {tag_name}", shell=True, check=True, capture_output=True)
        print(f"⚠️ Tag {tag_name} already exists")
        response = input("Delete and recreate? (y/N): ")
        if response.lower() == 'y':
            run_command(f"git tag -d {tag_name}", f"Deleting local tag {tag_name}")
            run_command(f"git push origin --delete {tag_name}", f"Deleting remote tag {tag_name}")
        else:
            return False
    except subprocess.CalledProcessError:
        # Tag doesn't exist, which is good
        pass
    
    # Create new tag
    commit_msg = f"Release v{version} - Added GPU compatibility notice and bug fixes"
    if not run_command(f'git tag -a {tag_name} -m "{commit_msg}"', f"Creating tag {tag_name}"):
        return False
    
    if not run_command(f"git push origin {tag_name}", f"Pushing tag {tag_name}"):
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="Release torch-installer v1.0.3")
    parser.add_argument("--skip-git", action="store_true", help="Skip git operations")
    parser.add_argument("--skip-build", action="store_true", help="Skip building package")
    parser.add_argument("--test-pypi", action="store_true", help="Upload to TestPyPI instead of PyPI")
    parser.add_argument("--pypi-only", action="store_true", help="Only upload to PyPI, skip git")
    
    args = parser.parse_args()
    version = "1.0.3"
    
    print("🚀 Releasing torch-installer v1.0.3")
    print("=" * 50)
    print("📋 Release notes:")
    print("   • Fixed Pylance type checking errors")
    print("   • Improved torch.version.cuda attribute handling")
    print("   • Added proper type annotations")
    print("   • Fixed bare except clauses")
    print("   • Removed unnecessary f-strings")
    print("   • Added GPU compatibility notice")
    print("=" * 50)
    
    # Git operations
    if not args.skip_git and not args.pypi_only:
        if not check_git_status():
            print("❌ Git status check failed")
            return False
        
        # Commit current changes
        print("📝 Committing version updates...")
        run_command("git add .", "Staging changes")
        commit_msg = f"Bump version to {version} and add GPU compatibility notice"
        run_command(f'git commit -m "{commit_msg}"', "Committing changes")
        run_command("git push origin main", "Pushing to main branch")
        
        # Create and push tag
        if not create_git_tag(version):
            print("❌ Failed to create git tag")
            return False
    
    # Build package
    if not args.skip_build:
        if not run_command("python build_package.py", "Building package"):
            return False
    
    # Upload to PyPI
    upload_cmd = "python upload_package.py"
    if args.test_pypi:
        upload_cmd += " --test"
        print("🧪 Uploading to TestPyPI...")
    else:
        print("🌍 Uploading to PyPI...")
    
    if args.skip_build:
        upload_cmd += " --skip-build"
    
    if not run_command(upload_cmd, "Uploading package"):
        return False
    
    print("\n🎉 Release completed successfully!")
    print(f"✅ torch-installer v{version} is now available!")
    
    if not args.test_pypi:
        print("\n📦 Installation command:")
        print("   pip install torch-installer-coff33ninja")
        print("\n🔗 Links:")
        print("   • PyPI: https://pypi.org/project/torch-installer-coff33ninja/")
        print("   • GitHub: https://github.com/coff33ninja/torch-installer")
    else:
        print("\n🧪 Test installation command:")
        print("   pip install --index-url https://test.pypi.org/simple/ torch-installer-coff33ninja")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)