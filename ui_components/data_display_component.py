#!/usr/bin/env python3
"""
TradePulse UI Data Display Component
Component for displaying data
"""

import panel as pn
from .base_component import BaseComponent
from .data_manager import DataManager

class DataDisplayComponent(BaseComponent):
    """Component for displaying data"""
    
    def __init__(self, data_manager: DataManager):
        super().__init__("DataDisplayComponent")
        self.data_manager = data_manager
        self.create_components()
    
    def create_components(self):
        """Create data display components"""
        self.components['price_display'] = pn.pane.Markdown("**Current Price:** $0.00")
        self.components['change_display'] = pn.pane.Markdown("**Change:** +0.00%")
        self.components['volume_display'] = pn.pane.Markdown("**Volume:** 0")
        self.components['market_cap_display'] = pn.pane.Markdown("**Market Cap:** $0.00B")
    
    def get_layout(self):
        """Get the data display layout"""
        return pn.Row(
            self.components['price_display'],
            self.components['change_display'],
            self.components['volume_display'],
            self.components['market_cap_display'],
            align='center'
        )
    
    def update_price_display(self, symbol: str):
        """Update price display for a symbol"""
        df = self.data_manager.get_price_data(symbol)
        if not df.empty:
            current_price = df['Close'].iloc[-1]
            prev_price = df['Close'].iloc[-2] if len(df) > 1 else current_price
            change = current_price - prev_price
            change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
            
            self.components['price_display'].object = f"**Current Price:** ${current_price:.2f}"
            self.components['change_display'].object = f"**Change:** {change:+.2f} ({change_pct:+.2f}%)"
            self.components['volume_display'].object = f"**Volume:** {df['Volume'].iloc[-1]:,}"
            
            # Mock market cap calculation
            market_cap = current_price * 1000000000  # Assuming 1B shares
            self.components['market_cap_display'].object = f"**Market Cap:** ${market_cap/1e9:.2f}B"
