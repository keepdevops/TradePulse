#!/usr/bin/env python3
"""
TradePulse UI Panels Test Module
Tests UI panels functionality
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_tests():
    """Test UI panels functionality"""
    print("🎨 Testing UI Panels...")
    try:
        from ui_panels.panel_ui import TradePulsePanelUI
        from ui_panels.data_manager import DataManager
        from ui_panels.chart_manager import ChartManager
        
        print("  ✅ All UI panel classes imported successfully")
        
        # Test Data Manager
        data_manager = DataManager()
        print("  ✅ DataManager created successfully")
        
        # Test Chart Manager
        chart_manager = ChartManager()
        print("  ✅ ChartManager created successfully")
        
        # Test TradePulse UI
        ui = TradePulsePanelUI()
        print("  ✅ TradePulsePanelUI created successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ UI panels test failed: {e}")
        return False

if __name__ == "__main__":
    run_tests()
