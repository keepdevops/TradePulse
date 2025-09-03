# TradePulse FastAPI Conda Installation Guide

This guide explains how to install FastAPI dependencies using conda and conda-forge.

## Prerequisites

1. **Install Anaconda or Miniconda**
   - Download from: https://docs.conda.io/en/latest/miniconda.html
   - Choose the appropriate version for your OS (Windows, macOS, Linux)

2. **Verify conda installation**
   ```bash
   conda --version
   ```

## Installation Methods

### Method 1: Automated Scripts (Recommended)

#### macOS/Linux
```bash
# Make script executable (if needed)
chmod +x install_fastapi_conda.sh

# Run installation script
./install_fastapi_conda.sh
```

#### Windows
```cmd
# Run installation script
install_fastapi_conda.bat
```

### Method 2: Manual Installation

```bash
# Create environment from YAML file
conda env create -f environment_fastapi.yml

# Activate the environment
conda activate tradepulse-fastapi
```

### Method 3: Step-by-step Installation

```bash
# Create base environment
conda create -n tradepulse-fastapi python=3.10

# Activate environment
conda activate tradepulse-fastapi

# Install core FastAPI packages
conda install -c conda-forge fastapi=0.104.1 uvicorn=0.24.0

# Install data processing packages
conda install -c conda-forge pandas=2.1.4 numpy=1.25.2 scikit-learn=1.3.2

# Install additional dependencies
conda install -c conda-forge matplotlib=3.8.2 plotly=5.17.0

# Install financial data packages
conda install -c conda-forge yfinance=0.2.28

# Install development tools
conda install -c conda-forge pytest=7.4.3 black=23.11.0 flake8=6.1.0
```

## Environment Management

### List Environments
```bash
conda env list
```

### Activate Environment
```bash
conda activate tradepulse-fastapi
```

### Deactivate Environment
```bash
conda deactivate
```

### Update Environment
```bash
conda env update -f environment_fastapi.yml
```

### Remove Environment
```bash
conda env remove -n tradepulse-fastapi
```

## Package Management

### Install Additional Packages
```bash
conda activate tradepulse-fastapi
conda install -c conda-forge package_name
```

### Install from pip (if not available in conda)
```bash
conda activate tradepulse-fastapi
pip install package_name
```

### Export Environment
```bash
conda env export > environment_export.yml
```

## Troubleshooting

### Common Issues

1. **Conda not found**
   - Ensure Anaconda/Miniconda is properly installed
   - Add conda to your PATH environment variable
   - Restart your terminal/command prompt

2. **Package conflicts**
   - Try installing packages one by one
   - Use `conda install -c conda-forge` for better package availability
   - Check package compatibility

3. **Environment creation fails**
   - Check available disk space
   - Ensure you have write permissions
   - Try updating conda: `conda update conda`

4. **Package not found in conda**
   - Use conda-forge channel: `conda install -c conda-forge package_name`
   - Install via pip: `pip install package_name`
   - Check alternative package names

### Performance Tips

1. **Use conda-forge channel**
   - Generally faster and more up-to-date packages
   - Better community support

2. **Install packages in batches**
   - Reduces dependency resolution time
   - Better error handling

3. **Use mamba (faster alternative to conda)**
   ```bash
   # Install mamba
   conda install -c conda-forge mamba
   
   # Use mamba instead of conda
   mamba env create -f environment_fastapi.yml
   ```

## Verification

After installation, verify everything works:

```bash
# Activate environment
conda activate tradepulse-fastapi

# Check Python version
python --version

# Check installed packages
conda list

# Test FastAPI import
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"

# Test uvicorn
python -c "import uvicorn; print('Uvicorn version:', uvicorn.__version__)"

# Start the server
python launch_fastapi_server.py
```

## Next Steps

After successful installation:

1. **Start the FastAPI server:**
   ```bash
   conda activate tradepulse-fastapi
   python launch_fastapi_server.py
   ```

2. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs

3. **Upload redline data:**
   ```bash
   conda activate tradepulse-fastapi
   python upload_redline_data.py
   ```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify conda installation: `conda --version`
3. Check environment status: `conda env list`
4. Review error messages carefully
5. Try the manual installation method
