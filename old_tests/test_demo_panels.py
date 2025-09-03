#!/usr/bin/env python3
"""
TradePulse Demo Panels Test Module
Tests refactored demo panels functionality
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def run_tests():
    """Test refactored demo panels functionality"""
    print("🎮 Testing Demo Panels...")
    try:
        from demo_panels.demo_chart_manager import DemoChartManager
        from demo_panels.demo_ui_components import DemoUIComponents
        from demo_panels.demo_data_generator import DemoDataGenerator
        from demo_panels.price_data_generator import PriceDataGenerator
        from demo_panels.portfolio_data_generator import PortfolioDataGenerator
        from demo_panels.trading_history_generator import TradingHistoryGenerator
        
        print("  ✅ All demo panel classes imported successfully")
        
        # Test Price Data Generator
        price_generator = PriceDataGenerator()
        print("  ✅ PriceDataGenerator created successfully")
        
        # Test Portfolio Data Generator
        portfolio_generator = PortfolioDataGenerator(price_generator)
        print("  ✅ PortfolioDataGenerator created successfully")
        
        # Test Trading History Generator
        trading_generator = TradingHistoryGenerator(price_generator)
        print("  ✅ TradingHistoryGenerator created successfully")
        
        # Test Demo Data Generator
        demo_generator = DemoDataGenerator()
        print("  ✅ DemoDataGenerator created successfully")
        
        # Test Demo Chart Manager
        chart_manager = DemoChartManager(demo_generator)
        print("  ✅ DemoChartManager created successfully")
        
        # Test Demo UI Components
        ui_components = DemoUIComponents(demo_generator)
        print("  ✅ DemoUIComponents created successfully")
        
        return True
    except Exception as e:
        print(f"  ❌ Demo panels test failed: {e}")
        return False

if __name__ == "__main__":
    run_tests()
