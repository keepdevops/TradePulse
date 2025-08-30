#!/usr/bin/env python3
"""
Test Portfolio Optimization
Tests the portfolio optimization functionality and message handling.
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


def test_portfolio_optimization():
    """Test portfolio optimization request."""
    print("\n🔍 Testing Portfolio Optimization...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Subscribe to response topic
        message_bus.subscribe("portfolio_optimization_response")
        
        # Start listening
        message_bus.start_listening()
        time.sleep(2)  # Wait for subscription to be ready
        
        # Send portfolio optimization request
        optimization_request = {
            "id": "test_opt_001",
            "type": "portfolio_optimization",
            "optimization_type": "markowitz",
            "risk_tolerance": "moderate",
            "constraints": {
                "min_weight": 0.05,
                "max_weight": 0.4
            },
            "target_return": 0.08,
            "target_volatility": 0.15
        }
        
        print(f"📤 Sending portfolio optimization request: {optimization_request}")
        success = message_bus.publish("portfolio_optimization_request", optimization_request)
        print(f"   Publish result: {'✅ Success' if success else '❌ Failed'}")
        
        # Wait for response
        print("⏳ Waiting for response...")
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Wait up to 10 seconds
            try:
                message = message_bus.receive(timeout=1000)
                if message:
                    print(f"📥 Received response: {message}")
                    
                    if 'data' in message and 'type' in message['data']:
                        response_data = message['data']
                        if response_data['type'] == 'portfolio_optimization_response':
                            if response_data['status'] == 'success':
                                print("✅ Portfolio optimization completed successfully!")
                                
                                # Display optimization results
                                opt_result = response_data['optimization_result']
                                print(f"   Optimization Type: {opt_result['optimization_type']}")
                                print(f"   Risk Tolerance: {opt_result['risk_tolerance']}")
                                print(f"   Expected Return: {opt_result['portfolio_metrics']['expected_return']:.4f}")
                                print(f"   Volatility: {opt_result['portfolio_metrics']['volatility']:.4f}")
                                print(f"   Sharpe Ratio: {opt_result['portfolio_metrics']['sharpe_ratio']:.4f}")
                                
                                # Display optimal weights
                                print("   Optimal Weights:")
                                for asset, weight in opt_result['optimal_weights'].items():
                                    print(f"     {asset}: {weight:.4f}")
                                
                                break
                            else:
                                print(f"❌ Portfolio optimization failed: {response_data.get('error', 'Unknown error')}")
                                break
                    else:
                        print(f"📥 Received other message: {message}")
                        
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        # Close connection
        message_bus.close()
        print("✅ Portfolio optimization test completed")
        
    except Exception as e:
        print(f"❌ Portfolio optimization test failed: {e}")


def test_strategy_request():
    """Test strategy generation request."""
    print("\n🧠 Testing Strategy Generation...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Subscribe to response topic
        message_bus.subscribe("strategy_response")
        
        # Start listening
        message_bus.start_listening()
        time.sleep(2)  # Wait for subscription to be ready
        
        # Send strategy request
        strategy_request = {
            "id": "test_strategy_001",
            "type": "strategy_generation",
            "strategy_type": "momentum",
            "market_conditions": "bullish",
            "risk_tolerance": "moderate",
            "timeframe": "1d"
        }
        
        print(f"📤 Sending strategy request: {strategy_request}")
        success = message_bus.publish("strategy_request", strategy_request)
        print(f"   Publish result: {'✅ Success' if success else '❌ Failed'}")
        
        # Wait for response
        print("⏳ Waiting for response...")
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Wait up to 10 seconds
            try:
                message = message_bus.receive(timeout=1000)
                if message:
                    print(f"📥 Received response: {message}")
                    
                    if 'data' in message and 'type' in message['data']:
                        response_data = message['data']
                        if response_data['type'] == 'strategy_response':
                            if response_data['status'] == 'success':
                                print("✅ Strategy generation completed successfully!")
                                
                                # Display strategy details
                                strategy = response_data['strategy']
                                print(f"   Strategy Type: {strategy.get('type', 'Unknown')}")
                                print(f"   Risk Tolerance: {strategy.get('metadata', {}).get('risk_tolerance', 'Unknown')}")
                                
                                break
                            else:
                                print(f"❌ Strategy generation failed: {response_data.get('error', 'Unknown error')}")
                                break
                    else:
                        print(f"📥 Received other message: {message}")
                        
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        # Close connection
        message_bus.close()
        print("✅ Strategy generation test completed")
        
    except Exception as e:
        print(f"❌ Strategy generation test failed: {e}")


def test_risk_assessment():
    """Test risk assessment request."""
    print("\n⚠️ Testing Risk Assessment...")
    
    try:
        # Create message bus client
        message_bus = MessageBusClient()
        
        # Subscribe to response topic
        message_bus.subscribe("risk_assessment_response")
        
        # Start listening
        message_bus.start_listening()
        time.sleep(2)  # Wait for subscription to be ready
        
        # Send risk assessment request
        risk_request = {
            "id": "test_risk_001",
            "type": "risk_assessment",
            "risk_tolerance": "moderate",
            "portfolio_data": {
                "positions": {
                    "AAPL": {"weight": 0.4, "value": 40000},
                    "GOOGL": {"weight": 0.3, "value": 30000},
                    "MSFT": {"weight": 0.3, "value": 30000}
                },
                "total_value": 100000,
                "cash": 0
            }
        }
        
        print(f"📤 Sending risk assessment request: {risk_request}")
        success = message_bus.publish("risk_assessment_request", risk_request)
        print(f"   Publish result: {'✅ Success' if success else '❌ Failed'}")
        
        # Wait for response
        print("⏳ Waiting for response...")
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Wait up to 10 seconds
            try:
                message = message_bus.receive(timeout=1000)
                if message:
                    print(f"📥 Received response: {message}")
                    
                    if 'data' in message and 'type' in message['data']:
                        response_data = message['data']
                        if response_data['type'] == 'risk_assessment_response':
                            if response_data['status'] == 'success':
                                print("✅ Risk assessment completed successfully!")
                                
                                # Display risk metrics
                                risk_metrics = response_data['risk_metrics']
                                print(f"   Risk Score: {risk_metrics.get('risk_score', 'Unknown')}")
                                print(f"   Position Count: {risk_metrics.get('position_count', 'Unknown')}")
                                print(f"   Max Position Weight: {risk_metrics.get('max_position_weight', 'Unknown'):.4f}")
                                print(f"   Diversification Score: {risk_metrics.get('diversification_score', 'Unknown'):.4f}")
                                
                                break
                            else:
                                print(f"❌ Risk assessment failed: {response_data.get('error', 'Unknown error')}")
                                break
                    else:
                        print(f"📥 Received other message: {message}")
                        
            except Exception as e:
                print(f"Error receiving message: {e}")
                break
        
        # Close connection
        message_bus.close()
        print("✅ Risk assessment test completed")
        
    except Exception as e:
        print(f"❌ Risk assessment test failed: {e}")


def main():
    """Run all tests."""
    print("🚀 Starting Portfolio Optimization Tests")
    print("=" * 60)
    
    # Test portfolio optimization
    test_portfolio_optimization()
    
    # Test strategy generation
    test_strategy_request()
    
    # Test risk assessment
    test_risk_assessment()
    
    print("\n🎉 All tests completed!")


if __name__ == "__main__":
    main()
