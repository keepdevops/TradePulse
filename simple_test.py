#!/usr/bin/env python3
"""
Simple Communication Test
Tests a single message to see if the data_grid module responds.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient

def test_single_message():
    """Test sending a single message and listening for response."""
    print("🧪 Testing Single Message Communication...")
    
    # Create message bus client
    message_bus = MessageBusClient()
    
    # Subscribe to response topic
    message_bus.subscribe("data_response")
    
    # Send a simple data request
    data_request = {
        "id": "simple_test",
        "type": "historical_data",
        "symbol": "AAPL",
        "period": "1d",
        "interval": "1h",
        "limit": 50
    }
    
    print(f"📤 Sending data request: {data_request}")
    message_bus.publish("data_request", data_request)
    
    # Listen for response
    print("📡 Listening for response...")
    start_time = time.time()
    
    while time.time() - start_time < 10:  # Listen for 10 seconds
        try:
            message = message_bus.receive(timeout=1000)
            if message:
                print(f"�� Received response: {message}")
                break
        except Exception as e:
            print(f"Error receiving: {e}")
            break
    
    # Close connection
    message_bus.close()
    print("✅ Test completed")

if __name__ == "__main__":
    test_single_message()