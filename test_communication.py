#!/usr/bin/env python3
"""
Test Module Communication
Tests the message bus communication between TradePulse modules.
"""

import sys
import time
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


def test_data_request():
    """Test sending a data request to the Data Grid module."""
    print("\n🔍 Testing Data Request Communication...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Send a data request
        data_request = {
            "type": "historical_data",
            "symbol": "AAPL",
            "period": "1d",
            "interval": "1h",
            "limit": 100
        }
        
        print(f"📤 Sending data request: {data_request}")
        message_bus.publish("data_request", json.dumps(data_request))
        
        # Wait for response
        print("⏳ Waiting for response...")
        time.sleep(2)
        
        # Close connection
        message_bus.close()
        print("✅ Data request test completed")
        
    except Exception as e:
        print(f"❌ Data request test failed: {e}")


def test_training_request():
    """Test sending a training request to the Models Grid module."""
    print("\n🤖 Testing Training Request Communication...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Send a training request
        training_request = {
            "type": "train_model",
            "model_type": "adm",
            "data_source": "sample_data",
            "target_column": "returns",
            "features": ["price", "volume", "rsi", "macd"]
        }
        
        print(f"📤 Sending training request: {training_request}")
        message_bus.publish("training_request", json.dumps(training_request))
        
        # Wait for response
        print("⏳ Waiting for response...")
        time.sleep(2)
        
        # Close connection
        message_bus.close()
        print("✅ Training request test completed")
        
    except Exception as e:
        print(f"❌ Training request test failed: {e}")


def test_strategy_request():
    """Test sending a strategy request to the AI Module."""
    print("\n🧠 Testing Strategy Request Communication...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Send a strategy request
        strategy_request = {
            "type": "generate_strategy",
            "strategy_type": "trend_following",
            "market_conditions": "bullish",
            "risk_tolerance": "moderate",
            "timeframe": "1h"
        }
        
        print(f"📤 Sending strategy request: {strategy_request}")
        message_bus.publish("strategy_request", json.dumps(strategy_request))
        
        # Wait for response
        print("⏳ Waiting for response...")
        time.sleep(2)
        
        # Close connection
        message_bus.close()
        print("✅ Strategy request test completed")
        
    except Exception as e:
        print(f"❌ Strategy request test failed: {e}")


def test_visualization_request():
    """Test sending a visualization request to the Data Grid module."""
    print("\n📊 Testing Visualization Request Communication...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Send a visualization request
        viz_request = {
            "type": "create_chart",
            "chart_type": "candlestick",
            "symbol": "AAPL",
            "period": "1d",
            "interval": "1h",
            "indicators": ["sma_20", "rsi"]
        }
        
        print(f"📤 Sending visualization request: {viz_request}")
        message_bus.publish("visualization_request", json.dumps(viz_request))
        
        # Wait for response
        print("⏳ Waiting for response...")
        time.sleep(2)
        
        # Close connection
        message_bus.close()
        print("✅ Visualization request test completed")
        
    except Exception as e:
        print(f"❌ Visualization request test failed: {e}")


def test_heartbeat_monitoring():
    """Test monitoring module heartbeats."""
    print("\n💓 Testing Heartbeat Monitoring...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Subscribe to heartbeat topic
        message_bus.subscribe("heartbeat")
        
        print("📡 Listening for heartbeats...")
        print("⏳ Waiting 10 seconds for heartbeats...")
        
        # Listen for heartbeats
        start_time = time.time()
        heartbeat_count = 0
        
        while time.time() - start_time < 10:
            try:
                # Check for messages (non-blocking)
                message = message_bus.receive_message(timeout=1)
                if message:
                    heartbeat_count += 1
                    print(f"💓 Received heartbeat: {message}")
            except:
                pass
        
        print(f"✅ Heartbeat monitoring completed. Received {heartbeat_count} heartbeats.")
        
        # Close connection
        message_bus.close()
        
    except Exception as e:
        print(f"❌ Heartbeat monitoring failed: {e}")


def main():
    """Run all communication tests."""
    print("🚀 TradePulse Module Communication Test")
    print("=" * 50)
    
    # Test each type of communication
    test_data_request()
    test_training_request()
    test_strategy_request()
    test_visualization_request()
    test_heartbeat_monitoring()
    
    print("\n🎉 All communication tests completed!")
    print("\n📋 Summary:")
    print("- Data Grid: Receives data_request and visualization_request")
    print("- Models Grid: Receives training_request and prediction_request")
    print("- AI Module: Receives strategy_request and risk_assessment_request")
    print("- All modules send heartbeats for monitoring")


if __name__ == "__main__":
    main()
