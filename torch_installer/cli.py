#!/usr/bin/env python3
"""
Command-line interface for torch-installer package.
"""

import sys
from .installer import main as installer_main

def main():
    """Entry point for the torch-installer CLI."""
    try:
        installer_main()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()