#!/usr/bin/env python3
"""
TradePulse Demo Panels - Display Components
Handles demo display component creation and management
"""

import panel as pn
import pandas as pd
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class DisplayComponents:
    """Handles demo display component creation and management"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.components = {}
        
        # Initialize display components
        self.create_display_components()
    
    def create_display_components(self):
        """Create all display components"""
        try:
            logger.info("🔧 Creating display components")
            
            # Price display
            self.components['price_display'] = pn.pane.Markdown(
                '**Current Price:** $0.00',
                style={'font-size': '18px', 'color': 'white'}
            )
            
            # Change display
            self.components['change_display'] = pn.pane.Markdown(
                '**Change:** $0.00 (0.00%)',
                style={'font-size': '16px', 'color': 'white'}
            )
            
            # Volume display
            self.components['volume_display'] = pn.pane.Markdown(
                '**Volume:** 0',
                style={'font-size': '16px', 'color': 'white'}
            )
            
            # Market cap display
            self.components['market_cap_display'] = pn.pane.Markdown(
                '**Market Cap:** $0.00',
                style={'font-size': '16px', 'color': 'white'}
            )
            
            # P/E ratio display
            self.components['pe_ratio_display'] = pn.pane.Markdown(
                '**P/E Ratio:** 0.00',
                style={'font-size': '16px', 'color': 'white'}
            )
            
            # 52-week range display
            self.components['week_range_display'] = pn.pane.Markdown(
                '**52-Week Range:** $0.00 - $0.00',
                style={'font-size': '16px', 'color': 'white'}
            )
            
            logger.info("✅ Display components created")
            
        except Exception as e:
            logger.error(f"Failed to create display components: {e}")
    
    def get_components(self) -> Dict[str, Any]:
        """Get all display components"""
        return self.components.copy()
    
    def update_price_display(self, price: float, change: float, change_pct: float):
        """Update price display components"""
        try:
            # Update price
            if 'price_display' in self.components:
                self.components['price_display'].object = f'**Current Price:** ${price:.2f}'
            
            # Update change
            if 'change_display' in self.components:
                change_sign = '+' if change >= 0 else ''
                change_color = 'green' if change >= 0 else 'red'
                self.components['change_display'].object = (
                    f'**Change:** {change_sign}${change:.2f} ({change_sign}{change_pct:.2f}%)'
                )
                self.components['change_display'].style = {
                    'font-size': '16px', 
                    'color': change_color
                }
            
        except Exception as e:
            logger.error(f"Failed to update price display: {e}")
    
    def update_volume_display(self, volume: int):
        """Update volume display"""
        try:
            if 'volume_display' in self.components:
                self.components['volume_display'].object = f'**Volume:** {volume:,}'
            
        except Exception as e:
            logger.error(f"Failed to update volume display: {e}")
    
    def update_market_data_display(self, market_cap: float, pe_ratio: float, 
                                  week_high: float, week_low: float):
        """Update market data displays"""
        try:
            # Update market cap
            if 'market_cap_display' in self.components:
                if market_cap >= 1e12:
                    market_cap_text = f'**Market Cap:** ${market_cap/1e12:.2f}T'
                elif market_cap >= 1e9:
                    market_cap_text = f'**Market Cap:** ${market_cap/1e9:.2f}B'
                elif market_cap >= 1e6:
                    market_cap_text = f'**Market Cap:** ${market_cap/1e6:.2f}M'
                else:
                    market_cap_text = f'**Market Cap:** ${market_cap:,.2f}'
                
                self.components['market_cap_display'].object = market_cap_text
            
            # Update P/E ratio
            if 'pe_ratio_display' in self.components:
                self.components['pe_ratio_display'].object = f'**P/E Ratio:** {pe_ratio:.2f}'
            
            # Update 52-week range
            if 'week_range_display' in self.components:
                self.components['week_range_display'].object = (
                    f'**52-Week Range:** ${week_low:.2f} - ${week_high:.2f}'
                )
            
        except Exception as e:
            logger.error(f"Failed to update market data display: {e}")
    
    def get_display_layout(self) -> pn.Column:
        """Get the display components layout"""
        try:
            # Create price section
            price_section = pn.Column(
                pn.pane.Markdown("### 💰 Price Information"),
                self.components.get('price_display', pn.pane.Markdown("No price")),
                self.components.get('change_display', pn.pane.Markdown("No change")),
                sizing_mode='stretch_width'
            )
            
            # Create market data section
            market_data_section = pn.Column(
                pn.pane.Markdown("### 📊 Market Data"),
                pn.Row(
                    self.components.get('volume_display', pn.pane.Markdown("No volume")),
                    self.components.get('market_cap_display', pn.pane.Markdown("No market cap")),
                    align='center'
                ),
                pn.Row(
                    self.components.get('pe_ratio_display', pn.pane.Markdown("No P/E")),
                    self.components.get('week_range_display', pn.pane.Markdown("No range")),
                    align='center'
                ),
                sizing_mode='stretch_width'
            )
            
            # Create complete layout
            layout = pn.Column(
                price_section,
                pn.Spacer(height=20),
                market_data_section,
                sizing_mode='stretch_width',
                background='#3d3d3d',
                margin=(10, 0)
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create display layout: {e}")
            return pn.Column("Error: Failed to create display layout")
    
    def reset_displays(self):
        """Reset all displays to default values"""
        try:
            self.update_price_display(0.0, 0.0, 0.0)
            self.update_volume_display(0)
            self.update_market_data_display(0.0, 0.0, 0.0, 0.0)
            
            logger.info("✅ Display components reset")
            
        except Exception as e:
            logger.error(f"Failed to reset displays: {e}")
