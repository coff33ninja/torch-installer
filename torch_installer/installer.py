#!/usr/bin/env python3
"""
PyTorch Installation Assistant

An intelligent, autonomous PyTorch installer that automatically detects your system,
GPU, and CUDA configuration to install the optimal PyTorch setup for your hardware.
"""

import subprocess
import sys
import re
import platform
import shutil
import urllib.request
import argparse
import datetime

__version__ = "1.0.0"


def get_system_info():
    """Get detailed system information using platform module"""
    info = {
        'system': platform.system(),
        'machine': platform.machine(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'platform': platform.platform()
    }
    
    print(f"🖥️  System: {info['system']} {info['architecture']}")
    print(f"🔧 Machine: {info['machine']}")
    print(f"🐍 Python: {info['python_version']}")
    
    return info


def run(cmd, capture=False, dry_run=False):
    print(f"🔧 Running: {cmd}")
    if dry_run:
        print("💡 Dry run enabled - command not executed")
        return True
    try:
        if capture:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL)
            return result.decode().strip()
        else:
            subprocess.check_call(cmd, shell=True)
            return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with error: {e}")
        return None


def is_torch_installed():
    try:
        import torch
        version = torch.__version__
        cuda_available = torch.cuda.is_available()
        
        print(f"✅ PyTorch already installed. Version: {version}")
        
        # Show complete ecosystem versions
        try:
            import torchvision
            import torchaudio
            print(f"📦 Complete ecosystem: torch={version}, torchvision={torchvision.__version__}, torchaudio={torchaudio.__version__}")
        except ImportError as e:
            print(f"⚠️ Some PyTorch packages missing: {e}")
        
        if "+cpu" in version:
            print("⚠️ CPU-only version detected")
            return "cpu-only"
        elif cuda_available:
            cuda_version = torch.version.cuda
            print(f"🎯 CUDA-enabled version with CUDA {cuda_version}")
            return "cuda-enabled"
        else:
            print("⚠️ CUDA version installed but CUDA not available")
            return "cuda-broken"
    except ImportError:
        return False


def detect_gpu_info():
    """Detect GPU information including model and CUDA support"""
    gpu_info = {
        'model': None,
        'cuda_version': None,
        'compute_capability': None,
        'memory': None
    }
    
    smi = shutil.which("nvidia-smi")
    if smi:
        output = run("nvidia-smi", capture=True)
        if output:
            # Extract GPU model - look for the GPU name in the table
            gpu_match = re.search(r"\|\s+\d+\s+(GeForce|Quadro|Tesla|RTX|GTX|GT)\s+([A-Za-z0-9\s]+?)\s+(?:WDDM|TCC)", output)
            if gpu_match:
                gpu_info['model'] = f"{gpu_match.group(1)} {gpu_match.group(2).strip()}"
            else:
                # Fallback pattern for different nvidia-smi formats
                gpu_match = re.search(r"(GeForce|Quadro|Tesla|RTX|GTX|GT)\s+([A-Za-z0-9\s]+)", output.split('\n')[7] if len(output.split('\n')) > 7 else "")
                if gpu_match:
                    gpu_info['model'] = f"{gpu_match.group(1)} {gpu_match.group(2).split()[0]}"
            
            # Extract CUDA version
            cuda_match = re.search(r"CUDA Version: (\d+\.\d+)", output)
            if cuda_match:
                gpu_info['cuda_version'] = cuda_match.group(1)
            
            # Extract memory
            memory_match = re.search(r"(\d+)MiB\s*/\s*(\d+)MiB", output)
            if memory_match:
                gpu_info['memory'] = f"{memory_match.group(2)}MB"
    
    return gpu_info


def detect_cuda_version(system_info):
    """Detect CUDA version with platform-specific logic"""
    system = system_info['system']
    
    if system == "Windows":
        print("🪟 Windows detected - checking for CUDA...")
        # On Windows, try nvidia-smi first
        smi = shutil.which("nvidia-smi")
        if smi:
            output = run("nvidia-smi", capture=True)
            if output:
                match = re.search(r"CUDA Version: (\d+\.\d+)", output)
                if match:
                    version = match.group(1).replace('.', '')
                    print(f"🚀 Detected CUDA version via nvidia-smi: {match.group(1)}")
                    return version
    
    elif system == "Linux":
        print("🐧 Linux detected - checking for CUDA...")
        # Try nvidia-smi first
        smi = shutil.which("nvidia-smi")
        if smi:
            output = run("nvidia-smi", capture=True)
            if output:
                match = re.search(r"CUDA Version: (\d+\.\d+)", output)
                if match:
                    version = match.group(1).replace('.', '')
                    print(f"🚀 Detected CUDA version via nvidia-smi: {match.group(1)}")
                    return version
        
        # Try nvcc fallback on Linux
        nvcc = shutil.which("nvcc")
        if nvcc:
            output = run("nvcc --version", capture=True)
            if output:
                match = re.search(r"release (\d+\.\d+)", output)
                if match:
                    version = match.group(1).replace('.', '')
                    print(f"🚀 Detected CUDA version via nvcc: {match.group(1)}")
                    return version
    
    elif system == "Darwin":
        print("🍎 macOS detected - CUDA not supported, will use CPU or MPS")
        return "mps"  # Metal Performance Shaders for Apple Silicon
    
    print(f"🧱 No CUDA version detected on {system} (CPU only).")
    return None


def get_supported_cuda_versions():
    """Dynamically fetch supported CUDA versions from PyTorch, with fallback"""
    fallback_versions = ['121', '118', '117', '116', '113']  # Known working versions
    
    try:
        print("🌐 Checking for latest supported CUDA versions...")
        # Try to get the latest info from PyTorch's wheel index
        url = "https://download.pytorch.org/whl/"
        with urllib.request.urlopen(url, timeout=5) as response:
            content = response.read().decode('utf-8')
            # Extract CUDA versions from the HTML (look for cu### patterns)
            cuda_matches = re.findall(r'cu(\d{3})', content)
            if cuda_matches:
                # Get unique versions and sort them (newest first)
                versions = sorted(list(set(cuda_matches)), reverse=True)
                print(f"✅ Found supported CUDA versions: {', '.join(versions)}")
                return versions[:6]  # Return top 6 most recent
    except Exception as e:
        print(f"⚠️ Could not fetch latest CUDA versions ({e}), using fallback list")
    
    print(f"📋 Using fallback CUDA versions: {', '.join(fallback_versions)}")
    return fallback_versions


def get_pytorch_versions_for_cuda(cuda_version):
    """Get PyTorch versions that support a specific CUDA version (currently available)"""
    # Updated mapping based on what's actually available in PyTorch repositories
    cuda_pytorch_compatibility = {
        # CUDA 11.1 and 11.3 wheels are no longer available
        "111": [],  # No longer supported - recommend CUDA upgrade
        "113": [],  # No longer supported - recommend CUDA upgrade  
        "116": [("2.1.2", "0.16.2", "2.1.2")],  # Limited availability
        "117": [("2.2.2", "0.17.2", "2.2.2"), ("2.1.2", "0.16.2", "2.1.2")],
        "118": [("2.8.0", "0.23.0", "2.8.0"), ("2.4.1", "0.19.1", "2.4.1")],
        "121": [("2.8.0", "0.23.0", "2.8.0"), ("2.4.1", "0.19.1", "2.4.1")]
    }
    
    return cuda_pytorch_compatibility.get(cuda_version, [])


def find_best_pytorch_version(detected_cuda):
    """Find the best PyTorch version for the detected CUDA version"""
    if not detected_cuda:
        return None, None, None
    
    # Get compatible PyTorch versions for this CUDA version
    compatible_versions = get_pytorch_versions_for_cuda(detected_cuda)
    
    if compatible_versions:
        # Return the newest compatible version (first in list)
        torch_ver, vision_ver, audio_ver = compatible_versions[0]
        detected_major_minor = f"{detected_cuda[:2]}.{detected_cuda[2:]}" if len(detected_cuda) == 3 else detected_cuda
        print(f"🎯 Found compatible PyTorch {torch_ver} for CUDA {detected_major_minor}")
        return torch_ver, vision_ver, audio_ver
    
    return None, None, None


def find_best_cuda_match(detected_version, supported_versions):
    """Find the best matching CUDA version for PyTorch installation"""
    if not detected_version or not supported_versions:
        return None
    
    # Convert detected version to int for comparison (e.g., "121" -> 121)
    try:
        detected_int = int(detected_version)
    except ValueError:
        return None
    
    # Convert supported versions to ints and sort
    supported_ints = []
    for version in supported_versions:
        try:
            supported_ints.append((int(version), version))
        except ValueError:
            continue
    
    supported_ints.sort(reverse=True)  # Newest first
    
    # Find exact match first
    for version_int, version_str in supported_ints:
        if version_int == detected_int:
            print(f"🎯 Perfect match found: CUDA {detected_version} -> PyTorch cu{version_str}")
            return version_str
    
    # Find closest lower version (backward compatibility)
    best_match = None
    for version_int, version_str in supported_ints:
        if version_int <= detected_int:
            best_match = version_str
            break
    
    if best_match:
        detected_major_minor = f"{detected_version[:2]}.{detected_version[2:]}" if len(detected_version) == 3 else detected_version
        match_major_minor = f"{best_match[:2]}.{best_match[2:]}" if len(best_match) == 3 else best_match
        print(f"🔄 Smart match: CUDA {detected_major_minor} -> PyTorch cu{best_match} (CUDA {match_major_minor} compatible)")
        return best_match
    
    # If no lower version found, try the oldest supported (last resort)
    if supported_ints:
        oldest = supported_ints[-1][1]
        print(f"⚠️ Fallback match: CUDA {detected_version} -> PyTorch cu{oldest} (oldest supported)")
        print("💡 This might not be optimal - consider upgrading or using --cpu-only")
        return oldest
    
    return None


def install_torch(cuda_version=None, system_info=None, force_cuda=None, dry_run=False, force_reinstall=False):
    """Install PyTorch with platform-specific optimizations and intelligent CUDA matching"""
    base_cmd = [sys.executable, "-m", "pip", "install", "--upgrade"]
    
    # Add force reinstall flags if needed
    if force_reinstall:
        base_cmd.extend(["--force-reinstall", "--no-deps"])
        print("🔄 Force reinstall mode - will reinstall PyTorch packages")
    system = system_info['system'] if system_info else platform.system()
    
    # Handle force CUDA override
    if force_cuda:
        cuda_version = force_cuda
        print(f"🔧 Force installing with CUDA version: {cuda_version}")
    
    if cuda_version == "mps" and system == "Darwin":
        # macOS with Apple Silicon - use default PyTorch with MPS support
        print("🍎 Installing PyTorch with MPS (Metal) support for Apple Silicon...")
        cmd = base_cmd + ["torch", "torchvision", "torchaudio"]
    elif cuda_version and cuda_version != "mps":
        # CUDA installation for Windows/Linux with intelligent matching
        cuda_versions_supported = get_supported_cuda_versions()
        
        if force_cuda:
            # Force mode - use exactly what user specified
            if cuda_version in cuda_versions_supported:
                matched_version = cuda_version
                # Use latest PyTorch with this CUDA version
                extra_index_url = f"https://download.pytorch.org/whl/cu{matched_version}"
                print(f"🎯 Installing latest PyTorch with CUDA {matched_version} wheels for {system}...")
                print("📦 Using --extra-index-url for safer package resolution...")
                cmd = base_cmd + ["torch", "torchvision", "torchaudio", f"--extra-index-url={extra_index_url}"]
            else:
                print(f"⚠️ Forced CUDA version cu{cuda_version} not in supported list: {cuda_versions_supported}")
                print("🚀 Proceeding anyway as requested...")
                matched_version = cuda_version
                extra_index_url = f"https://download.pytorch.org/whl/cu{matched_version}"
                cmd = base_cmd + ["torch", "torchvision", "torchaudio", f"--extra-index-url={extra_index_url}"]
        else:
            # Smart matching mode - try current PyTorch first, then fallback to older versions
            matched_version = find_best_cuda_match(cuda_version, cuda_versions_supported)
            
            if matched_version:
                # Check if current PyTorch actually has wheels for this CUDA version
                print(f"🔍 Checking if latest PyTorch has CUDA {matched_version} wheels...")
                
                # For older CUDA versions, automatically use compatible older PyTorch
                if int(matched_version) < 116:  # CUDA versions older than 11.6
                    print(f"⚠️ CUDA {matched_version} is older - using compatible PyTorch version...")
                    torch_ver, vision_ver, audio_ver = find_best_pytorch_version(cuda_version)
                    
                    if torch_ver:
                        print(f"🔄 Installing PyTorch {torch_ver} with native CUDA {cuda_version} support...")
                        extra_index_url = f"https://download.pytorch.org/whl/cu{cuda_version}"
                        cmd = base_cmd + [
                            f"torch=={torch_ver}+cu{cuda_version}",
                            f"torchvision=={vision_ver}+cu{cuda_version}",
                            f"torchaudio=={audio_ver}",
                            f"--extra-index-url={extra_index_url}"
                        ]
                    else:
                        print(f"❌ No compatible PyTorch version found for CUDA {cuda_version}")
                        print("💡 Falling back to CPU-only install.")
                        cmd = base_cmd + ["torch", "torchvision", "torchaudio"]
                else:
                    # Try latest PyTorch with matched CUDA version
                    extra_index_url = f"https://download.pytorch.org/whl/cu{matched_version}"
                    print(f"🎯 Installing latest PyTorch with CUDA {matched_version} wheels for {system}...")
                    print("📦 Using --extra-index-url for safer package resolution...")
                    cmd = base_cmd + ["torch", "torchvision", "torchaudio", f"--extra-index-url={extra_index_url}"]
            else:
                # No match in current PyTorch - try older compatible versions
                print(f"⚠️ Current PyTorch doesn't support CUDA {cuda_version}")
                torch_ver, vision_ver, audio_ver = find_best_pytorch_version(cuda_version)
                
                if torch_ver:
                    print(f"🔄 Installing compatible PyTorch {torch_ver} with CUDA {cuda_version} support...")
                    extra_index_url = f"https://download.pytorch.org/whl/cu{cuda_version}"
                    cmd = base_cmd + [
                        f"torch=={torch_ver}+cu{cuda_version}",
                        f"torchvision=={vision_ver}+cu{cuda_version}",
                        f"torchaudio=={audio_ver}",
                        f"--extra-index-url={extra_index_url}"
                    ]
                else:
                    print(f"❌ No compatible PyTorch version found for CUDA {cuda_version}")
                    print("💡 SOLUTION: Upgrade CUDA to 11.8+ or 12.1+ for GPU acceleration")
                    print("📥 Download from: https://developer.nvidia.com/cuda-downloads")
                    print("🔄 Falling back to CPU-only install for now...")
                    cmd = base_cmd + ["torch", "torchvision", "torchaudio"]
    else:
        print(f"📦 Installing CPU-only PyTorch for {system}...")
        cmd = base_cmd + ["torch", "torchvision", "torchaudio"]
    
    # Add platform-specific optimizations
    if system == "Windows" and system_info and system_info['architecture'] == '64bit':
        print("🪟 Using Windows x64 optimizations...")
    elif system == "Linux" and system_info and 'x86_64' in system_info['machine']:
        print("🐧 Using Linux x86_64 optimizations...")
    
    if dry_run:
        print("💡 Dry run enabled. Install command would be:")
        print(f"   {' '.join(cmd)}")
        
        # Show package breakdown for specific versions
        if any("==" in arg for arg in cmd):
            print("📦 Package versions to be installed:")
            for arg in cmd:
                if "torch==" in arg:
                    print(f"   • {arg}")
                elif "torchvision==" in arg:
                    print(f"   • {arg}")
                elif "torchaudio==" in arg:
                    print(f"   • {arg}")
        return
    
    run(" ".join(cmd))


def verify_cuda_tensor():
    """Post-install CUDA tensor sanity test"""
    try:
        import torch  # noqa: F401 - Import needed for runtime check
        if torch.cuda.is_available():
            print("🧪 Running CUDA tensor test...")
            x = torch.rand(2, 2).cuda()
            # Perform a simple operation to verify CUDA works
            result = x * 2 + 1
            print("✅ CUDA tensor operation succeeded:")
            print(f"   Sample result: {result[0, :2].cpu().numpy()}")
            return True
        else:
            print("⚠️ CUDA not available at runtime.")
            return False
    except ImportError:
        print("❌ PyTorch not found - cannot run CUDA test")
        return False
    except Exception as e:
        print(f"❌ CUDA test failed: {e}")
        return False


def verify_mps_tensor():
    """Post-install MPS tensor sanity test for Apple Silicon"""
    try:
        import torch  # noqa: F401 - Import needed for runtime check
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("🧪 Running MPS tensor test...")
            x = torch.rand(2, 2).to('mps')
            # Perform a simple operation to verify MPS works
            result = x * 2 + 1
            print("✅ MPS tensor operation succeeded:")
            print(f"   Sample result: {result[0, :2].cpu().numpy()}")
            return True
        else:
            print("⚠️ MPS not available at runtime.")
            return False
    except ImportError:
        print("❌ PyTorch not found - cannot run MPS test")
        return False
    except Exception as e:
        print(f"❌ MPS test failed: {e}")
        return False


def get_gpu_upgrade_guidance(gpu_info, detected_cuda, auto_install=False):
    """Provide GPU-specific upgrade guidance with optional auto-install"""
    if not gpu_info['model']:
        return [
            "� GPU  ACCELERATION UPGRADE GUIDE:",
            "   1. Ensure you have an NVIDIA GPU installed",
            "   2. Download CUDA 11.8+ or 12.1+ from https://developer.nvidia.com/cuda-downloads",
            "   3. Install the new CUDA version",
            "   4. Run this installer again for automatic GPU support"
        ]
    
    gpu_model = gpu_info['model']
    guidance = [f"💡 GPU ACCELERATION UPGRADE GUIDE ({gpu_model}):"]
    
    # Determine recommended CUDA version and add auto-install option
    if any(kepler_gpu in gpu_model.upper() for kepler_gpu in ['GT 610', 'GT 620', 'GT 630', 'GT 710', 'GT 720', 'GT 730']):
        recommended_cuda = "11.3"  # Kepler generation - max CUDA 11.4, but 11.3 is most stable
        guidance.extend([
            f"   ⚠️ Your {gpu_model} is a Kepler-generation GPU (2012-2014)",
            f"   💡 Recommended: CUDA {recommended_cuda} for maximum compatibility",
            f"   🔧 Note: CUDA 11.8+ may cause driver conflicts (exit code 46)"
        ])
    elif any(modern_gpu in gpu_model.upper() for modern_gpu in ['RTX', 'GTX 16', 'GTX 20', 'GTX 30', 'GTX 40']):
        recommended_cuda = "12.1"
        guidance.extend([
            f"   🚀 Your {gpu_model} supports modern CUDA versions",
            f"   ✨ Recommended: CUDA {recommended_cuda} for best performance"
        ])
    else:
        recommended_cuda = "11.8"
        guidance.extend([
            f"   🎮 Detected GPU: {gpu_model}",
            f"   💡 Recommended: CUDA {recommended_cuda} for compatibility"
        ])
    
    # Add installation options
    if platform.system() == "Windows" and auto_install:
        managers = check_package_manager()
        if managers['winget'] or managers['choco']:
            guidance.extend([
                "   🤖 AUTOMATIC INSTALLATION AVAILABLE:",
                f"   • Run: python torch_installer.py --auto-install-cuda",
                f"   • This will install CUDA {recommended_cuda} automatically"
            ])
        else:
            guidance.extend([
                "   📦 Install a package manager first:",
                "   • winget (included in Windows 11, available for Windows 10)",
                "   • Or chocolatey: https://chocolatey.org/install"
            ])
    else:
        guidance.extend([
            f"   1. Download CUDA {recommended_cuda} from:",
            "      https://developer.nvidia.com/cuda-downloads",
            "   2. Install the new CUDA version",
            "   3. Run this installer again for GPU acceleration"
        ])
    
    if detected_cuda:
        detected_readable = f"{detected_cuda[:2]}.{detected_cuda[2:]}" if len(detected_cuda) == 3 else detected_cuda
        guidance.append(f"   📋 Current CUDA {detected_readable} is too old for modern PyTorch")
    
    return guidance


def check_package_manager():
    """Check which package managers are available on Windows"""
    managers = {}
    
    # Check for winget
    if shutil.which("winget"):
        managers['winget'] = True
    else:
        managers['winget'] = False
    
    # Check for chocolatey
    if shutil.which("choco"):
        managers['choco'] = True
    else:
        managers['choco'] = False
    
    return managers


def get_available_cuda_versions(package_manager):
    """Get available CUDA versions from package managers"""
    versions = []
    
    if package_manager == 'winget':
        try:
            output = run("winget show NVIDIA.CUDA --versions", capture=True)
            if output:
                # Parse winget output for versions
                lines = output.split('\n')
                for line in lines:
                    if re.match(r'^\d+\.\d+', line.strip()):
                        versions.append(line.strip())
        except:
            pass
    
    elif package_manager == 'choco':
        try:
            output = run("choco info cuda --all-versions", capture=True)
            if output:
                # Parse chocolatey output for versions
                version_matches = re.findall(r'(\d+\.\d+\.\d+(?:\.\d+)?)', output)
                versions = list(set(version_matches))  # Remove duplicates
        except:
            pass
    
    return sorted(versions, reverse=True)  # Newest first


def install_cuda_windows(target_version, gpu_info, dry_run=False):
    """Install CUDA on Windows using package managers"""
    if platform.system() != "Windows":
        return False, "CUDA auto-install only supported on Windows"
    
    managers = check_package_manager()
    gpu_model = gpu_info.get('model', 'Unknown GPU')
    
    print(f"🔧 Attempting to install CUDA {target_version} for {gpu_model}")
    
    # Determine best CUDA version for the GPU
    if any(kepler_gpu in gpu_model.upper() for kepler_gpu in ['GT 610', 'GT 620', 'GT 630', 'GT 710', 'GT 720', 'GT 730']):
        recommended_version = "11.3"  # Kepler generation - avoid driver conflicts
        print(f"💡 Recommending CUDA {recommended_version} for Kepler GPU: {gpu_model}")
        print(f"⚠️ Note: Your {gpu_model} may have driver conflicts with CUDA 11.8+")
    else:
        recommended_version = "12.1"
        print(f"🚀 Recommending CUDA {recommended_version} for modern GPU: {gpu_model}")
    
    # Use recommended version if no specific target provided
    if not target_version:
        target_version = recommended_version
    
    # Try winget first (faster and native)
    if managers['winget']:
        print("📦 Trying winget (Windows Package Manager)...")
        
        # Get available versions
        available_versions = get_available_cuda_versions('winget')
        if available_versions:
            print(f"✅ Found CUDA versions in winget: {', '.join(available_versions[:3])}...")
            
            # Find best matching version
            best_match = None
            for version in available_versions:
                if version.startswith(target_version):
                    best_match = version
                    break
            
            if best_match:
                cmd = f"winget install NVIDIA.CUDA --version {best_match}"
                if dry_run:
                    print(f"💡 Would run: {cmd}")
                    return True, f"Would install CUDA {best_match} via winget"
                else:
                    print(f"🔧 Installing CUDA {best_match} via winget...")
                    result = run(cmd)
                    if result:
                        return True, f"Successfully installed CUDA {best_match}"
                    else:
                        print("⚠️ winget installation failed, trying chocolatey...")
    
    # Try chocolatey as fallback
    if managers['choco']:
        print("🍫 Trying Chocolatey...")
        
        # Get available versions
        available_versions = get_available_cuda_versions('choco')
        if available_versions:
            print(f"✅ Found CUDA versions in chocolatey: {', '.join(available_versions[:3])}...")
            
            # Find best matching version
            best_match = None
            for version in available_versions:
                if version.startswith(target_version):
                    best_match = version
                    break
            
            if best_match:
                cmd = f"choco install cuda --version={best_match} -y"
                if dry_run:
                    print(f"💡 Would run: {cmd}")
                    return True, f"Would install CUDA {best_match} via chocolatey"
                else:
                    print(f"🔧 Installing CUDA {best_match} via chocolatey...")
                    result = run(cmd)
                    if result:
                        return True, f"Successfully installed CUDA {best_match}"
    
    # No package managers available
    if not managers['winget'] and not managers['choco']:
        return False, "No package managers available. Install winget or chocolatey first."
    
    return False, f"CUDA {target_version} not found in available package managers"


def show_installed_versions():
    """Show detailed information about installed PyTorch ecosystem"""
    try:
        import torch
        print(f"\n📊 Installed PyTorch Ecosystem:")
        print(f"   🔥 PyTorch: {torch.__version__}")
        
        try:
            import torchvision
            print(f"   👁️ TorchVision: {torchvision.__version__}")
        except ImportError:
            print(f"   👁️ TorchVision: Not installed")
        
        try:
            import torchaudio
            print(f"   🔊 TorchAudio: {torchaudio.__version__}")
        except ImportError:
            print(f"   🔊 TorchAudio: Not installed")
        
        # Show backend support
        print(f"   🎯 CUDA Support: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"   🚀 CUDA Version: {torch.version.cuda}")
            print(f"   🎮 GPU Count: {torch.cuda.device_count()}")
            # Show actual GPU names
            for i in range(torch.cuda.device_count()):
                print(f"   🎮 GPU {i}: {torch.cuda.get_device_name(i)}")
        
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print(f"   🍎 MPS Support: Available")
        
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    return True


def setup_logging(enable_logging):
    """Setup logging to file if requested"""
    if enable_logging:
        logfile = f"torch_install_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        print(f"💾 Logging install to {logfile}")
        
        # Create a custom stdout that writes to both console and file
        class TeeOutput:

            def __init__(self, file):
                self.terminal = sys.stdout
                self.log = file
            
            def write(self, message):
                self.terminal.write(message)
                self.log.write(message)
                self.log.flush()
            
            def flush(self):
                self.terminal.flush()
                self.log.flush()
        
        log_file = open(logfile, 'w', encoding='utf-8')
        sys.stdout = TeeOutput(log_file)
        return log_file
    return None


def main():
    parser = argparse.ArgumentParser(description="🚀 PyTorch Installation Assistant")
    parser.add_argument("--force-cuda", metavar="VERSION",
                       help="Force install specific CUDA version (e.g., cu121, cu118)")
    parser.add_argument("--list-cuda", action="store_true",
                       help="List supported CUDA versions and exit")
    parser.add_argument("--cpu-only", action="store_true",
                       help="Force CPU-only installation")
    parser.add_argument("--dry-run", action="store_true",
                       help="Only show install commands, don't run them")
    parser.add_argument("--log", action="store_true",
                       help="Log all output to a timestamped file")
    parser.add_argument("--show-matching", action="store_true",
                       help="Show CUDA version matching logic and exit")
    parser.add_argument("--force-reinstall", action="store_true",
                       help="Force reinstall even if PyTorch is already present")
    parser.add_argument("--gpu-info", action="store_true",
                       help="Show GPU and CUDA compatibility information")
    parser.add_argument("--auto-install-cuda", action="store_true",
                       help="Automatically install CUDA using package managers (Windows only)")
    parser.add_argument("--cuda-version", metavar="VERSION",
                       help="Specify CUDA version to install (e.g., 11.8, 12.1)")
    parser.add_argument("--show-versions", action="store_true",
                       help="Show currently installed PyTorch ecosystem versions")
    
    args = parser.parse_args()
    
    # Setup logging if requested
    log_file = setup_logging(args.log)
    
    print("🚀 PyTorch Installation Assistant")
    print("=" * 40)
    
    if args.dry_run:
        print("💡 DRY RUN MODE - No actual installation will occur")
        print("=" * 40)
    
    # Handle list CUDA versions
    if args.list_cuda:
        print("📋 Supported CUDA versions:")
        versions = get_supported_cuda_versions()
        for version in versions:
            version_display = f"{version[:2]}.{version[2:]}" if len(version) == 3 else version
            print(f"  • cu{version} (CUDA {version_display})")
        return
    
    # Handle show matching logic
    if args.show_matching:
        print("🧠 CUDA Version Matching Logic Demo")
        print("=" * 40)
        system_info = get_system_info()
        detected = detect_cuda_version(system_info)
        if detected and detected != "mps":
            supported = get_supported_cuda_versions()
            print(f"\n🔍 Detected CUDA: {detected}")
            print(f"📋 Supported versions: {supported}")
            match = find_best_cuda_match(detected, supported)
            if match:
                print(f"✅ Would install: cu{match}")
            else:
                torch_ver, vision_ver, audio_ver = find_best_pytorch_version(detected)
                if torch_ver:
                    print(f"✅ Would install: PyTorch {torch_ver} with CUDA {detected}")
                    print(f"   📦 Full package set: torch={torch_ver}, torchvision={vision_ver}, torchaudio={audio_ver}")
                else:
                    print("❌ No compatible version found - would install CPU-only")
        else:
            print(f"ℹ️ No CUDA detected (found: {detected})")
        return
    
    # Handle GPU info
    if args.gpu_info:
        print("🎮 GPU and CUDA Compatibility Information")
        print("=" * 50)
        system_info = get_system_info()
        gpu_info = detect_gpu_info()
        detected = detect_cuda_version(system_info)
        
        # Show GPU information
        if gpu_info['model']:
            print(f"🎮 Detected GPU: {gpu_info['model']}")
            if gpu_info['memory']:
                print(f"💾 GPU Memory: {gpu_info['memory']}")
        else:
            print("❓ No NVIDIA GPU detected or nvidia-smi not available")
        
        if detected and detected != "mps":
            detected_readable = f"{detected[:2]}.{detected[2:]}" if len(detected) == 3 else detected
            print(f"🔍 Detected CUDA: {detected_readable}")
            
            # Show current PyTorch compatibility
            supported = get_supported_cuda_versions()
            match = find_best_cuda_match(detected, supported)
            
            if match:
                print(f"✅ Latest PyTorch supports your CUDA via cu{match}")
            else:
                print("⚠️ Latest PyTorch doesn't support your CUDA version")
                torch_ver, vision_ver, audio_ver = find_best_pytorch_version(detected)
                if torch_ver:
                    print(f"💡 Recommended: PyTorch {torch_ver} with native CUDA {detected_readable} support")
                    print(f"   📦 Full package set: torch={torch_ver}, torchvision={vision_ver}, torchaudio={audio_ver}")
                else:
                    print("❌ No compatible PyTorch version found")
                    # Show GPU-specific upgrade guidance with auto-install option
                    guidance = get_gpu_upgrade_guidance(gpu_info, detected, auto_install=True)
                    for line in guidance:
                        print(line)
            
            print(f"\n📋 All supported CUDA versions in latest PyTorch:")
            for version in supported:
                version_display = f"{version[:2]}.{version[2:]}" if len(version) == 3 else version
                print(f"  • CUDA {version_display} (cu{version})")
        else:
            print(f"ℹ️ No CUDA detected (found: {detected})")
        return
    
    # Handle show versions
    if args.show_versions:
        print("📊 Currently Installed PyTorch Ecosystem")
        print("=" * 45)
        show_installed_versions()
        return
    
    # Handle auto-install CUDA
    if args.auto_install_cuda:
        print("🤖 CUDA Auto-Installation Mode")
        print("=" * 35)
        
        if platform.system() != "Windows":
            print("❌ CUDA auto-install is only supported on Windows")
            print("💡 For other platforms, install CUDA manually from NVIDIA")
            return
        
        system_info = get_system_info()
        gpu_info = detect_gpu_info()
        
        if not gpu_info['model']:
            print("❌ No NVIDIA GPU detected")
            print("💡 Ensure you have an NVIDIA GPU and drivers installed")
            return
        
        print(f"🎮 Detected GPU: {gpu_info['model']}")
        
        # Check current CUDA
        current_cuda = detect_cuda_version(system_info)
        if current_cuda and current_cuda != "mps":
            current_readable = f"{current_cuda[:2]}.{current_cuda[2:]}" if len(current_cuda) == 3 else current_cuda
            print(f"📋 Current CUDA: {current_readable}")
        
        # Install CUDA
        target_version = args.cuda_version
        success, message = install_cuda_windows(target_version, gpu_info, dry_run=args.dry_run)
        
        if success:
            print(f"✅ {message}")
            if not args.dry_run:
                print("🔄 Please restart your command prompt/terminal and run the installer again")
                print("   This ensures the new CUDA installation is properly detected")
        else:
            print(f"❌ {message}")
            print("💡 You can install CUDA manually from:")
            print("   https://developer.nvidia.com/cuda-downloads")
        
        return
    
    # Get system information using platform module
    system_info = get_system_info()
    print()
    
    torch_status = is_torch_installed()
    
    if not torch_status or args.force_reinstall or (torch_status == "cpu-only" and not args.cpu_only):
        if torch_status == "cpu-only":
            print("🔄 CPU-only PyTorch detected. Installing CUDA version...")
        elif args.force_reinstall:
            print("🔄 Force reinstall requested. Reinstalling PyTorch...")
        else:
            print("📦 PyTorch not found. Starting installation...")
        
        if args.cpu_only:
            print("🔧 CPU-only installation requested")
            cuda_ver = None
        elif args.force_cuda:
            # Clean up the force_cuda argument (remove 'cu' prefix if present)
            force_cuda = args.force_cuda.replace('cu', '') if args.force_cuda.startswith('cu') else args.force_cuda
            cuda_ver = detect_cuda_version(system_info)  # Still detect for info
            install_torch(cuda_ver, system_info, force_cuda=force_cuda, dry_run=args.dry_run, force_reinstall=args.force_reinstall)
            if not args.dry_run:
                # Verify installation and run tests
                print("\n🔍 Verifying installation...")
                if is_torch_installed():
                    print("✅ PyTorch installation completed successfully!")
                    verify_cuda_tensor()
                else:
                    print("❌ PyTorch installation may have failed. Please check the output above.")
            if log_file:
                log_file.close()
            return
        else:
            cuda_ver = detect_cuda_version(system_info)
        
        install_torch(cuda_ver, system_info, dry_run=args.dry_run, force_reinstall=(torch_status == "cpu-only" or args.force_reinstall))
        
        if not args.dry_run:
            # Verify installation
            print("\n🔍 Verifying installation...")
            if is_torch_installed():
                print("✅ PyTorch installation completed successfully!")
                show_installed_versions()
                
                # Run hardware-specific tests
                if cuda_ver == "mps":
                    verify_mps_tensor()
                elif cuda_ver:
                    verify_cuda_tensor()
                else:
                    print("🧪 CPU-only installation - no GPU tests needed")
            else:
                print("❌ PyTorch installation may have failed. Please check the output above.")
    else:
        print("🔥 Torch is already ready to blaze!")
        
        # Show additional system compatibility info and run tests
        try:
            import torch  # noqa: F401 - Import needed for runtime check
            print(f"🎯 CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                print(f"🔥 CUDA device count: {torch.cuda.device_count()}")
                print(f"🎮 Current CUDA device: {torch.cuda.get_device_name(0)}")
                if not args.dry_run:
                    verify_cuda_tensor()
            elif "+cpu" in torch.__version__:
                # Show GPU-specific upgrade guidance with auto-install option
                gpu_info = detect_gpu_info()
                detected_cuda = detect_cuda_version(system_info)
                guidance = get_gpu_upgrade_guidance(gpu_info, detected_cuda, auto_install=True)
                print()
                for line in guidance:
                    print(line)
            if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                print("🍎 MPS (Metal) available: True")
                if not args.dry_run:
                    verify_mps_tensor()
        except ImportError:
            print("⚠️ PyTorch not available for compatibility check")
            pass
    
    # Clean up logging
    if log_file:
        log_file.close()


if __name__ == "__main__":
    main()
