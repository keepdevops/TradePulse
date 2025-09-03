#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Operations
Data-related operations for the data displays
"""

import panel as pn
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class DataDisplaysOperations:
    """Data-related operations for data displays"""
    
    def update_price_data(self, display_core, price: float, change: float, change_percent: float):
        """Update price and change data"""
        try:
            display_core.current_price = price
            display_core.price_change = change
            display_core.price_change_percent = change_percent
            
            # Update price display
            display_core.components.update_price_display(display_core.price_display, price)
            
            # Update change display with color coding
            display_core.components.update_change_display(display_core.change_display, change, change_percent)
            
            logger.info(f"✅ Price data updated: ${price:.2f} ({change_percent:+.2f}%)")
            
        except Exception as e:
            logger.error(f"Failed to update price data: {e}")
    
    def update_volume_data(self, display_core, volume: int):
        """Update volume data"""
        try:
            display_core.volume = volume
            
            # Update volume display
            display_core.components.update_volume_display(display_core.volume_display, volume)
            
            logger.info(f"✅ Volume data updated: {volume}")
            
        except Exception as e:
            logger.error(f"Failed to update volume data: {e}")
    
    def update_market_data(self, display_core, market_cap: float, high_24h: float, low_24h: float):
        """Update market data"""
        try:
            display_core.market_cap = market_cap
            display_core.high_24h = high_24h
            display_core.low_24h = low_24h
            
            # Update market info display
            display_core.components.update_market_info_display(
                display_core.market_info_display, market_cap, high_24h, low_24h
            )
            
            logger.info(f"✅ Market data updated: Cap=${market_cap:.2f}, High=${high_24h:.2f}, Low=${low_24h:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to update market data: {e}")
    
    def update_summary_statistics(self, display_core, avg_volume: int, high_52w: float, low_52w: float, pe_ratio: float):
        """Update summary statistics"""
        try:
            # Update summary stats display
            display_core.components.update_summary_stats_display(
                display_core.summary_stats, avg_volume, high_52w, low_52w, pe_ratio
            )
            
            logger.info(f"✅ Summary statistics updated: Avg Vol={avg_volume}, 52w High=${high_52w:.2f}, 52w Low=${low_52w:.2f}, P/E={pe_ratio:.2f}")
            
        except Exception as e:
            logger.error(f"Failed to update summary statistics: {e}")
    
    def get_current_data(self, display_core) -> Dict[str, Any]:
        """Get current display data"""
        try:
            return {
                'current_price': display_core.current_price,
                'price_change': display_core.price_change,
                'price_change_percent': display_core.price_change_percent,
                'volume': display_core.volume,
                'market_cap': display_core.market_cap,
                'high_24h': display_core.high_24h,
                'low_24h': display_core.low_24h
            }
        except Exception as e:
            logger.error(f"Failed to get current data: {e}")
            return {}
    
    def get_display_statistics(self, display_core) -> Dict[str, Any]:
        """Get display component statistics"""
        try:
            return {
                'price_updated': display_core.current_price > 0,
                'change_updated': display_core.price_change != 0,
                'volume_updated': display_core.volume > 0,
                'market_data_updated': display_core.market_cap > 0,
                'current_price': display_core.current_price,
                'price_change_percent': display_core.price_change_percent,
                'volume_formatted': display_core.formatters.format_volume(display_core.volume)
            }
        except Exception as e:
            logger.error(f"Failed to get display statistics: {e}")
            return {}
    
    def clear_displays(self, display_core):
        """Clear all display data"""
        try:
            self.update_price_data(display_core, 0.0, 0.0, 0.0)
            self.update_volume_data(display_core, 0)
            self.update_market_data(display_core, 0.0, 0.0, 0.0)
            self.update_summary_statistics(display_core, 0, 0.0, 0.0, 0.0)
            
            logger.info("✅ All displays cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear displays: {e}")
    
    def validate_price_data(self, price: float, change: float, change_percent: float) -> bool:
        """Validate price data"""
        try:
            if price < 0:
                return False
            
            if abs(change_percent) > 1000:  # Unreasonable change percentage
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate price data: {e}")
            return False
    
    def validate_volume_data(self, volume: int) -> bool:
        """Validate volume data"""
        try:
            if volume < 0:
                return False
            
            if volume > 1_000_000_000_000:  # Unreasonable volume
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate volume data: {e}")
            return False
    
    def validate_market_data(self, market_cap: float, high_24h: float, low_24h: float) -> bool:
        """Validate market data"""
        try:
            if market_cap < 0:
                return False
            
            if high_24h < low_24h:
                return False
            
            if high_24h < 0 or low_24h < 0:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate market data: {e}")
            return False
    
    def export_display_data(self, display_core, filename: str = None) -> str:
        """Export display data to JSON"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"display_data_export_{timestamp}.json"
            
            # Get current data
            current_data = self.get_current_data(display_core)
            display_stats = self.get_display_statistics(display_core)
            
            export_data = {
                'timestamp': datetime.now().isoformat(),
                'current_data': current_data,
                'display_statistics': display_stats
            }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"📤 Display data exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export display data: {e}")
            return None



