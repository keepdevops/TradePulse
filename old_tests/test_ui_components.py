#!/usr/bin/env python3
"""
TradePulse UI Components Test Module
Tests refactored UI components functionality
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_tests():
    """Test refactored UI components functionality"""
    print("🎨 Testing UI Components...")
    try:
        from ui_components.base_component import BaseComponent
        from ui_components.data_manager import DataManager
        from ui_components.chart_component import ChartComponent
        from ui_components.tradepulse_ui import TradePulseModularUI
        from ui_components.ui_callbacks import UICallbacks
        
        print("  ✅ All UI component classes imported successfully")
        
        # Test Base Component (abstract class - can't instantiate directly)
        print("  ✅ BaseComponent class imported successfully (abstract)")
        
        # Test Data Manager
        data_manager = DataManager()
        print("  ✅ DataManager created successfully")
        
        # Test Chart Component
        chart_component = ChartComponent(data_manager)
        print("  ✅ ChartComponent created successfully")
        
        # Test TradePulse UI
        ui = TradePulseModularUI()
        print("  ✅ TradePulseModularUI created successfully")
        
        # Test UI Callbacks
        callbacks = UICallbacks(ui)
        print("  ✅ UICallbacks created successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ UI components test failed: {e}")
        return False

if __name__ == "__main__":
    run_tests()
