@echo off
REM TradePulse FastAPI Conda Installation Script (Windows)
REM Install FastAPI dependencies using conda and conda-forge

echo 🚀 TradePulse FastAPI Conda Installation
echo ========================================

REM Check if conda is installed
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Conda is not installed. Please install Anaconda or Miniconda first.
    echo    Download from: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

echo ✅ Conda found: 
conda --version

REM Check if environment already exists
conda env list | findstr "tradepulse-fastapi" >nul
if %errorlevel% equ 0 (
    echo ⚠️  Environment 'tradepulse-fastapi' already exists.
    set /p choice="Do you want to remove it and recreate? (y/N): "
    if /i "%choice%"=="y" (
        echo 🗑️  Removing existing environment...
        conda env remove -n tradepulse-fastapi
    ) else (
        echo 📝 Updating existing environment...
        conda env update -f environment_fastapi.yml
        echo ✅ Environment updated successfully!
        echo.
        echo 🎯 To activate the environment:
        echo    conda activate tradepulse-fastapi
        echo.
        echo 🚀 To start the FastAPI server:
        echo    conda activate tradepulse-fastapi
        echo    python launch_fastapi_server.py
        pause
        exit /b 0
    )
)

REM Create new environment
echo 🔧 Creating conda environment 'tradepulse-fastapi'...
conda env create -f environment_fastapi.yml

if %errorlevel% equ 0 (
    echo ✅ Environment created successfully!
    echo.
    echo 🎯 Next steps:
    echo 1. Activate the environment:
    echo    conda activate tradepulse-fastapi
    echo.
    echo 2. Start the FastAPI server:
    echo    python launch_fastapi_server.py
    echo.
    echo 3. Use the redline data upload utility:
    echo    python upload_redline_data.py
    echo.
    echo 📚 API documentation will be available at:
    echo    http://localhost:8000/docs
    echo.
    echo 🎉 Installation complete!
) else (
    echo ❌ Failed to create environment. Please check the error messages above.
)

pause
