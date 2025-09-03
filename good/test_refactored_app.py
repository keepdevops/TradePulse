#!/usr/bin/env python3
"""
Simple test script for the refactored TradePulse application
"""

import requests
import time
import sys
from pathlib import Path

def test_application_availability():
    """Test if the application is responding"""
    try:
        print("🔍 Testing application availability...")
        response = requests.get("http://localhost:5006", timeout=5)
        if response.status_code == 200:
            print("✅ Application is responding (HTTP 200)")
            return True
        else:
            print(f"❌ Application returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Application not accessible: {e}")
        return False

def test_panel_imports():
    """Test if the main panels can be imported"""
    try:
        print("\n🔍 Testing panel imports...")
        
        # Test main panels
        from modular_panels.data_panel import DataPanel
        print("✅ DataPanel imported successfully")
        
        from modular_panels.models_panel import ModelsPanel
        print("✅ ModelsPanel imported successfully")
        
        from modular_panels.portfolio_panel import PortfolioPanel
        print("✅ PortfolioPanel imported successfully")
        
        from modular_panels.ai_panel import AIPanel
        print("✅ AIPanel imported successfully")
        
        from modular_panels.charts_panel import ChartsPanel
        print("✅ ChartsPanel imported successfully")
        
        from modular_panels.alerts_panel import AlertsPanel
        print("✅ AlertsPanel imported successfully")
        
        from modular_panels.system_panel import SystemPanel
        print("✅ SystemPanel imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Panel import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during panel import: {e}")
        return False

def test_data_components():
    """Test if data components can be imported"""
    try:
        print("\n🔍 Testing data components...")
        
        # Test data manager
        from ui_components.data_manager import DataManager
        print("✅ DataManager imported successfully")
        
        # Test data access
        from ui_components.data_access import DataAccessManager
        print("✅ DataAccessManager imported successfully")
        
        # Test dashboard manager
        from ui_components.dashboard_manager import DashboardManager
        print("✅ DashboardManager imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Data component import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during data component import: {e}")
        return False

def test_file_structure():
    """Test if the expected file structure exists"""
    print("\n🔍 Testing file structure...")
    
    expected_files = [
        "modular_panel_ui_main_refactored.py",
        "modular_panels/data_panel.py",
        "modular_panels/models_panel.py",
        "modular_panels/portfolio_panel.py",
        "modular_panels/ai_panel.py",
        "modular_panels/charts_panel.py",
        "modular_panels/alerts_panel.py",
        "modular_panels/system_panel.py",
        "ui_components/data_manager.py",
        "ui_components/data_access.py",
        "ui_components/dashboard_manager.py"
    ]
    
    missing_files = []
    for file_path in expected_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path} exists")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 TradePulse Refactored Application Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Panel Imports", test_panel_imports),
        ("Data Components", test_data_components),
        ("Application Availability", test_application_availability)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Refactored application is working correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

