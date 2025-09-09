#!/usr/bin/env python3
"""
TradePulse Modular Panel UI Launcher - REFACTORED VERSION
Launches the modular panel UI where each TradePulse module has its own dedicated panel
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
        'ui_components.data_manager',
        'modular_panels.data_panel',
        'modular_panels.models_panel',
        'modular_panels.portfolio_panel',
        'modular_panels.ai_panel',
        'modular_panels.charts_panel',
        'modular_panels.alerts_panel',
        'modular_panels.system_panel'
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
    
    if len(available_modules) >= 5:
        print("🎉 Core TradePulse modules available - full integration enabled!")
    else:
        print("⚠️ Some modules missing - will use mock implementations")
    
    return len(available_modules) >= 5

def launch_modular_ui():
    """Launch the refactored modular panel UI with tabbed modules"""
    try:
        # Import and run the REFACTORED MODULAR PANEL UI
        from modular_panel_ui_main_refactored import create_refactored_modular_ui
        
        print("🚀 Launching TradePulse REFACTORED MODULAR PANEL UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("🧩 Each module has its own dedicated panel with focused components:")
        print("   📊 Data Panel - Data management and uploads")
        print("   🤖 Models Panel - AI/ML model management")
        print("   💼 Portfolio Panel - Portfolio optimization")
        print("   🧠 AI Panel - AI-powered trading strategies")
        print("   📈 Charts Panel - Advanced charting and analysis")
        print("   🚨 Alerts Panel - Trading alerts and notifications")
        print("   ⚙️ System Panel - System monitoring and control")
        print("🔧 All panels now use refactored, focused components")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app = create_refactored_modular_ui()
        app.show()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're in the correct directory and dependencies are installed")
        print("💡 The modular_panel_ui_main_refactored.py should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🎯 TradePulse REFACTORED MODULAR PANEL UI Launcher")
    print("=" * 60)
    print("🧩 This launches the REFACTORED MODULAR architecture where each TradePulse")
    print("   module has its own dedicated panel with focused components.")
    print("🔧 All panels now use the new refactored structure with components under 200 lines.")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("modular_panel_ui_main_refactored.py").exists():
        print("❌ modular_panel_ui_main_refactored.py not found in current directory")
        print("💡 Please run this script from the TradePulse root directory")
        print("💡 Make sure the refactored modular architecture is properly set up")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install required dependencies")
        return
    
    # Check TradePulse modules
    has_tradepulse_modules = check_tradepulse_modules()
    
    # Launch UI
    if not launch_modular_ui():
        print("❌ Failed to launch REFACTORED MODULAR Panel UI")
        return
    
    print("✅ REFACTORED MODULAR Panel UI launched successfully!")

if __name__ == "__main__":
    main()
