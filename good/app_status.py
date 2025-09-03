#!/usr/bin/env python3
"""
TradePulse Application Status Script
Shows the current status of the application and the 299 files under 200 lines being used
"""

import os
import sys
import subprocess
from pathlib import Path
import psutil

def get_app_status():
    """Get the current application status"""
    print("=" * 60)
    print("🚀 TRADEPULSE APPLICATION STATUS")
    print("=" * 60)
    
    # Check if application is running
    app_running = False
    app_pid = None
    app_port = None
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'python' and any('simple_launcher' in cmd for cmd in proc.info['cmdline'] if cmd):
                app_running = True
                app_pid = proc.info['pid']
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    if app_running:
        print(f"✅ Application Status: RUNNING")
        print(f"🔄 Process ID: {app_pid}")
        print(f"🌐 Access URL: http://localhost:5006")
        print(f"📊 Port: 5006 (wsm-server)")
    else:
        print("❌ Application Status: NOT RUNNING")
    
    print()
    
    # Check port status
    try:
        result = subprocess.run(['lsof', '-i', ':5006'], capture_output=True, text=True)
        if result.returncode == 0:
            print("🔌 Port 5006 Status: IN USE")
            print("   " + result.stdout.strip().replace('\n', '\n   '))
        else:
            print("🔌 Port 5006 Status: AVAILABLE")
    except Exception as e:
        print(f"🔌 Port 5006 Status: ERROR - {e}")
    
    print()

def show_files_summary():
    """Show summary of the 299 files under 200 lines"""
    print("=" * 60)
    print("📁 FILES UNDER 200 LINES SUMMARY")
    print("=" * 60)
    
    # Count files by directory
    directories = {}
    total_files = 0
    
    try:
        result = subprocess.run([
            'find', '.', '-type', 'f', '-name', '*.py', '-exec', 'wc', '-l', '{}', '+'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        lines = int(parts[0])
                        file_path = parts[1]
                        
                        if lines < 200:
                            total_files += 1
                            directory = Path(file_path).parent.name
                            directories[directory] = directories.get(directory, 0) + 1
            
            print(f"📊 Total Files Under 200 Lines: {total_files}")
            print()
            print("📂 Files by Directory:")
            for directory, count in sorted(directories.items(), key=lambda x: x[1], reverse=True):
                print(f"   {directory}: {count} files")
        else:
            print("❌ Could not analyze files")
            
    except Exception as e:
        print(f"❌ Error analyzing files: {e}")
    
    print()

def show_key_components():
    """Show key components being used"""
    print("=" * 60)
    print("🔧 KEY COMPONENTS IN USE")
    print("=" * 60)
    
    key_components = [
        "modular_panels/ai/",
        "modular_panels/alerts/",
        "modular_panels/charts/",
        "modular_panels/data/",
        "modular_panels/portfolio/",
        "ui_components/",
        "ui_panels/",
        "auth/",
        "integrated_panels/",
        "demo_panels/"
    ]
    
    for component in key_components:
        if os.path.exists(component):
            file_count = len([f for f in Path(component).rglob("*.py") if f.stat().st_size > 0])
            print(f"✅ {component}: {file_count} Python files")
        else:
            print(f"❌ {component}: Not found")
    
    print()

def show_launch_options():
    """Show available launch options"""
    print("=" * 60)
    print("🚀 AVAILABLE LAUNCH OPTIONS")
    print("=" * 60)
    
    launch_scripts = [
        "run_tradepulse_app.py",
        "simple_launcher.py",
        "modular_panel_ui_main_refactored.py",
        "launch_demo_ui.py",
        "launch_integrated_ui.py",
        "launch_modular_ui.py",
        "launch_panel_ui.py"
    ]
    
    for script in launch_scripts:
        if os.path.exists(script):
            size = os.path.getsize(script)
            print(f"✅ {script} ({size} bytes)")
        else:
            print(f"❌ {script} (not found)")
    
    print()
    print("💡 To start the application:")
    print("   python run_tradepulse_app.py")
    print("   or")
    print("   python simple_launcher.py")

def main():
    """Main function"""
    get_app_status()
    show_files_summary()
    show_key_components()
    show_launch_options()

if __name__ == "__main__":
    main()
