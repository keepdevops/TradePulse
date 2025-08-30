#!/usr/bin/env python3
"""
Interactive Module Communication Test
Tests two-way communication with TradePulse modules.
"""

import sys
import time
import json
import threading
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient
from utils.logger import setup_logger

logger = setup_logger(__name__)


class InteractiveTester:
    """Interactive tester for module communication."""
    
    def __init__(self):
        """Initialize the interactive tester."""
        self.message_bus = MessageBusClient()
        self.responses = []
        self.running = True
        
    def start_listening(self):
        """Start listening for responses in a separate thread."""
        def listen():
            self.message_bus.subscribe("response")
            self.message_bus.subscribe("data_response")
            self.message_bus.subscribe("training_response")
            self.message_bus.subscribe("strategy_response")
            self.message_bus.subscribe("visualization_response")
            
            while self.running:
                try:
                    message = self.message_bus.receive_message(timeout=1)
                    if message:
                        self.responses.append(message)
                        print(f"📥 Received: {message}")
                except:
                    pass
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
        return thread
    
    def send_message(self, topic, message):
        """Send a message to a specific topic."""
        try:
            print(f"📤 Sending to {topic}: {message}")
            self.message_bus.publish(topic, json.dumps(message))
            return True
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
            return False
    
    def test_data_workflow(self):
        """Test a complete data workflow."""
        print("\n🔍 Testing Data Workflow...")
        
        # Step 1: Request data
        data_request = {
            "id": "test_001",
            "type": "historical_data",
            "symbol": "AAPL",
            "period": "1d",
            "interval": "1h",
            "limit": 100
        }
        
        if self.send_message("data_request", data_request):
            print("⏳ Waiting for data response...")
            time.sleep(3)
            
            # Step 2: Request visualization
            viz_request = {
                "id": "test_002",
                "type": "create_chart",
                "chart_type": "candlestick",
                "symbol": "AAPL",
                "period": "1d",
                "interval": "1h",
                "indicators": ["sma_20", "rsi"]
            }
            
            if self.send_message("visualization_request", viz_request):
                print("⏳ Waiting for visualization response...")
                time.sleep(3)
    
    def test_ml_workflow(self):
        """Test a complete ML workflow."""
        print("\n🤖 Testing ML Workflow...")
        
        # Step 1: Request model training
        training_request = {
            "id": "test_003",
            "type": "train_model",
            "model_type": "adm",
            "data_source": "sample_data",
            "target_column": "returns",
            "features": ["price", "volume", "rsi", "macd"]
        }
        
        if self.send_message("training_request", training_request):
            print("⏳ Waiting for training response...")
            time.sleep(3)
            
            # Step 2: Request prediction
            prediction_request = {
                "id": "test_004",
                "type": "make_prediction",
                "model_type": "adm",
                "data": "sample_input_data"
            }
            
            if self.send_message("prediction_request", prediction_request):
                print("⏳ Waiting for prediction response...")
                time.sleep(3)
    
    def test_ai_workflow(self):
        """Test a complete AI workflow."""
        print("\n🧠 Testing AI Workflow...")
        
        # Step 1: Request strategy generation
        strategy_request = {
            "id": "test_005",
            "type": "generate_strategy",
            "strategy_type": "trend_following",
            "market_conditions": "bullish",
            "risk_tolerance": "moderate",
            "timeframe": "1h"
        }
        
        if self.send_message("strategy_request", strategy_request):
            print("⏳ Waiting for strategy response...")
            time.sleep(3)
            
            # Step 2: Request risk assessment
            risk_request = {
                "id": "test_006",
                "type": "assess_risk",
                "strategy": "trend_following",
                "position_size": 1000,
                "stop_loss": 0.02
            }
            
            if self.send_message("risk_assessment_request", risk_request):
                print("⏳ Waiting for risk assessment response...")
                time.sleep(3)
    
    def run_all_tests(self):
        """Run all interactive tests."""
        print("🚀 Interactive TradePulse Communication Test")
        print("=" * 60)
        print("This test will send messages and listen for responses...")
        
        # Start listening for responses
        listen_thread = self.start_listening()
        time.sleep(2)  # Give time for subscription
        
        # Run workflow tests
        self.test_data_workflow()
        self.test_ml_workflow()
        self.test_ai_workflow()
        
        # Wait a bit more for any delayed responses
        print("\n⏳ Waiting for any delayed responses...")
        time.sleep(5)
        
        # Show summary
        print(f"\n📊 Test Summary:")
        print(f"Total responses received: {len(self.responses)}")
        
        if self.responses:
            print("\n📥 Responses received:")
            for i, response in enumerate(self.responses, 1):
                print(f"  {i}. {response}")
        else:
            print("  No responses received - modules may not be processing messages yet")
        
        print("\n💡 Note: If no responses were received, the modules may need to be")
        print("   updated to handle these specific message types or respond to them.")
        
        # Cleanup
        self.running = False
        self.message_bus.close()
        listen_thread.join(timeout=1)


def main():
    """Run the interactive communication test."""
    tester = InteractiveTester()
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        tester.running = False
        tester.message_bus.close()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        tester.running = False
        tester.message_bus.close()


if __name__ == "__main__":
    main()
