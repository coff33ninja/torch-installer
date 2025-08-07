#!/usr/bin/env python3
"""Setup script for torch-installer package."""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read version from __init__.py
def get_version():
    version_file = os.path.join("torch_installer", "__init__.py")
    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    return "1.0.0"

setup(
    name="torch-installer-coff33ninja",
    version="1.0.3",
    author="coff33ninja",
    author_email="coff33ninja@gmail.com",  # Replace with your email
    description="An intelligent, autonomous PyTorch installer that automatically detects your system, GPU, and CUDA configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/coff33ninja/torch-installer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",

        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Installation/Setup",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "twine>=3.0",
            "build>=0.7",
        ],
    },
    entry_points={
        "console_scripts": [
            "torch-installer=torch_installer.cli:main",
            "pytorch-installer=torch_installer.cli:main",
        ],
    },
    keywords="pytorch torch cuda gpu installer machine-learning deep-learning",
    project_urls={
        "Bug Reports": "https://github.com/coff33ninja/torch-installer/issues",
        "Source": "https://github.com/coff33ninja/torch-installer",
        "Documentation": "https://github.com/coff33ninja/torch-installer#readme",
    },
)