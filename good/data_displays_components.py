#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Components
UI components for the data displays
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DataDisplaysComponents:
    """UI components for data displays"""
    
    def create_price_display(self):
        """Create price display component"""
        try:
            price_display = pn.pane.Markdown(
                "**Current Price:** $0.00",
                style={'font-size': '24px', 'font-weight': 'bold'}
            )
            
            return price_display
            
        except Exception as e:
            logger.error(f"Failed to create price display: {e}")
            return pn.pane.Markdown("**Price Display Error**")
    
    def create_change_display(self):
        """Create price change display component"""
        try:
            change_display = pn.pane.Markdown(
                "**Change:** $0.00 (0.00%)",
                style={'font-size': '18px'}
            )
            
            return change_display
            
        except Exception as e:
            logger.error(f"Failed to create change display: {e}")
            return pn.pane.Markdown("**Change Display Error**")
    
    def create_volume_display(self):
        """Create volume display component"""
        try:
            volume_display = pn.pane.Markdown(
                "**Volume:** 0",
                style={'font-size': '16px'}
            )
            
            return volume_display
            
        except Exception as e:
            logger.error(f"Failed to create volume display: {e}")
            return pn.pane.Markdown("**Volume Display Error**")
    
    def create_market_info_display(self):
        """Create market information display"""
        try:
            market_info = pn.Column(
                pn.pane.Markdown("**📊 Market Information**"),
                pn.pane.Markdown("**Market Cap:** $0.00"),
                pn.pane.Markdown("**24h High:** $0.00"),
                pn.pane.Markdown("**24h Low:** $0.00"),
                sizing_mode='stretch_width'
            )
            
            return market_info
            
        except Exception as e:
            logger.error(f"Failed to create market info display: {e}")
            return pn.pane.Markdown("**Market Info Error**")
    
    def create_summary_stats(self):
        """Create summary statistics display"""
        try:
            summary_stats = pn.Column(
                pn.pane.Markdown("**📈 Summary Statistics**"),
                pn.pane.Markdown("**Avg Volume:** 0"),
                pn.pane.Markdown("**52w High:** $0.00"),
                pn.pane.Markdown("**52w Low:** $0.00"),
                pn.pane.Markdown("**P/E Ratio:** 0.00"),
                sizing_mode='stretch_width'
            )
            
            return summary_stats
            
        except Exception as e:
            logger.error(f"Failed to create summary stats: {e}")
            return pn.pane.Markdown("**Summary Stats Error**")
    
    def create_data_displays_panel(self, display_core):
        """Create complete data displays panel"""
        return pn.Column(
            pn.pane.Markdown("### 💰 Market Data Displays"),
            display_core.get_data_displays_layout(),
            sizing_mode='stretch_width'
        )
    
    def update_price_display(self, price_display, price: float):
        """Update price display"""
        try:
            if price_display:
                price_display.object = f"**Current Price:** ${price:.2f}"
        except Exception as e:
            logger.error(f"Failed to update price display: {e}")
    
    def update_change_display(self, change_display, change: float, change_percent: float):
        """Update change display"""
        try:
            if change_display:
                change_color = "green" if change >= 0 else "red"
                change_symbol = "+" if change >= 0 else ""
                
                change_display.object = f"**Change:** {change_symbol}${change:.2f} ({change_symbol}{change_percent:.2f}%)"
                change_display.style = {
                    'font-size': '18px',
                    'color': change_color
                }
        except Exception as e:
            logger.error(f"Failed to update change display: {e}")
    
    def update_volume_display(self, volume_display, volume: int):
        """Update volume display"""
        try:
            if volume_display:
                # Format volume with appropriate units
                if volume >= 1_000_000_000:
                    formatted_volume = f"{volume / 1_000_000_000:.2f}B"
                elif volume >= 1_000_000:
                    formatted_volume = f"{volume / 1_000_000:.2f}M"
                elif volume >= 1_000:
                    formatted_volume = f"{volume / 1_000:.2f}K"
                else:
                    formatted_volume = str(volume)
                
                volume_display.object = f"**Volume:** {formatted_volume}"
        except Exception as e:
            logger.error(f"Failed to update volume display: {e}")
    
    def update_market_info_display(self, market_info_display, market_cap: float, high_24h: float, low_24h: float):
        """Update market info display"""
        try:
            if market_info_display and hasattr(market_info_display, 'objects') and len(market_info_display.objects) > 1:
                # Format market cap
                if market_cap >= 1_000_000_000_000:
                    formatted_market_cap = f"${market_cap / 1_000_000_000_000:.2f}T"
                elif market_cap >= 1_000_000_000:
                    formatted_market_cap = f"${market_cap / 1_000_000_000:.2f}B"
                elif market_cap >= 1_000_000:
                    formatted_market_cap = f"${market_cap / 1_000_000:.2f}M"
                else:
                    formatted_market_cap = f"${market_cap:.2f}"
                
                market_cap_display = market_info_display.objects[1]
                market_cap_display.object = f"**Market Cap:** {formatted_market_cap}"
                
                high_display = market_info_display.objects[2]
                high_display.object = f"**24h High:** ${high_24h:.2f}"
                
                low_display = market_info_display.objects[3]
                low_display.object = f"**24h Low:** ${low_24h:.2f}"
        except Exception as e:
            logger.error(f"Failed to update market info display: {e}")
    
    def update_summary_stats_display(self, summary_stats, avg_volume: int, high_52w: float, low_52w: float, pe_ratio: float):
        """Update summary stats display"""
        try:
            if summary_stats and hasattr(summary_stats, 'objects') and len(summary_stats.objects) > 1:
                # Format average volume
                if avg_volume >= 1_000_000_000:
                    formatted_avg_volume = f"{avg_volume / 1_000_000_000:.2f}B"
                elif avg_volume >= 1_000_000:
                    formatted_avg_volume = f"{avg_volume / 1_000_000:.2f}M"
                elif avg_volume >= 1_000:
                    formatted_avg_volume = f"{avg_volume / 1_000:.2f}K"
                else:
                    formatted_avg_volume = str(avg_volume)
                
                avg_volume_display = summary_stats.objects[1]
                avg_volume_display.object = f"**Avg Volume:** {formatted_avg_volume}"
                
                high_52w_display = summary_stats.objects[2]
                high_52w_display.object = f"**52w High:** ${high_52w:.2f}"
                
                low_52w_display = summary_stats.objects[3]
                low_52w_display.object = f"**52w Low:** ${low_52w:.2f}"
                
                pe_ratio_display = summary_stats.objects[4]
                pe_ratio_display.object = f"**P/E Ratio:** {pe_ratio:.2f}"
        except Exception as e:
            logger.error(f"Failed to update summary stats display: {e}")

