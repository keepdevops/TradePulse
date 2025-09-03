#!/bin/bash

# TradePulse Environment Setup Script v10.7
# Optimized for Apple Silicon M3 with conda-forge

set -e

echo "🚀 Setting up TradePulse conda environment v10.7..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo -e "${RED}❌ Conda is not installed or not in PATH${NC}"
    echo "Please install Miniconda or Anaconda first:"
    echo "https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Check if we're on Apple Silicon
if [[ $(uname -m) == "arm64" ]]; then
    echo -e "${BLUE}🍎 Detected Apple Silicon (ARM64) architecture${NC}"
    ARCH="apple_silicon"
else
    echo -e "${YELLOW}⚠️  Detected x86_64 architecture${NC}"
    ARCH="x86_64"
fi

# Remove existing environment if it exists
if conda env list | grep -q "tradepulse"; then
    echo -e "${YELLOW}⚠️  Removing existing tradepulse environment...${NC}"
    conda env remove -n tradepulse -y
fi

# Create new environment from environment.yml
echo -e "${BLUE}📦 Creating new tradepulse environment...${NC}"
conda env create -f environment.yml

# Activate the environment
echo -e "${BLUE}🔧 Activating tradepulse environment...${NC}"
source $(conda info --base)/etc/profile.d/conda.sh
conda activate tradepulse

# Verify Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python version: $PYTHON_VERSION${NC}"

# Install additional packages that might be needed
echo -e "${BLUE}📚 Installing additional packages...${NC}"
pip install --upgrade pip

# Install packages that might have compatibility issues with conda
echo -e "${BLUE}🔧 Installing pip-specific packages...${NC}"

# Core dependencies
pip install "mplfinance>=0.12.0a0"
pip install "seaborn>=0.12.0"

# ML and Data Science
pip install "catboost>=1.2.0"
pip install "optuna>=3.2.0"
pip install "polars>=0.19.0"
pip install "vaex>=4.15.0"

# Monitoring and Development
pip install "structlog>=23.1.0"
pip install "rich>=13.4.0"
pip install "pydantic>=2.0.0"
pip install "hydra-core>=1.3.0"

# Async and Performance
pip install "asyncio-mqtt>=0.13.0"
pip install "aiohttp>=3.8.0"
pip install "memory-profiler>=0.61.0"
pip install "line-profiler>=4.1.0"

# Verify key packages
echo -e "${BLUE}🔍 Verifying key packages...${NC}"
python -c "import pandas, numpy, scipy, matplotlib, seaborn, plotly, sklearn, pyzmq; print('✅ Core packages imported successfully')"
python -c "import mplfinance, duckdb, sqlalchemy; print('✅ Specialized packages imported successfully')"

# Create a simple test script
echo -e "${BLUE}🧪 Creating test script...${NC}"
cat > test_environment.py << 'EOF'
#!/usr/bin/env python3
"""
TradePulse Environment Test Script
Tests that all key packages are working correctly
"""

def test_imports():
    """Test that all key packages can be imported."""
    try:
        # Core scientific computing
        import pandas as pd
        import numpy as np
        import scipy
        print("✅ Core scientific computing packages imported")
        
        # Data visualization
        import matplotlib.pyplot as plt
        import seaborn as sns
        import plotly.express as px
        print("✅ Data visualization packages imported")
        
        # Machine learning
        import sklearn
        import xgboost as xgb
        print("✅ Machine learning packages imported")
        
        # Message bus
        import zmq
        print("✅ Message bus (ZMQ) imported")
        
        # Financial charting
        import mplfinance as mpf
        print("✅ Financial charting imported")
        
        # Database
        import duckdb
        import sqlalchemy
        print("✅ Database packages imported")
        
        # Testing
        import pytest
        print("✅ Testing framework imported")
        
        print("\n🎉 All packages imported successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key packages."""
    try:
        # Test pandas
        import pandas as pd
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        assert len(df) == 3
        print("✅ Pandas basic functionality working")
        
        # Test numpy
        import numpy as np
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.mean() == 3.0
        print("✅ Numpy basic functionality working")
        
        # Test matplotlib
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [1, 4, 2])
        plt.close(fig)
        print("✅ Matplotlib basic functionality working")
        
        print("\n🎉 Basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Functionality test error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing TradePulse Environment...")
    print("=" * 50)
    
    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()
    
    if imports_ok and functionality_ok:
        print("\n🎉 Environment setup complete and verified!")
        print("You can now activate the environment with: conda activate tradepulse")
    else:
        print("\n❌ Environment setup has issues. Please check the errors above.")
EOF

# Make test script executable
chmod +x test_environment.py

# Run the test
echo -e "${BLUE}🧪 Running environment test...${NC}"
python test_environment.py

# Create activation reminder
echo -e "${GREEN}🎉 Environment setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 To activate the environment:${NC}"
echo "conda activate tradepulse"
echo ""
echo -e "${BLUE}📋 To deactivate:${NC}"
echo "conda deactivate"
echo ""
echo -e "${BLUE}📋 To remove the environment:${NC}"
echo "conda env remove -n tradepulse"
echo ""
echo -e "${BLUE}📋 To update packages:${NC}"
echo "conda env update -f environment.yml"
echo ""
echo -e "${BLUE}📋 To install additional packages:${NC}"
echo "conda activate tradepulse"
echo "pip install package_name"
echo ""
echo -e "${GREEN}🚀 Happy trading with TradePulse v10.7!${NC}"
