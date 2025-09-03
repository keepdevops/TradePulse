#!/usr/bin/env python3
"""
TradePulse Panel UI - Trading Event Handlers
Trading-specific event handling logic
"""

import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class TradingEventHandler:
    """Handles trading-specific events"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
    
    def start_trading(self, event):
        """Start trading session"""
        self.components['control'].set_trading_status(True)
        logger.info("🚀 Trading session started")
    
    def stop_trading(self, event):
        """Stop trading session"""
        self.components['control'].set_trading_status(False)
        logger.info("⏹ Trading session stopped")
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        current_symbol = event.new
        self.components['chart'].update_charts(current_symbol)
        self.components['data_display'].update_price_display(current_symbol)

class PortfolioEventHandler:
    """Handles portfolio-related events"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using selected strategy"""
        try:
            strategy = self.components['portfolio'].components['optimization_strategy'].value
            risk_tolerance = self.components['portfolio'].components['risk_tolerance'].value
            
            logger.info(f"🔧 Optimizing portfolio with {strategy} strategy, {risk_tolerance} risk tolerance")
            
            # Simulate optimization
            self.data_manager.portfolio_data['performance']['total_return'] += 0.01
            self.components['portfolio'].update_portfolio_display()
            
            # Add alert
            self.components['alert'].add_alert_message(f"Portfolio optimized using {strategy} strategy")
            
            logger.info(f"✅ Portfolio optimization completed")
            
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
    
    def place_order(self, event):
        """Place trading order"""
        try:
            symbol = self.components['portfolio'].components['order_symbol'].value
            quantity = self.components['portfolio'].components['order_quantity'].value
            order_type = self.components['portfolio'].components['order_type'].value
            price = self.components['portfolio'].components['order_price'].value
            
            logger.info(f"📋 Placing {order_type} order: {quantity} shares of {symbol} at ${price}")
            
            # Simulate order placement
            order_id = f"ORD_{int(time.time())}"
            
            # Update portfolio
            if symbol not in self.data_manager.portfolio_data['positions']:
                self.data_manager.portfolio_data['positions'][symbol] = {
                    'shares': 0,
                    'avg_price': 0.0,
                    'current_price': price if price > 0 else 150.0
                }
            
            # Add to positions
            current_pos = self.data_manager.portfolio_data['positions'][symbol]
            current_pos['shares'] += quantity
            current_pos['avg_price'] = (current_pos['avg_price'] * (current_pos['shares'] - quantity) + 
                                      price * quantity) / current_pos['shares']
            
            # Update portfolio display
            self.components['portfolio'].update_portfolio_display()
            
            # Add alert
            self.components['alert'].add_alert_message(f"Order placed: {quantity} shares of {symbol} at ${price}")
            
            logger.info(f"✅ Order {order_id} placed successfully")
            
        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}")

class MLEventHandler:
    """Handles ML-related events"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
    
    def generate_prediction(self, event):
        """Generate ML prediction"""
        try:
            model = self.components['ml'].get_selected_model()
            symbol = self.components['control'].get_current_symbol()
            
            logger.info(f"🤖 Generating prediction using {model} model for {symbol}")
            
            # Simulate prediction
            if model == 'Ensemble':
                prediction = "Strong Buy"
                confidence = 0.85
            elif model == 'ADM':
                prediction = "Buy"
                confidence = 0.78
            elif model == 'CIPO':
                prediction = "Hold"
                confidence = 0.65
            else:  # BICIPO
                prediction = "Sell"
                confidence = 0.72
            
            # Add alert
            self.components['alert'].add_alert_message(f"{model} prediction for {symbol}: {prediction} (confidence: {confidence:.2f})")
            
            logger.info(f"✅ {model} prediction: {prediction} (confidence: {confidence:.2f})")
            
        except Exception as e:
            logger.error(f"❌ Prediction generation failed: {e}")

class AlertEventHandler:
    """Handles alert-related events"""
    
    def __init__(self, data_manager, components):
        self.data_manager = data_manager
        self.components = components
    
    def add_alert(self, event):
        """Add price alert"""
        try:
            high_price = self.components['alert'].components['alert_price_high'].value
            low_price = self.components['alert'].components['alert_price_low'].value
            current_symbol = self.components['control'].get_current_symbol()
            
            if high_price > 0 or low_price > 0:
                alert_text = f"Alert set for {current_symbol}: "
                if high_price > 0:
                    alert_text += f"High: ${high_price} "
                if low_price > 0:
                    alert_text += f"Low: ${low_price}"
                
                self.components['alert'].add_alert_message(alert_text)
                logger.info(f"🔔 {alert_text}")
            
        except Exception as e:
            logger.error(f"❌ Alert creation failed: {e}")
