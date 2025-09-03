#!/usr/bin/env python3
"""
TradePulse Demo Panel UI Launcher - REFACTORED VERSION
Launches the refactored demo Panel UI using the new modular architecture
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
        'demo_panels.demo_panel_ui',
        'demo_panels.demo_data_generator',
        'demo_panels.demo_ui_components',
        'demo_panels.demo_chart_manager',
        'demo_panels.demo_controller',
        'ui_components.data_manager',
        'ui_components.chart_component'
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

def launch_demo_ui():
    """Launch the refactored demo Panel UI"""
    try:
        from demo_panels.demo_panel_ui import TradePulseDemo
        
        print("🚀 Launching TradePulse REFACTORED Demo Panel UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        demo = TradePulseDemo()
        app = demo.get_app()
        app.show()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 The refactored demo_panels components should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False

def main():
    """Main function"""
    print("🎯 TradePulse REFACTORED Demo Panel UI Launcher")
    print("=" * 55)
    
    # Check if we're in the right directory
    if not Path("demo_panels").exists():
        print("❌ demo_panels directory not found in current directory")
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
    if not launch_demo_ui():
        print("❌ Failed to launch REFACTORED Demo Panel UI")
        return
    
    print("✅ REFACTORED Demo Panel UI launched successfully!")

if __name__ == "__main__":
    main()
