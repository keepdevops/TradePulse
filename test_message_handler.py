#!/usr/bin/env python3
"""
Test Message Handler Directly
Tests the message handler class directly to see if it works.
"""

import sys
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from data_grid.message_handler import DataGridMessageHandler
from utils.message_bus_client import MessageBusClient

def test_message_handler():
    """Test the message handler directly."""
    print("🧪 Testing Message Handler Directly...")
    
    try:
        # Create a mock message bus client
        message_bus = MessageBusClient()
        
        # Create mock fetcher and visualizer (None for now)
        fetcher = None
        visualizer = None
        
        # Create message handler
        handler = DataGridMessageHandler(message_bus, fetcher, visualizer)
        print("✅ Message handler created successfully")
        
        # Test the handler methods
        handlers = handler.get_message_handlers()
        print(f"📋 Available handlers: {list(handlers.keys())}")
        
        # Test data request handling
        print("\n🔍 Testing data request handler...")
        test_data = {
            "id": "direct_test",
            "type": "historical_data",
            "symbol": "AAPL",
            "period": "1d",
            "interval": "1h",
            "limit": 100
        }
        
        # Call the handler directly
        handler.handle_data_request("data_request", test_data)
        print("✅ Data request handler executed successfully")
        
        # Test visualization request handling
        print("\n📊 Testing visualization request handler...")
        test_viz_data = {
            "id": "direct_viz_test",
            "type": "create_chart",
            "chart_type": "candlestick",
            "symbol": "AAPL",
            "period": "1d",
            "interval": "1h",
            "indicators": ["sma_20", "rsi"]
        }
        
        # Call the handler directly
        handler.handle_visualization_request("visualization_request", test_viz_data)
        print("✅ Visualization request handler executed successfully")
        
        # Close message bus
        message_bus.close()
        print("\n🎉 All message handler tests passed!")
        
    except Exception as e:
        print(f"❌ Message handler test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_message_handler()
