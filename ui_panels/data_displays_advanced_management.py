#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Advanced Management
Advanced UI management for the data displays
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class DataDisplaysAdvancedManagement:
    """Advanced UI management for data displays"""
    
    @staticmethod
    def create_data_summary_display(data: dict):
        """Create data summary display"""
        try:
            if not data:
                return pn.pane.Markdown("""
                ### 📊 Data Summary
                No data available
                """)
            
            summary_text = f"""
            ### 📊 Data Summary
            
            **Current Price**: ${data.get('current_price', 0):.2f}  
            **Price Change**: {data.get('price_change', 0):+.2f} ({data.get('price_change_percent', 0):+.2f}%)  
            **Volume**: {data.get('volume', 0):,}  
            **Market Cap**: ${data.get('market_cap', 0):,.2f}  
            **24h Range**: ${data.get('low_24h', 0):.2f} - ${data.get('high_24h', 0):.2f}
            """
            
            return pn.pane.Markdown(summary_text)
            
        except Exception as e:
            logger.error(f"Failed to create data summary display: {e}")
            return pn.pane.Markdown("Error: Failed to create data summary display")
    
    @staticmethod
    def create_market_status_display(status: str, details: dict):
        """Create market status display"""
        try:
            status_emoji = {
                'open': '🟢',
                'closed': '🔴',
                'pre_market': '🟡',
                'after_hours': '🟠',
                'unknown': '⚪'
            }.get(status.lower(), '⚪')
            
            status_text = f"""
            ### {status_emoji} Market Status: {status.title()}
            
            **Last Updated**: {details.get('last_updated', 'Unknown')}  
            **Data Source**: {details.get('data_source', 'Unknown')}  
            **Refresh Rate**: {details.get('refresh_rate', 'Unknown')}  
            **Data Quality**: {details.get('data_quality', 'Unknown')}
            """
            
            return pn.pane.Markdown(status_text)
            
        except Exception as e:
            logger.error(f"Failed to create market status display: {e}")
            return pn.pane.Markdown("Error: Failed to create market status display")



