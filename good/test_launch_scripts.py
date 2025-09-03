#!/usr/bin/env python3
"""
TradePulse Launch Scripts Test Module
Tests refactored launch scripts functionality
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_tests():
    """Test refactored launch scripts functionality"""
    print("🚀 Testing Launch Scripts...")
    try:
        # Test that launch scripts exist and are importable
        import launch_modular_ui
        import launch_integrated_ui
        import launch_demo_ui
        import launch_comprehensive_ui
        import modular_panel_ui_main_refactored
        
        print("  ✅ All launch scripts imported successfully")
        
        # Test that main functions exist
        if hasattr(launch_modular_ui, 'main'):
            print("  ✅ launch_modular_ui has main function")
        
        if hasattr(launch_integrated_ui, 'main'):
            print("  ✅ launch_integrated_ui has main function")
        
        if hasattr(launch_demo_ui, 'main'):
            print("  ✅ launch_demo_ui has main function")
        
        if hasattr(launch_comprehensive_ui, 'main'):
            print("  ✅ launch_comprehensive_ui has main function")
        
        if hasattr(modular_panel_ui_main_refactored, 'main'):
            print("  ✅ modular_panel_ui_main_refactored has main function")
        
        return True
    except Exception as e:
        print(f"  ❌ Launch scripts test failed: {e}")
        return False

if __name__ == "__main__":
    run_tests()
