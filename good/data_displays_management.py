#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Management
UI management for the data displays
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DataDisplaysManagement:
    """UI management for data displays"""
    
    @staticmethod
    def get_data_displays_layout(display_core):
        """Get the complete data displays layout"""
        try:
            # Main price and change row
            price_change_row = pn.Row(
                display_core.price_display,
                pn.Spacer(width=30),
                display_core.change_display,
                pn.Spacer(width=30),
                display_core.volume_display,
                align='center',
                sizing_mode='stretch_width'
            )
            
            # Market info and summary stats row
            info_stats_row = pn.Row(
                display_core.market_info_display,
                pn.Spacer(width=30),
                display_core.summary_stats,
                align='start',
                sizing_mode='stretch_width'
            )
            
            # Complete data displays layout
            complete_layout = pn.Column(
                pn.pane.Markdown("### 💰 Market Data Displays"),
                price_change_row,
                pn.Divider(),
                info_stats_row,
                sizing_mode='stretch_width'
            )
            
            return complete_layout
            
        except Exception as e:
            logger.error(f"Failed to create data displays layout: {e}")
            return pn.pane.Markdown("**Data Displays Layout Error**")
    
    @staticmethod
    def create_price_display_layout(price: float, change: float, change_percent: float):
        """Create price display layout"""
        try:
            change_color = "green" if change >= 0 else "red"
            change_symbol = "+" if change >= 0 else ""
            
            layout = pn.Row(
                pn.pane.Markdown(f"**Current Price:** ${price:.2f}", 
                               style={'font-size': '24px', 'font-weight': 'bold'}),
                pn.Spacer(width=30),
                pn.pane.Markdown(f"**Change:** {change_symbol}${change:.2f} ({change_symbol}{change_percent:.2f}%)",
                               style={'font-size': '18px', 'color': change_color}),
                align='center',
                sizing_mode='stretch_width'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create price display layout: {e}")
            return pn.pane.Markdown("**Price Display Layout Error**")
    
    @staticmethod
    def create_market_info_layout(market_cap: float, high_24h: float, low_24h: float):
        """Create market info layout"""
        try:
            # Format market cap
            if market_cap >= 1_000_000_000_000:
                formatted_market_cap = f"${market_cap / 1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                formatted_market_cap = f"${market_cap / 1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                formatted_market_cap = f"${market_cap / 1_000_000:.2f}M"
            else:
                formatted_market_cap = f"${market_cap:.2f}"
            
            layout = pn.Column(
                pn.pane.Markdown("**📊 Market Information**"),
                pn.pane.Markdown(f"**Market Cap:** {formatted_market_cap}"),
                pn.pane.Markdown(f"**24h High:** ${high_24h:.2f}"),
                pn.pane.Markdown(f"**24h Low:** ${low_24h:.2f}"),
                sizing_mode='stretch_width'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create market info layout: {e}")
            return pn.pane.Markdown("**Market Info Layout Error**")
    
    @staticmethod
    def create_summary_stats_layout(avg_volume: int, high_52w: float, low_52w: float, pe_ratio: float):
        """Create summary stats layout"""
        try:
            # Format average volume
            if avg_volume >= 1_000_000_000:
                formatted_avg_volume = f"{avg_volume / 1_000_000_000:.2f}B"
            elif avg_volume >= 1_000_000:
                formatted_avg_volume = f"{avg_volume / 1_000_000:.2f}M"
            elif avg_volume >= 1_000:
                formatted_avg_volume = f"{avg_volume / 1_000:.2f}K"
            else:
                formatted_avg_volume = str(avg_volume)
            
            layout = pn.Column(
                pn.pane.Markdown("**📈 Summary Statistics**"),
                pn.pane.Markdown(f"**Avg Volume:** {formatted_avg_volume}"),
                pn.pane.Markdown(f"**52w High:** ${high_52w:.2f}"),
                pn.pane.Markdown(f"**52w Low:** ${low_52w:.2f}"),
                pn.pane.Markdown(f"**P/E Ratio:** {pe_ratio:.2f}"),
                sizing_mode='stretch_width'
            )
            
            return layout
            
        except Exception as e:
            logger.error(f"Failed to create summary stats layout: {e}")
            return pn.pane.Markdown("**Summary Stats Layout Error**")
    
    @staticmethod
    def create_error_display(error_message: str):
        """Create error display"""
        return pn.pane.Markdown(f"""
        ### ❌ Error
        **Message**: {error_message}
        """)
    
    @staticmethod
    def create_success_display(success_message: str):
        """Create success display"""
        return pn.pane.Markdown(f"""
        ### ✅ Success
        **Message**: {success_message}
        """)
    
    @staticmethod
    def create_loading_display():
        """Create loading display"""
        return pn.pane.Markdown("""
        ### ⏳ Loading Market Data...
        Please wait while we fetch the latest market information.
        """)
    
    @staticmethod
    def create_data_summary_display(data: dict):
        """Create data summary display"""
        from .data_displays_advanced_management import DataDisplaysAdvancedManagement
        return DataDisplaysAdvancedManagement.create_data_summary_display(data)
    
    @staticmethod
    def create_market_status_display(status: str, details: dict):
        """Create market status display"""
        from .data_displays_advanced_management import DataDisplaysAdvancedManagement
        return DataDisplaysAdvancedManagement.create_market_status_display(status, details)
