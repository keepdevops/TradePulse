#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Data Generator
Handles generation of demo data for showcase purposes
"""

import panel as pn
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from typing import Dict, List, Optional, Any
import logging

from .price_data_generator import PriceDataGenerator
from .portfolio_data_generator import PortfolioDataGenerator
from .trading_history_generator import TradingHistoryGenerator

logger = logging.getLogger(__name__)

class DemoDataGenerator:
    """Handles generation of demo data for showcase purposes"""
    
    def __init__(self):
        self.price_data_generator = PriceDataGenerator()
        self.portfolio_data_generator = PortfolioDataGenerator(self.price_data_generator)
        self.trading_history_generator = TradingHistoryGenerator(self.price_data_generator)
        
        # For backward compatibility
        self.symbols = self.price_data_generator.symbols
        self.current_symbol = "AAPL"
        self.price_data = self.price_data_generator.price_data
        self.portfolio_data = self.portfolio_data_generator.portfolio_data
        self.trading_history = self.trading_history_generator.trading_history
    
    def init_demo_data(self):
        """Initialize demo price data"""
        self.price_data_generator.init_demo_data()
        self.price_data = self.price_data_generator.price_data
    
    def init_portfolio_data(self):
        """Initialize demo portfolio data"""
        self.portfolio_data_generator.init_portfolio_data()
        self.portfolio_data = self.portfolio_data_generator.portfolio_data
    
    def init_trading_history(self):
        """Initialize demo trading history"""
        self.trading_history_generator.init_trading_history()
        self.trading_history = self.trading_history_generator.trading_history
    
    def get_price_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get price data for a specific symbol"""
        return self.price_data_generator.get_price_data(symbol)
    
    def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a specific symbol"""
        return self.price_data_generator.get_current_price(symbol)
    
    def get_price_change(self, symbol: str, days: int = 1) -> Optional[Dict[str, float]]:
        """Get price change for a specific symbol over specified days"""
        return self.price_data_generator.get_price_change(symbol, days)
    
    def get_volume_data(self, symbol: str) -> Optional[pd.Series]:
        """Get volume data for a specific symbol"""
        return self.price_data_generator.get_volume_data(symbol)
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get portfolio summary data"""
        return self.portfolio_data_generator.get_portfolio_summary()
    
    def get_trading_history_summary(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent trading history"""
        return self.trading_history_generator.get_trading_history_summary(limit)
    
    def update_portfolio_value(self):
        """Update portfolio values based on current prices"""
        self.portfolio_data_generator.update_portfolio_value()
        self.portfolio_data = self.portfolio_data_generator.portfolio_data
    
    def add_trade(self, trade_data: Dict[str, Any]):
        """Add a new trade to the trading history"""
        self.trading_history_generator.add_trade(trade_data)
        self.trading_history = self.trading_history_generator.trading_history
        
        # Update portfolio based on trade
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
        self.portfolio_data_generator.update_portfolio_from_trade(trade)
        self.portfolio_data = self.portfolio_data_generator.portfolio_data
    
    def get_demo_statistics(self) -> Dict[str, Any]:
        """Get comprehensive demo data statistics"""
        try:
            return {
                'symbols_count': len(self.symbols),
                'price_data_points': sum(len(df) for df in self.price_data.values()),
                'portfolio_positions': len(self.portfolio_data.get('positions', {})),
                'trading_history_count': len(self.trading_history),
                'total_portfolio_value': self.portfolio_data.get('total_value', 0),
                'available_cash': self.portfolio_data.get('cash', 0),
                'last_update': datetime.now()
            }
        except Exception as e:
            logger.error(f"Failed to get demo statistics: {e}")
            return {}
    
    def reset_demo_data(self):
        """Reset all demo data to initial state"""
        try:
            logger.info("🔄 Resetting demo data")
            
            # Reinitialize all data
            self.init_demo_data()
            self.init_portfolio_data()
            self.init_trading_history()
            
            logger.info("✅ Demo data reset completed")
            
        except Exception as e:
            logger.error(f"Failed to reset demo data: {e}")
    
    def export_demo_data(self) -> Dict[str, Any]:
        """Export demo data for external use"""
        try:
            price_export = self.price_data_generator.export_price_data()
            portfolio_export = self.portfolio_data_generator.export_portfolio_data()
            trading_export = self.trading_history_generator.export_trading_history()
            
            export_data = {
                'price_data': price_export.get('price_data', {}),
                'portfolio_data': portfolio_export.get('portfolio_data', {}),
                'trading_history': trading_export.get('trading_history', []),
                'export_timestamp': datetime.now().isoformat()
            }
            
            logger.info("📤 Demo data exported")
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export demo data: {e}")
            return {}
    
    def import_demo_data(self, demo_data: Dict[str, Any]):
        """Import demo data from external source"""
        try:
            if 'price_data' in demo_data:
                self.price_data_generator.import_price_data({'price_data': demo_data['price_data']})
                self.price_data = self.price_data_generator.price_data
            
            if 'portfolio_data' in demo_data:
                self.portfolio_data_generator.import_portfolio_data({'portfolio_data': demo_data['portfolio_data']})
                self.portfolio_data = self.portfolio_data_generator.portfolio_data
            
            if 'trading_history' in demo_data:
                self.trading_history_generator.import_trading_history({'trading_history': demo_data['trading_history']})
                self.trading_history = self.trading_history_generator.trading_history
            
            logger.info("📥 Demo data imported")
            
        except Exception as e:
            logger.error(f"Failed to import demo data: {e}")
