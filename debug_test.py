#!/usr/bin/env python3
"""
Debug Communication Test
Shows exactly what's happening with message flow.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient

def debug_message_flow():
    """Debug the message flow step by step."""
    print("🔍 Debugging Message Flow...")
    
    # Create message bus client
    message_bus = MessageBusClient()
    
    # Subscribe to response topic
    print("📡 Subscribing to data_response topic...")
    message_bus.subscribe("data_response")
    
    # Start listening
    print("🎧 Starting message listener...")
    message_bus.start_listening()
    
    # Wait a moment for subscription to be ready
    time.sleep(2)
    
    # Send a simple data request
    data_request = {
        "id": "debug_test",
        "type": "historical_data",
        "symbol": "AAPL",
        "period": "1d",
        "interval": "1h",
        "limit": 50
    }
    
    print(f"📤 Publishing data request to 'data_request' topic...")
    print(f"   Message: {data_request}")
    
    success = message_bus.publish("data_request", data_request)
    print(f"   Publish result: {'✅ Success' if success else '❌ Failed'}")
    
    # Listen for response with detailed logging
    print("\n📡 Listening for response (10 seconds)...")
    start_time = time.time()
    
    while time.time() - start_time < 10:
        try:
            print(f"   Checking for messages... (elapsed: {int(time.time() - start_time)}s)")
            message = message_bus.receive(timeout=1000)
            if message:
                print(f"📥 Received message: {message}")
                break
            else:
                print("   No message received")
        except Exception as e:
            print(f"   Error receiving: {e}")
            break
    
    # Stop listening
    print("🛑 Stopping message listener...")
    message_bus.stop_listening()
    
    # Close connection
    message_bus.close()
    print("✅ Debug test completed")

if __name__ == "__main__":
    debug_message_flow()
