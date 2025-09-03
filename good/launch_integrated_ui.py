#!/usr/bin/env python3
"""
TradePulse Integrated Panel UI Launcher - REFACTORED VERSION
Launches the refactored integrated Panel UI using the new modular architecture
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['panel', 'pandas', 'numpy', 'plotly', 'tabulator']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Installed {package}")
            except ImportError:
                print(f"❌ Failed to install {package}")
                return False
    
    return True

def check_tradepulse_modules():
    """Check if TradePulse modules are available"""
    print("🔍 Checking TradePulse module availability...")
    
    modules_to_check = [
        'integrated_panels.tradepulse_integration',
        'integrated_panels.ui_orchestrator',
        'integrated_panels.system_monitor',
        'integrated_panels.performance_tracker',
        'ui_components.data_manager',
        'ui_components.chart_component',
        'ui_components.portfolio_component'
    ]
    
    available_modules = []
    missing_modules = []
    
    for module in modules_to_check:
        try:
            __import__(module)
            available_modules.append(module)
            print(f"✅ {module}")
        except ImportError:
            missing_modules.append(module)
            print(f"⚠️ {module} (will use mock)")
    
    print(f"\n📊 Module Status:")
    print(f"✅ Available: {len(available_modules)}")
    print(f"⚠️ Missing: {len(missing_modules)}")
    
    if len(available_modules) > 0:
        print("🎉 Core TradePulse modules available - full integration enabled!")
    else:
        print("⚠️ Using mock modules - limited functionality")
    
    return len(available_modules) > 0

def launch_integrated_ui():
    """Launch the refactored integrated Panel UI"""
    try:
        # Import and run the REFACTORED integrated UI
        from integrated_panels.integrated_panel_ui import main
        
        print("🚀 Launching TradePulse REFACTORED Integrated Panel UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app = main()
        app.show()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and dependencies are installed")
        print("💡 The refactored integrated_panels components should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎯 TradePulse REFACTORED Integrated Panel UI Launcher")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("integrated_panels").exists():
        print("❌ integrated_panels directory not found in current directory")
        print("💡 Please run this script from the TradePulse root directory")
        print("💡 Make sure the refactoring has been completed")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install required dependencies")
        return
    
    # Check TradePulse modules
    has_tradepulse_modules = check_tradepulse_modules()
    
    # Launch UI
    if not launch_integrated_ui():
        print("❌ Failed to launch REFACTORED Integrated Panel UI")
        return
    
    print("✅ REFACTORED Integrated Panel UI launched successfully!")

if __name__ == "__main__":
    main()
