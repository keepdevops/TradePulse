#!/bin/bash
# TradePulse FastAPI Conda Installation Script
# Install FastAPI dependencies using conda and conda-forge

set -e  # Exit on any error

echo "🚀 TradePulse FastAPI Conda Installation"
echo "========================================"

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is not installed. Please install Anaconda or Miniconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

echo "✅ Conda found: $(conda --version)"

# Check if environment already exists
if conda env list | grep -q "tradepulse-fastapi"; then
    echo "⚠️  Environment 'tradepulse-fastapi' already exists."
    read -p "Do you want to remove it and recreate? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing existing environment..."
        conda env remove -n tradepulse-fastapi
    else
        echo "📝 Updating existing environment..."
        conda env update -f environment_fastapi.yml
        echo "✅ Environment updated successfully!"
        echo ""
        echo "🎯 To activate the environment:"
        echo "   conda activate tradepulse-fastapi"
        echo ""
        echo "🚀 To start the FastAPI server:"
        echo "   conda activate tradepulse-fastapi"
        echo "   python launch_fastapi_server.py"
        exit 0
    fi
fi

# Create new environment
echo "🔧 Creating conda environment 'tradepulse-fastapi'..."
conda env create -f environment_fastapi.yml

if [ $? -eq 0 ]; then
    echo "✅ Environment created successfully!"
    echo ""
    echo "🎯 Next steps:"
    echo "1. Activate the environment:"
    echo "   conda activate tradepulse-fastapi"
    echo ""
    echo "2. Start the FastAPI server:"
    echo "   python launch_fastapi_server.py"
    echo ""
    echo "3. Use the redline data upload utility:"
    echo "   python upload_redline_data.py"
    echo ""
    echo "📚 API documentation will be available at:"
    echo "   http://localhost:8000/docs"
    echo ""
    echo "🎉 Installation complete!"
else
    echo "❌ Failed to create environment. Please check the error messages above."
    exit 1
fi
