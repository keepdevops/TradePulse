#!/usr/bin/env python3
"""
Message Format Test
Tests the exact message format being sent and received.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient

def test_message_format():
    """Test the exact message format."""
    print("🔍 Testing Message Format...")
    
    # Create message bus client
    message_bus = MessageBusClient()
    
    # Subscribe to the SAME topic we're sending to (to see what we're actually sending)
    print("📡 Subscribing to 'data_request' topic to see outgoing messages...")
    message_bus.subscribe("data_request")
    
    # Start listening
    message_bus.start_listening()
    time.sleep(2)
    
    # Send a message
    print("\n📤 Sending test message...")
    test_data = {
        "id": "format_test",
        "type": "test",
        "message": "Hello Data Grid!"
    }
    
    success = message_bus.publish("data_request", test_data)
    print(f"   Publish result: {'✅ Success' if success else '❌ Failed'}")
    
    # Listen for the message we just sent
    print("\n📡 Listening for the message we just sent...")
    start_time = time.time()
    
    while time.time() - start_time < 5:
        try:
            message = message_bus.receive(timeout=1000)
            if message:
                print(f"📥 Received message: {message}")
                print(f"   Type: {type(message)}")
                print(f"   Keys: {list(message.keys()) if isinstance(message, dict) else 'Not a dict'}")
                
                if isinstance(message, dict):
                    if 'topic' in message:
                        print(f"   Topic: {message['topic']}")
                    if 'data' in message:
                        print(f"   Data: {message['data']}")
                    if 'timestamp' in message:
                        print(f"   Timestamp: {message['timestamp']}")
                break
        except Exception as e:
            print(f"   Error: {e}")
            break
    
    # Close connection
    message_bus.stop_listening()
    message_bus.close()
    print("\n✅ Message format test completed")

if __name__ == "__main__":
    test_message_format()
