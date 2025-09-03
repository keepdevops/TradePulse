#!/usr/bin/env python3
"""
TradePulse Integrated Panels Test Module
Tests integrated panels functionality
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_tests():
    """Test integrated panels functionality"""
    print("🔗 Testing Integrated Panels...")
    try:
        from integrated_panels.integrated_panel_ui import TradePulseIntegratedUI
        from integrated_panels.ui_orchestrator import UIOrchestrator
        from integrated_panels.performance_tracker import PerformanceTracker
        from integrated_panels.tradepulse_integration import TradePulseIntegration
        from integrated_panels.system_monitor import SystemMonitor
        
        print("  ✅ All integrated panel classes imported successfully")
        
        # Test UI Orchestrator
        ui_orchestrator = UIOrchestrator()
        print("  ✅ UIOrchestrator created successfully")
        
        # Test Performance Tracker
        performance_tracker = PerformanceTracker()
        print("  ✅ PerformanceTracker created successfully")
        
        # Test TradePulse Integration
        tradepulse_integration = TradePulseIntegration()
        print("  ✅ TradePulseIntegration created successfully")
        
        # Test System Monitor
        system_monitor = SystemMonitor()
        print("  ✅ SystemMonitor created successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Integrated panels test failed: {e}")
        return False

if __name__ == "__main__":
    run_tests()
