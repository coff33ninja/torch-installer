# 📦 Packaging and Distribution Guide

This guide will help you package your torch-installer project and upload it to PyPI and GitHub.

## 🚀 Quick Start

### 1. Build the Package
```bash
python build_package.py
```

### 2. Test Locally
```bash
pip install dist/torch_installer-*.whl
torch-installer --help
```

### 3. Upload to PyPI
```bash
# Test on TestPyPI first
python upload_package.py --test

# Then upload to real PyPI
python upload_package.py
```

## 📋 Prerequisites

### Python Environment
- Python 3.7 or higher
- pip and setuptools installed

### PyPI Accounts
1. **TestPyPI Account** (for testing): https://test.pypi.org/account/register/
2. **PyPI Account** (for production): https://pypi.org/account/register/

### API Tokens
Generate API tokens for secure uploads:
- **TestPyPI**: https://test.pypi.org/manage/account/token/
- **PyPI**: https://pypi.org/manage/account/token/

## 🔧 Manual Build Process

### 1. Install Build Dependencies
```bash
pip install --upgrade build twine
```

### 2. Clean Previous Builds
```bash
# Remove old build artifacts
rm -rf build/ dist/ *.egg-info/
```

### 3. Build the Package
```bash
python -m build
```

This creates:
- `dist/torch_installer-1.0.0.tar.gz` (source distribution)
- `dist/torch_installer-1.0.0-py3-none-any.whl` (wheel distribution)

### 4. Check the Package
```bash
python -m twine check dist/*
```

## 📤 Manual Upload Process

### Upload to TestPyPI (Recommended First)
```bash
python -m twine upload --repository testpypi dist/*
```

### Test Installation from TestPyPI
```bash
pip install --index-url https://test.pypi.org/simple/ torch-installer
```

### Upload to PyPI (Production)
```bash
python -m twine upload dist/*
```

## 🐙 GitHub Setup

### 1. Create Repository
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/coff33ninja/torch-installer.git
git push -u origin main
```

### 2. Set Up GitHub Secrets
Go to your repository settings → Secrets and variables → Actions

Add these secrets:
- `PYPI_API_TOKEN`: Your PyPI API token
- `TEST_PYPI_API_TOKEN`: Your TestPyPI API token

### 3. GitHub Actions Workflow
The included `.github/workflows/test-and-publish.yml` will:
- Run tests on multiple Python versions and OS
- Auto-publish to TestPyPI on `develop` branch pushes
- Auto-publish to PyPI on GitHub releases

## 🏷️ Version Management

### Update Version
Edit `torch_installer/__init__.py`:
```python
__version__ = "1.0.1"  # Increment version
```

### Create GitHub Release
1. Go to your repository → Releases
2. Click "Create a new release"
3. Tag version: `v1.0.1`
4. Release title: `v1.0.1`
5. Describe changes
6. Click "Publish release"

This will automatically trigger PyPI upload via GitHub Actions.

## 🧪 Testing

### Run Tests Locally
```bash
pip install pytest
pytest tests/
```

### Test Package Installation
```bash
# Build and install locally
python -m build
pip install dist/*.whl

# Test CLI commands
torch-installer --help
pytorch-installer --help

# Test Python import
python -c "import torch_installer; print(torch_installer.__version__)"
```

## 📊 Package Structure

```
torch-installer/
├── torch_installer/           # Main package
│   ├── __init__.py           # Package initialization
│   ├── installer.py          # Core functionality
│   └── cli.py               # Command-line interface
├── tests/                   # Test suite
│   ├── __init__.py
│   └── test_basic.py
├── .github/workflows/       # GitHub Actions
│   └── test-and-publish.yml
├── build_package.py         # Build script
├── upload_package.py        # Upload script
├── setup.py                 # Setup configuration
├── pyproject.toml          # Modern Python packaging
├── MANIFEST.in             # Include additional files
├── LICENSE                 # MIT License
├── README.md              # Documentation
└── .gitignore            # Git ignore rules
```

## 🔍 Troubleshooting

### Common Build Issues

**"No module named 'build'"**
```bash
pip install --upgrade build
```

**"Version already exists"**
- Increment version in `torch_installer/__init__.py`
- Rebuild and upload

**"Invalid credentials"**
- Check your API token
- Ensure token has correct permissions

### Common Upload Issues

**"403 Forbidden"**
- Check API token permissions
- Verify package name isn't taken

**"400 Bad Request"**
- Run `twine check dist/*` to validate package
- Check metadata in `setup.py`

## 🎯 Best Practices

### Version Numbering
Use semantic versioning (SemVer):
- `1.0.0` - Major release
- `1.0.1` - Bug fixes
- `1.1.0` - New features
- `2.0.0` - Breaking changes

### Release Process
1. Update version number
2. Update CHANGELOG.md
3. Test locally
4. Upload to TestPyPI
5. Test from TestPyPI
6. Create GitHub release
7. Auto-upload to PyPI via GitHub Actions

### Security
- Never commit API tokens to git
- Use GitHub Secrets for CI/CD
- Regularly rotate API tokens

## 📚 Additional Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Help](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🎉 Success!

Once uploaded, users can install your package with:
```bash
pip install torch-installer
```

And use it with:
```bash
torch-installer
# or
pytorch-installer
```