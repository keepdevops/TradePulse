#!/usr/bin/env python3
"""
TradePulse UI Callbacks
Callback functions for UI interactions
"""

import threading
import time
import numpy as np
import logging

logger = logging.getLogger(__name__)

class UICallbacks:
    """Callback functions for UI interactions"""
    
    def __init__(self, ui):
        self.ui = ui
    
    def on_symbol_change(self, event):
        """Handle symbol change"""
        self.ui.current_symbol = event.new
        self.ui.chart_component.update_charts(self.ui.current_symbol)
        self.ui.data_display_component.update_price_display(self.ui.current_symbol)
    
    def start_trading(self, event):
        """Start trading session"""
        self.ui.is_running = True
        self.ui.control_component.set_trading_status(True)
        
        # Start integrated updates
        threading.Thread(target=self.run_integrated_updates, daemon=True).start()
        
        logger.info("🚀 Trading session started")
    
    def stop_trading(self, event):
        """Stop trading session"""
        self.ui.is_running = False
        self.ui.control_component.set_trading_status(False)
        
        logger.info("⏹ Trading session stopped")
    
    def optimize_portfolio(self, event):
        """Optimize portfolio using selected strategy"""
        try:
            strategy = self.ui.portfolio_component.components['optimization_strategy'].value
            risk_tolerance = self.ui.portfolio_component.components['risk_tolerance'].value
            
            logger.info(f"🔧 Optimizing portfolio with {strategy} strategy, {risk_tolerance} risk tolerance")
            
            # Simulate optimization
            self.ui.data_manager.portfolio_data['performance']['total_return'] += 0.01
            self.ui.portfolio_component.update_portfolio_display()
            
            # Add alert
            self.ui.alert_component.add_alert_message(f"Portfolio optimized using {strategy} strategy")
            
            logger.info(f"✅ Portfolio optimization completed")
            
        except Exception as e:
            logger.error(f"❌ Portfolio optimization failed: {e}")
    
    def generate_prediction(self, event):
        """Generate ML prediction"""
        try:
            model = self.ui.ml_component.get_selected_model()
            symbol = self.ui.current_symbol
            
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
            self.ui.alert_component.add_alert_message(f"{model} prediction for {symbol}: {prediction} (confidence: {confidence:.2f})")
            
            logger.info(f"✅ {model} prediction: {prediction} (confidence: {confidence:.2f})")
            
        except Exception as e:
            logger.error(f"❌ Prediction generation failed: {e}")
    
    def place_order(self, event):
        """Place trading order"""
        try:
            symbol = self.ui.portfolio_component.components['order_symbol'].value
            quantity = self.ui.portfolio_component.components['order_quantity'].value
            order_type = self.ui.portfolio_component.components['order_type'].value
            price = self.ui.portfolio_component.components['order_price'].value
            
            logger.info(f"📋 Placing {order_type} order: {quantity} shares of {symbol} at ${price}")
            
            # Simulate order placement
            order_id = f"ORD_{int(time.time())}"
            
            # Update portfolio
            if symbol not in self.ui.data_manager.portfolio_data['positions']:
                self.ui.data_manager.portfolio_data['positions'][symbol] = {
                    'shares': 0,
                    'avg_price': 0.0,
                    'current_price': price if price > 0 else 150.0
                }
            
            # Add to positions
            current_pos = self.ui.data_manager.portfolio_data['positions'][symbol]
            current_pos['shares'] += quantity
            current_pos['avg_price'] = (current_pos['avg_price'] * (current_pos['shares'] - quantity) + 
                                      price * quantity) / current_pos['shares']
            
            # Update portfolio display
            self.ui.portfolio_component.update_portfolio_display()
            
            # Add alert
            self.ui.alert_component.add_alert_message(f"Order placed: {quantity} shares of {symbol} at ${price}")
            
            logger.info(f"✅ Order {order_id} placed successfully")
            
        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}")
    
    def add_alert(self, event):
        """Add price alert"""
        try:
            high_price = self.ui.alert_component.components['alert_price_high'].value
            low_price = self.ui.alert_component.components['alert_price_low'].value
            
            if high_price > 0 or low_price > 0:
                alert_text = f"Alert set for {self.ui.current_symbol}: "
                if high_price > 0:
                    alert_text += f"High: ${high_price} "
                if low_price > 0:
                    alert_text += f"Low: ${low_price}"
                
                self.ui.alert_component.add_alert_message(alert_text)
                logger.info(f"🔔 {alert_text}")
            
        except Exception as e:
            logger.error(f"❌ Alert creation failed: {e}")
    
    def run_integrated_updates(self):
        """Run integrated updates with all TradePulse features"""
        while self.ui.is_running:
            try:
                # Update price data
                for symbol in self.ui.data_manager.symbols:
                    if symbol in self.ui.data_manager.price_data:
                        df = self.ui.data_manager.price_data[symbol]
                        last_price = df.iloc[-1]['Close']
                        new_price = last_price + np.random.normal(0, 1)
                        
                        # Update the last row
                        df.iloc[-1, df.columns.get_loc('Close')] = new_price
                        df.iloc[-1, df.columns.get_loc('High')] = max(df.iloc[-1]['High'], new_price)
                        df.iloc[-1, df.columns.get_loc('Low')] = min(df.iloc[-1]['Low'], new_price)
                        
                        # Update portfolio positions
                        if symbol in self.ui.data_manager.portfolio_data['positions']:
                            self.ui.data_manager.portfolio_data['positions'][symbol]['current_price'] = new_price
                
                # Update current symbol display
                if self.ui.current_symbol in self.ui.data_manager.price_data:
                    self.ui.data_display_component.update_price_display(self.ui.current_symbol)
                    self.ui.chart_component.update_charts(self.ui.current_symbol)
                
                # Update portfolio display
                self.ui.portfolio_component.update_portfolio_display()
                
                # Simulate ML predictions
                for symbol in self.ui.data_manager.symbols:
                    if symbol in self.ui.data_manager.ml_predictions:
                        for model in self.ui.data_manager.ml_predictions[symbol]:
                            self.ui.data_manager.ml_predictions[symbol][model] = np.random.normal(0, 1, len(self.ui.data_manager.ml_predictions[symbol][model]))
                
                time.sleep(self.ui.update_interval)
                
            except Exception as e:
                logger.error(f"❌ Error in integrated updates: {e}")
                time.sleep(self.ui.update_interval)
