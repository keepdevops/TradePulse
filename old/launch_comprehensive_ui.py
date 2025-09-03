#!/usr/bin/env python3
"""
TradePulse Comprehensive MODULAR PANEL UI Launcher
Launches any of the modular TradePulse UIs where each module has its own dedicated panel
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
    """Launch the modular panel UI with tabbed modules"""
    try:
        from modular_panel_ui_main import main
        
        print("🚀 Launching TradePulse MODULAR PANEL UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("🧩 Each module has its own dedicated panel:")
        print("   📊 Data Panel - Data management and uploads")
        print("   🤖 Models Panel - AI/ML model management")
        print("   💼 Portfolio Panel - Portfolio optimization")
        print("   🧠 AI Panel - AI-powered trading strategies")
        print("   📈 Charts Panel - Advanced charting and analysis")
        print("   🔔 Alerts Panel - Trading alerts and notifications")
        print("   ⚙️ System Panel - System monitoring and control")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app, port, host = main()
        app.show()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 The modular_panel_ui_main.py should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False

def launch_integrated_ui():
    """Launch the integrated panel UI"""
    try:
        from integrated_panels.integrated_panel_ui import main
        
        print("🚀 Launching TradePulse Integrated Panel UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app = main()
        app.show()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 The integrated_panels components should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False

def launch_panel_ui():
    """Launch the standard panel UI"""
    try:
        from ui_panels.panel_ui import main
        
        print("🚀 Launching TradePulse Panel UI...")
        print("📊 Starting web interface...")
        print("🌐 UI will be available at: http://localhost:5006")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        app = main()
        app.show()
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 The ui_panels components should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False

def launch_demo_ui():
    """Launch the demo panel UI"""
    try:
        from demo_panels.demo_panel_ui import TradePulseDemo
        
        print("🚀 Launching TradePulse Demo Panel UI...")
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
        print("💡 The demo_panels components should be available")
        return False
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return False

def show_menu():
    """Show the UI selection menu"""
    print("\n🎯 TradePulse MODULAR PANEL UI Launcher")
    print("=" * 60)
    print("🧩 Available UIs (Each with dedicated module panels):")
    print("1. 🧩 Modular Panel UI - Each module has its own panel (tabs)")
    print("2. 🔗 Integrated Panel UI - Full system integration")
    print("3. 📊 Panel UI - Standard trading interface")
    print("4. 🎮 Demo Panel UI - Showcase and testing")
    print("5. ❌ Exit")
    print("-" * 60)
    print("💡 The MODULAR Panel UI (#1) is the main architecture where:")
    print("   📊 Data Panel - Data management and uploads")
    print("   🤖 Models Panel - AI/ML model management")
    print("   💼 Portfolio Panel - Portfolio optimization")
    print("   🧠 AI Panel - AI-powered trading strategies")
    print("   📈 Charts Panel - Advanced charting and analysis")
    print("   🔔 Alerts Panel - Trading alerts and notifications")
    print("   ⚙️ System Panel - System monitoring and control")
    print("-" * 60)

def main():
    """Main function"""
    print("🎯 TradePulse Comprehensive MODULAR PANEL UI Launcher")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("modular_panels").exists():
        print("❌ modular_panels directory not found in current directory")
        print("💡 Please run this script from the TradePulse root directory")
        print("💡 Make sure the modular architecture is properly set up")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install required dependencies")
        return
    
    # Check TradePulse modules
    has_tradepulse_modules = check_tradepulse_modules()
    
    while True:
        show_menu()
        
        try:
            choice = input("Select UI to launch (1-5): ").strip()
            
            if choice == "1":
                if launch_modular_ui():
                    print("✅ MODULAR Panel UI launched successfully!")
                    break
                else:
                    print("❌ Failed to launch Modular Panel UI")
                    
            elif choice == "2":
                if launch_integrated_ui():
                    print("✅ Integrated Panel UI launched successfully!")
                    break
                else:
                    print("❌ Failed to launch Integrated Panel UI")
                    
            elif choice == "3":
                if launch_panel_ui():
                    print("✅ Panel UI launched successfully!")
                    break
                else:
                    print("❌ Failed to launch Panel UI")
                    
            elif choice == "4":
                if launch_demo_ui():
                    print("✅ Demo Panel UI launched successfully!")
                    break
                else:
                    print("❌ Failed to launch Demo Panel UI")
                    
            elif choice == "5":
                print("👋 Exiting TradePulse UI Launcher")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting TradePulse UI Launcher")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
