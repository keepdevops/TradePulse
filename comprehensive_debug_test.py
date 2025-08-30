#!/usr/bin/env python3
"""
Comprehensive Debug Test
Shows exactly what's happening in the message flow step by step.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient

def comprehensive_debug():
    """Comprehensive debugging of the message flow."""
    print("🔍 Comprehensive Message Flow Debug")
    print("=" * 60)
    
    # Step 1: Create message bus client
    print("\n1️⃣ Creating Message Bus Client...")
    message_bus = MessageBusClient()
    print("   ✅ Message Bus Client created")
    
    # Step 2: Subscribe to response topics
    print("\n2️⃣ Subscribing to response topics...")
    message_bus.subscribe("data_response")
    message_bus.subscribe("visualization_response")
    print("   ✅ Subscribed to response topics")
    
    # Step 3: Start listening
    print("\n3️⃣ Starting message listener...")
    message_bus.start_listening()
    print("   ✅ Message listener started")
    
    # Step 4: Wait for subscription to be ready
    print("\n4️⃣ Waiting for subscription to be ready...")
    time.sleep(3)
    print("   ✅ Ready to send messages")
    
    # Step 5: Send test messages
    print("\n5️⃣ Sending test messages...")
    
    # Test 1: Data request
    print("\n   📤 Sending data request...")
    data_request = {
        "id": "debug_test_001",
        "type": "historical_data",
        "symbol": "AAPL",
        "period": "1d",
        "interval": "1h",
        "limit": 50
    }
    
    success1 = message_bus.publish("data_request", data_request)
    print(f"   📤 Data request sent: {'✅ Success' if success1 else '❌ Failed'}")
    
    # Test 2: Visualization request
    print("\n   📤 Sending visualization request...")
    viz_request = {
        "id": "debug_test_002",
        "type": "create_chart",
        "chart_type": "candlestick",
        "symbol": "AAPL",
        "period": "1d",
        "interval": "1h",
        "indicators": ["sma_20", "rsi"]
    }
    
    success2 = message_bus.publish("visualization_request", viz_request)
    print(f"   📤 Visualization request sent: {'✅ Success' if success2 else '❌ Failed'}")
    
    # Step 6: Listen for responses
    print("\n6️⃣ Listening for responses...")
    print("   ⏳ Listening for 15 seconds...")
    
    start_time = time.time()
    responses_received = 0
    
    while time.time() - start_time < 15:
        try:
            elapsed = int(time.time() - start_time)
            print(f"   🔍 Checking for messages... (elapsed: {elapsed}s)")
            
            message = message_bus.receive(timeout=1000)
            if message:
                responses_received += 1
                print(f"   📥 Received message #{responses_received}: {message}")
                
                # Check message structure
                if 'topic' in message:
                    print(f"      📋 Topic: {message['topic']}")
                if 'data' in message:
                    print(f"      📋 Data: {message['data']}")
                if 'timestamp' in message:
                    print(f"      📋 Timestamp: {message['timestamp']}")
            else:
                print("   ⏳ No message received")
                
        except Exception as e:
            print(f"   ❌ Error receiving message: {e}")
            break
    
    # Step 7: Summary
    print(f"\n7️⃣ Test Summary:")
    print(f"   📊 Total responses received: {responses_received}")
    
    if responses_received == 0:
        print("\n   ❌ No responses received!")
        print("   🔍 Possible issues:")
        print("      - Data Grid module not running")
        print("      - Message handler not properly integrated")
        print("      - Message format mismatch")
        print("      - Network/ZeroMQ issues")
    else:
        print(f"\n   ✅ Successfully received {responses_received} responses!")
    
    # Step 8: Cleanup
    print("\n8️⃣ Cleaning up...")
    message_bus.stop_listening()
    message_bus.close()
    print("   ✅ Cleanup completed")

if __name__ == "__main__":
    comprehensive_debug()
