"""
PyTorch Installation Assistant

An intelligent, autonomous PyTorch installer that automatically detects your system,
GPU, and CUDA configuration to install the optimal PyTorch setup for your hardware.
"""

__version__ = "1.0.2"
__author__ = "coff33ninja"
__email__ = "your-email@example.com"
__license__ = "MIT"

from .installer import (
    get_system_info,
    detect_gpu_info,
    detect_cuda_version,
    install_torch,
    verify_cuda_tensor,
    verify_mps_tensor,
    show_installed_versions,
    is_torch_installed,
)

__all__ = [
    "get_system_info",
    "detect_gpu_info", 
    "detect_cuda_version",
    "install_torch",
    "verify_cuda_tensor",
    "verify_mps_tensor",
    "show_installed_versions",
    "is_torch_installed",
]