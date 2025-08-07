# 🚀 PyTorch Installation Assistant

An intelligent, autonomous PyTorch installer that automatically detects your system, GPU, and CUDA configuration to install the optimal PyTorch setup for your hardware.

## ✨ Features

- **🧠 Intelligent GPU Detection**: Automatically detects NVIDIA, AMD, and Apple Silicon GPUs
- **🎯 Smart CUDA Matching**: Finds the best PyTorch version for your CUDA installation
- **🤖 Autonomous CUDA Installation**: Automatically installs CUDA on Windows using package managers
- **📦 Complete Ecosystem**: Installs torch, torchvision, and torchaudio with version compatibility
- **🔄 Fallback Logic**: Handles older CUDA versions and compatibility issues gracefully
- **🎮 Hardware-Specific Optimization**: Tailored recommendations for different GPU generations
- **🔍 Comprehensive Testing**: Post-install verification with tensor operations
- **📊 Detailed Reporting**: Shows complete system and package information

## �️ Installation

Simply download the `torch_installer.py` script - no additional dependencies required beyond Python's standard library.

```bash
# Download the script
curl -O https://raw.githubusercontent.com/coff33ninja/torch-installer/main/torch_installer.py

# Or clone the repository
git clone https://github.com/coff33ninja/torch-installer.git
cd torch-installer/pytorch-installer.git
```

## 🚀 Quick Start

### Basic Installation
```bash
# Automatic installation with smart detection
python torch_installer.py

# CPU-only installation
python torch_installer.py --cpu-only

# Force specific CUDA version
python torch_installer.py --force-cuda cu121
```

### CUDA Auto-Installation (Windows Only)
```bash
# Auto-install recommended CUDA version
python torch_installer.py --auto-install-cuda

# Install specific CUDA version
python torch_installer.py --auto-install-cuda --cuda-version 12.1

# Dry-run to see what would be installed
python torch_installer.py --auto-install-cuda --dry-run
```

## � Commnand Reference

### Core Installation Commands

| Command | Description | Example |
|---------|-------------|---------|
| `python torch_installer.py` | Auto-detect and install optimal PyTorch | Basic usage |
| `--cpu-only` | Force CPU-only installation | `python torch_installer.py --cpu-only` |
| `--force-cuda cu121` | Force specific CUDA version | `python torch_installer.py --force-cuda cu121` |
| `--force-reinstall` | Reinstall even if PyTorch exists | `python torch_installer.py --force-reinstall` |

### CUDA Management (Windows)

| Command | Description | Example |
|---------|-------------|---------|
| `--auto-install-cuda` | Automatically install CUDA | `python torch_installer.py --auto-install-cuda` |
| `--cuda-version 12.1` | Specify CUDA version to install | `python torch_installer.py --auto-install-cuda --cuda-version 12.1` |

### Information & Diagnostics

| Command | Description | Example |
|---------|-------------|---------|
| `--gpu-info` | Show GPU and CUDA compatibility | `python torch_installer.py --gpu-info` |
| `--show-versions` | Display installed PyTorch ecosystem | `python torch_installer.py --show-versions` |
| `--show-matching` | Demo CUDA version matching logic | `python torch_installer.py --show-matching` |
| `--list-cuda` | List supported CUDA versions | `python torch_installer.py --list-cuda` |

### Development & Testing

| Command | Description | Example |
|---------|-------------|---------|
| `--dry-run` | Show commands without executing | `python torch_installer.py --dry-run` |
| `--log` | Log all output to timestamped file | `python torch_installer.py --log` |

## 🎮 GPU Support Matrix

### NVIDIA GPUs

| GPU Generation | Recommended CUDA | PyTorch Support | Performance |
|----------------|------------------|-----------------|-------------|
| **RTX 40 Series** | CUDA 12.1+ | ✅ Excellent | 🔥🔥🔥🔥🔥 |
| **RTX 30 Series** | CUDA 12.1+ | ✅ Excellent | 🔥🔥🔥🔥🔥 |
| **RTX 20 Series** | CUDA 11.8+ | ✅ Excellent | 🔥🔥🔥🔥 |
| **GTX 16 Series** | CUDA 11.8+ | ✅ Very Good | 🔥🔥🔥🔥 |
| **GTX 10 Series** | CUDA 11.8+ | ✅ Good | 🔥🔥🔥 |
| **GT 700 Series** | CUDA 11.8 | ⚠️ Limited | 🔥🔥 |
| **Older GPUs** | Manual Install | ❌ Not Recommended | 🔥 |

### Other GPUs

| GPU Type | Support | Recommendation |
|----------|---------|----------------|
| **Apple Silicon (M1/M2/M3)** | ✅ MPS Support | Automatic detection |
| **AMD GPUs** | ⚠️ ROCm (Linux only) | Manual ROCm installation |
| **Intel GPUs** | ❌ Not supported | Use CPU-only mode |

## 🔧 Usage Examples

### Scenario 1: First-time Installation
```bash
# Let the installer detect everything automatically
python torch_installer.py

# Output example:
# 🚀 PyTorch Installation Assistant
# 🎮 Detected GPU: GeForce RTX 3080
# 🚀 Detected CUDA version: 12.1
# 🎯 Installing PyTorch with CUDA 121 wheels
# ✅ PyTorch installation completed successfully!
```

### Scenario 2: Upgrading CUDA and PyTorch
```bash
# Auto-install newer CUDA version
python torch_installer.py --auto-install-cuda --cuda-version 12.1

# Then reinstall PyTorch
python torch_installer.py --force-reinstall
```

### Scenario 3: Troubleshooting Installation
```bash
# Check current setup
python torch_installer.py --show-versions

# See GPU compatibility
python torch_installer.py --gpu-info

# Test what would be installed
python torch_installer.py --dry-run
```

### Scenario 4: Development Environment
```bash
# Install with logging for debugging
python torch_installer.py --log

# Check CUDA matching logic
python torch_installer.py --show-matching
```

## 🧠 Intelligent Features

### Smart CUDA Version Matching

The installer automatically matches your CUDA version to compatible PyTorch versions:

```
🔍 Detected CUDA: 11.1
📋 Supported versions: ['121', '118', '117', '116', '113']
⚠️ Fallback match: CUDA 111 -> PyTorch cu113 (oldest supported)
✅ Would install: PyTorch 2.0.1 with CUDA 111
📦 Full package set: torch=2.0.1, torchvision=0.15.2, torchaudio=2.0.2
```

### GPU-Specific Recommendations

For older GPUs:
```
💡 GPU ACCELERATION UPGRADE GUIDE (GeForce GT 710):
   ⚠️ Your GeForce GT 710 is an older GPU with limited CUDA support
   💡 Recommended: CUDA 11.8 for optimal compatibility
   🤖 AUTOMATIC INSTALLATION AVAILABLE:
   • Run: python torch_installer.py --auto-install-cuda
```

For modern GPUs:
```
💡 GPU ACCELERATION UPGRADE GUIDE (GeForce RTX 3080):
   🚀 Your GeForce RTX 3080 supports modern CUDA versions
   ✨ Recommended: CUDA 12.1 for best performance
   🤖 AUTOMATIC INSTALLATION AVAILABLE:
   • Run: python torch_installer.py --auto-install-cuda
```

## 🔍 System Information Display

### Complete Ecosystem View
```bash
python torch_installer.py --show-versions

# Output:
# 📊 Installed PyTorch Ecosystem:
#    🔥 PyTorch: 2.8.0+cu121
#    👁️ TorchVision: 0.23.0+cu121
#    🔊 TorchAudio: 2.8.0+cu121
#    🎯 CUDA Support: True
#    🚀 CUDA Version: 12.1
#    🎮 GPU Count: 1
#    🎮 GPU 0: GeForce RTX 3080
```

### GPU Compatibility Analysis
```bash
python torch_installer.py --gpu-info

# Output:
# 🎮 GPU and CUDA Compatibility Information
# 🎮 Detected GPU: GeForce RTX 3080
# 💾 GPU Memory: 10240MB
# 🔍 Detected CUDA: 12.1
# ✅ Latest PyTorch supports your CUDA via cu121
```

## 🤖 CUDA Auto-Installation (Windows)

### Prerequisites
- Windows 10/11
- NVIDIA GPU with compatible drivers
- Package manager: winget (built-in) or chocolatey

### Installation Process
1. **Detection**: Identifies your GPU model and current CUDA version
2. **Recommendation**: Suggests optimal CUDA version for your hardware
3. **Package Manager Check**: Verifies winget or chocolatey availability
4. **Version Matching**: Finds compatible CUDA version in repositories
5. **Installation**: Automatically downloads and installs CUDA
6. **Verification**: Confirms successful installation

### Example Output
```bash
python torch_installer.py --auto-install-cuda

# 🤖 CUDA Auto-Installation Mode
# 🎮 Detected GPU: GeForce RTX 3080
# 📋 Current CUDA: 11.8
# 🔧 Attempting to install CUDA 12.1 for GeForce RTX 3080
# 📦 Trying winget (Windows Package Manager)...
# ✅ Found CUDA versions in winget: 13.0, 12.9, 12.1...
# 🔧 Installing CUDA 12.1 via winget...
# ✅ Successfully installed CUDA 12.1
# 🔄 Please restart your command prompt and run the installer again
```

## 🔧 Advanced Configuration

### Environment Variables
- `CUDA_HOME`: Override CUDA installation path detection
- `PYTORCH_CUDA_ALLOC_CONF`: Configure CUDA memory allocation

### Custom Package Managers
The installer supports:
- **winget**: Native Windows package manager (recommended)
- **chocolatey**: Third-party package manager with more versions

### Offline Installation
For air-gapped environments:
1. Download PyTorch wheels manually from https://pytorch.org/get-started/locally/
2. Use `pip install` with local wheel files
3. Run installer with `--show-versions` to verify

## 🐛 Troubleshooting

### Common Issues

#### "CUDA not available" after installation
```bash
# Check CUDA installation
nvidia-smi

# Verify PyTorch CUDA support
python -c "import torch; print(torch.cuda.is_available())"

# Reinstall with force
python torch_installer.py --force-reinstall
```

#### Package manager not found (Windows)
```bash
# Install chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

# Or update Windows for winget (Windows 10)
# winget is included in Windows 11 by default
```

#### Older CUDA version detected
```bash
# Check what would be installed
python torch_installer.py --show-matching

# Auto-upgrade CUDA (Windows)
python torch_installer.py --auto-install-cuda

# Or force specific PyTorch version
python torch_installer.py --force-cuda cu118
```

### Debug Mode
```bash
# Enable detailed logging
python torch_installer.py --log --dry-run

# Check system compatibility
python torch_installer.py --gpu-info --show-versions
```

## 🔄 Update & Maintenance

### Updating PyTorch
```bash
# Check for updates and reinstall
python torch_installer.py --force-reinstall

# Upgrade to specific version
python torch_installer.py --force-cuda cu121 --force-reinstall
```

### Updating CUDA (Windows)
```bash
# Auto-install latest compatible version
python torch_installer.py --auto-install-cuda

# Install specific version
python torch_installer.py --auto-install-cuda --cuda-version 12.1
```

## 🤝 Contributing

### Reporting Issues
When reporting issues, please include:
```bash
# System information
python torch_installer.py --gpu-info --show-versions --log

# Attach the generated log file
```

### Feature Requests
- GPU support for additional vendors
- Package manager support for other platforms
- Integration with conda/mamba environments

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NVIDIA** for CUDA toolkit and GPU drivers
- **PyTorch Team** for the excellent deep learning framework
- **Microsoft** for winget package manager
- **Chocolatey** community for package management on Windows

---

## 📞 Support

For support and questions:
- 📧 Create an issue on GitHub
- 💬 Join the discussion in GitHub Discussions
- 📖 Check the troubleshooting section above

**Happy Deep Learning! 🚀🔥**