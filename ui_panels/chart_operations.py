#!/usr/bin/env python3
"""
TradePulse UI Panels - Chart Operations
Handles chart operations and management
"""

import pandas as pd
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class ChartOperations:
    """Handles chart operations and management"""
    
    def __init__(self, chart_manager):
        self.chart_manager = chart_manager
    
    def update_chart(self, data: pd.DataFrame, symbol: str = "Unknown"):
        """Update chart with new data"""
        try:
            if data.empty:
                logger.warning("⚠️ No data provided for chart update")
                return
            
            # Store data
            self.chart_manager.charts[symbol] = data
            
            # Create chart based on current type
            if self.chart_manager.current_chart_type == 'candlestick':
                fig = self.chart_manager.create_candlestick_chart(data, symbol)
            elif self.chart_manager.current_chart_type == 'line':
                fig = self.chart_manager.create_line_chart(data, symbol)
            elif self.chart_manager.current_chart_type == 'bar':
                fig = self.chart_manager.create_bar_chart(data, symbol)
            elif self.chart_manager.current_chart_type == 'area':
                fig = self.chart_manager.create_line_chart(data, symbol)  # Area chart as line for now
            elif self.chart_manager.current_chart_type == 'scatter':
                fig = self.chart_manager.create_line_chart(data, symbol)  # Scatter chart as line for now
            else:
                fig = self.chart_manager.create_line_chart(data, symbol)
            
            # Update chart container
            self.chart_manager.chart_container.object = fig
            
            # Record chart update
            self._record_chart_update(symbol, self.chart_manager.current_chart_type, len(data))
            
            logger.info(f"✅ Chart updated for {symbol} with {len(data)} data points")
            
        except Exception as e:
            logger.error(f"Failed to update chart: {e}")
    
    def _update_chart_display(self):
        """Update chart display with current data and type"""
        try:
            if not self.chart_manager.charts:
                return
            
            # Get first available symbol
            symbol = list(self.chart_manager.charts.keys())[0]
            data = self.chart_manager.charts[symbol]
            
            # Update chart
            self.update_chart(data, symbol)
            
        except Exception as e:
            logger.error(f"Failed to update chart display: {e}")
    
    def refresh_chart(self, event):
        """Refresh the current chart"""
        try:
            logger.info("🔄 Refreshing chart...")
            self._update_chart_display()
            
        except Exception as e:
            logger.error(f"Failed to refresh chart: {e}")
    
    def export_chart(self, event):
        """Export the current chart"""
        try:
            if not self.chart_manager.charts:
                logger.warning("⚠️ No chart data to export")
                return
            
            # Get current chart data
            symbol = list(self.chart_manager.charts.keys())[0]
            data = self.chart_manager.charts[symbol]
            
            # Create export filename
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{symbol}_{self.chart_manager.current_chart_type}_{timestamp}.csv"
            
            # Export data
            data.to_csv(filename)
            
            logger.info(f"📤 Chart exported to {filename}")
            
        except Exception as e:
            logger.error(f"Failed to export chart: {e}")
    
    def toggle_fullscreen(self, event):
        """Toggle chart fullscreen mode"""
        try:
            logger.info("⛶ Toggling chart fullscreen...")
            # This would typically involve JavaScript interaction
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"Failed to toggle fullscreen: {e}")
    
    def _record_chart_update(self, symbol: str, chart_type: str, data_points: int):
        """Record chart update operation"""
        try:
            update_record = {
                'timestamp': pd.Timestamp.now(),
                'symbol': symbol,
                'chart_type': chart_type,
                'data_points': data_points
            }
            
            self.chart_manager.chart_history.append(update_record)
            
        except Exception as e:
            logger.error(f"Failed to record chart update: {e}")
    
    def clear_charts(self):
        """Clear all charts and data"""
        try:
            self.chart_manager.charts.clear()
            self.chart_manager.chart_history.clear()
            self.chart_manager.chart_container.object = self.chart_manager._create_empty_chart()
            
            logger.info("🗑️ All charts cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear charts: {e}")
    
    def get_chart_statistics(self) -> Dict[str, Any]:
        """Get chart manager statistics"""
        try:
            return {
                'current_chart_type': self.chart_manager.current_chart_type,
                'available_chart_types': len(self.chart_manager.chart_types),
                'charts_created': len(self.chart_manager.charts),
                'chart_updates': len(self.chart_manager.chart_history),
                'last_update': self.chart_manager.chart_history[-1]['timestamp'] if self.chart_manager.chart_history else None
            }
        except Exception as e:
            logger.error(f"Failed to get chart statistics: {e}")
            return {}
