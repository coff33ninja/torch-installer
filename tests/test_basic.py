"""Basic tests for torch-installer package."""

import pytest
import platform
from unittest.mock import patch

# Import the functions we want to test
from torch_installer.installer import (
    get_system_info,
    detect_gpu_info,
    detect_cuda_version,
    is_torch_installed,
)
from torch_installer import __version__


def test_version():
    """Test that version is defined."""
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_get_system_info():
    """Test system information detection."""
    info = get_system_info()
    
    assert isinstance(info, dict)
    assert 'system' in info
    assert 'machine' in info
    assert 'architecture' in info
    assert 'python_version' in info
    
    # Check that values are reasonable
    assert info['system'] in ['Windows', 'Linux', 'Darwin']
    assert info['python_version'] == platform.python_version()


def test_detect_gpu_info():
    """Test GPU information detection."""
    gpu_info = detect_gpu_info()
    
    assert isinstance(gpu_info, dict)
    assert 'model' in gpu_info
    assert 'cuda_version' in gpu_info
    assert 'compute_capability' in gpu_info
    assert 'memory' in gpu_info


def test_detect_cuda_version():
    """Test CUDA version detection."""
    system_info = get_system_info()
    cuda_version = detect_cuda_version(system_info)
    
    # CUDA version should be None, a string, or "mps" for macOS
    assert cuda_version is None or isinstance(cuda_version, str)
    
    if cuda_version == "mps":
        assert system_info['system'] == 'Darwin'


def test_is_torch_installed():
    """Test PyTorch installation detection."""
    result = is_torch_installed()
    
    # Should return False (not installed) or a string describing the installation
    assert result is False or isinstance(result, str)
    
    if isinstance(result, str):
        assert result in ['cpu-only', 'cuda-enabled', 'cuda-broken']


@patch('subprocess.check_output')
def test_detect_gpu_info_with_nvidia_smi(mock_subprocess):
    """Test GPU detection with mocked nvidia-smi output."""
    # Mock nvidia-smi output
    mock_output = """
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 525.60.11    Driver Version: 525.60.11    CUDA Version: 12.1   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  GeForce RTX 3080    Off  | 00000000:01:00.0  On |                  N/A |
| 30%   45C    P8    25W / 320W |   1024MiB / 10240MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
"""
    
    mock_subprocess.return_value = mock_output.encode()
    
    with patch('shutil.which', return_value='/usr/bin/nvidia-smi'):
        gpu_info = detect_gpu_info()
        
        assert 'RTX' in gpu_info['model']
        assert gpu_info['cuda_version'] == '12.1'
        assert gpu_info['memory'] == '10240MB'


def test_cli_import():
    """Test that CLI module can be imported."""
    try:
        from torch_installer.cli import main
        assert callable(main)
    except ImportError:
        pytest.fail("Could not import CLI module")


if __name__ == "__main__":
    pytest.main([__file__])
