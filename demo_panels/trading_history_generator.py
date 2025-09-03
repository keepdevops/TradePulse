#!/usr/bin/env python3
"""
TradePulse Demo Panels - Trading History Generator
Handles generation of demo trading history
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TradingHistoryGenerator:
    """Handles generation of demo trading history"""
    
    def __init__(self, price_data_generator):
        self.price_data_generator = price_data_generator
        self.trading_history = []
        self.init_trading_history()
    
    def init_trading_history(self):
        """Initialize demo trading history"""
        try:
            logger.info("🔧 Initializing demo trading history")
            
            # Generate sample trading history
            history_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
            
            for i, date in enumerate(history_dates):
                if np.random.random() < 0.3:  # 30% chance of trade per day
                    symbol = np.random.choice(self.price_data_generator.symbols)
                    action = np.random.choice(['BUY', 'SELL'])
                    quantity = np.random.randint(50, 500)
                    price = self.price_data_generator.price_data[symbol]['Close'].iloc[i] if i < len(self.price_data_generator.price_data[symbol]) else 100
                    
                    trade = {
                        'date': date,
                        'symbol': symbol,
                        'action': action,
                        'quantity': quantity,
                        'price': price,
                        'value': quantity * price,
                        'commission': quantity * price * 0.001,  # 0.1% commission
                        'status': 'COMPLETED'
                    }
                    
                    self.trading_history.append(trade)
            
            logger.info(f"✅ Demo trading history initialized with {len(self.trading_history)} trades")
            
        except Exception as e:
            logger.error(f"Failed to initialize demo trading history: {e}")
    
    def get_trading_history_summary(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trading history"""
        try:
            return self.trading_history[-limit:] if self.trading_history else []
        except Exception as e:
            logger.error(f"Failed to get trading history summary: {e}")
            return []
    
    def add_trade(self, trade_data: Dict[str, Any]):
        """Add a new trade to the trading history"""
        try:
            trade = {
                'date': datetime.now(),
                'symbol': trade_data.get('symbol', 'UNKNOWN'),
                'action': trade_data.get('action', 'BUY'),
                'quantity': trade_data.get('quantity', 0),
                'price': trade_data.get('price', 0.0),
                'value': trade_data.get('quantity', 0) * trade_data.get('price', 0.0),
                'commission': trade_data.get('quantity', 0) * trade_data.get('price', 0.0) * 0.001,
                'status': 'COMPLETED'
            }
            
            self.trading_history.append(trade)
            
            logger.info(f"✅ Trade added: {trade['action']} {trade['quantity']} {trade['symbol']} @ {trade['price']}")
            
        except Exception as e:
            logger.error(f"Failed to add trade: {e}")
    
    def reset_trading_history(self):
        """Reset trading history to initial state"""
        try:
            logger.info("🔄 Resetting trading history")
            self.init_trading_history()
            logger.info("✅ Trading history reset completed")
        except Exception as e:
            logger.error(f"Failed to reset trading history: {e}")
    
    def export_trading_history(self) -> Dict[str, Any]:
        """Export trading history for external use"""
        try:
            export_data = {
                'trading_history': self.trading_history.copy(),
                'export_timestamp': datetime.now().isoformat()
            }
            logger.info("📤 Trading history exported")
            return export_data
        except Exception as e:
            logger.error(f"Failed to export trading history: {e}")
            return {}
    
    def import_trading_history(self, trading_history: Dict[str, Any]):
        """Import trading history from external source"""
        try:
            if 'trading_history' in trading_history:
                self.trading_history = trading_history['trading_history']
            logger.info("📥 Trading history imported")
        except Exception as e:
            logger.error(f"Failed to import trading history: {e}")
