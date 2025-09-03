#!/usr/bin/env python3
"""
TradePulse UI Panels - Chart Manager
Handles chart creation, management, and visualization
"""

import panel as pn
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Optional, Any
import logging

from .chart_creator import ChartCreator
from .chart_operations import ChartOperations

logger = logging.getLogger(__name__)

class ChartManager:
    """Handles chart creation, management, and visualization"""
    
    def __init__(self):
        self.charts = {}
        self.chart_types = ['candlestick', 'line', 'bar', 'area', 'scatter']
        self.current_chart_type = 'candlestick'
        self.chart_history = []
        
        # Initialize chart creator
        self.chart_creator = ChartCreator()
        
        # Initialize chart operations
        self.chart_operations = ChartOperations(self)
        
        # Create chart components
        self.chart_type_selector = self._create_chart_type_selector()
        self.chart_container = self._create_chart_container()
        self.chart_controls = self._create_chart_controls()
    
    def _create_chart_type_selector(self):
        """Create chart type selection component"""
        try:
            chart_type_selector = pn.widgets.Select(
                name='Chart Type',
                options=self.chart_types,
                value=self.current_chart_type,
                width=150
            )
            
            # Setup callback
            chart_type_selector.param.watch(self._on_chart_type_change, 'value')
            
            return chart_type_selector
            
        except Exception as e:
            logger.error(f"Failed to create chart type selector: {e}")
            return pn.pane.Markdown("**Chart Type Selector Error**")
    
    def _create_chart_container(self):
        """Create chart container component"""
        try:
            chart_container = pn.pane.Plotly(
                self._create_empty_chart(),
                sizing_mode='stretch_width',
                height=400
            )
            
            return chart_container
            
        except Exception as e:
            logger.error(f"Failed to create chart container: {e}")
            return pn.pane.Markdown("**Chart Container Error**")
    
    def _create_chart_controls(self):
        """Create chart control buttons"""
        try:
            refresh_button = pn.widgets.Button(
                name='🔄 Refresh',
                button_type='primary',
                width=100
            )
            refresh_button.on_click(self.refresh_chart)
            
            export_button = pn.widgets.Button(
                name='📤 Export',
                button_type='success',
                width=100
            )
            export_button.on_click(self.export_chart)
            
            fullscreen_button = pn.widgets.Button(
                name='⛶ Fullscreen',
                button_type='light',
                width=100
            )
            fullscreen_button.on_click(self.toggle_fullscreen)
            
            controls_row = pn.Row(
                refresh_button,
                export_button,
                fullscreen_button,
                align='center'
            )
            
            return controls_row
            
        except Exception as e:
            logger.error(f"Failed to create chart controls: {e}")
            return pn.pane.Markdown("**Chart Controls Error**")
    
    def _create_empty_chart(self):
        """Create an empty placeholder chart"""
        return self.chart_creator.create_empty_chart()
    
    def _on_chart_type_change(self, event):
        """Handle chart type selection change"""
        try:
            new_chart_type = event.new
            old_chart_type = event.old
            
            logger.info(f"🔄 Chart type changed: {old_chart_type} → {new_chart_type}")
            
            self.current_chart_type = new_chart_type
            
            # Update current chart if data exists
            if self.charts:
                self._update_chart_display()
            
        except Exception as e:
            logger.error(f"Failed to handle chart type change: {e}")
    
    def create_candlestick_chart(self, data: pd.DataFrame, symbol: str = "Unknown") -> go.Figure:
        """Create a candlestick chart from OHLC data"""
        return self.chart_creator.create_candlestick_chart(data, symbol)
    
    def create_line_chart(self, data: pd.DataFrame, symbol: str = "Unknown", column: str = "close") -> go.Figure:
        """Create a line chart from data"""
        return self.chart_creator.create_line_chart(data, symbol, column)
    
    def create_bar_chart(self, data: pd.DataFrame, symbol: str = "Unknown", column: str = "volume") -> go.Figure:
        """Create a bar chart from data"""
        return self.chart_creator.create_bar_chart(data, symbol, column)
    
    def update_chart(self, data: pd.DataFrame, symbol: str = "Unknown"):
        """Update chart with new data"""
        self.chart_operations.update_chart(data, symbol)
    
    def _update_chart_display(self):
        """Update chart display with current data and type"""
        try:
            if not self.charts:
                return
            
            # Get first available symbol
            symbol = list(self.charts.keys())[0]
            data = self.charts[symbol]
            
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
            if not self.charts:
                logger.warning("⚠️ No chart data to export")
                return
            
            # Get current chart data
            symbol = list(self.charts.keys())[0]
            data = self.charts[symbol]
            
            # Create export filename
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{symbol}_{self.current_chart_type}_{timestamp}.csv"
            
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
            
            self.chart_history.append(update_record)
            
        except Exception as e:
            logger.error(f"Failed to record chart update: {e}")
    
    def get_chart_layout(self):
        """Get the complete chart layout"""
        try:
            # Chart controls row
            controls_row = pn.Row(
                pn.pane.Markdown("### 📊 Chart Management"),
                pn.Spacer(width=20),
                self.chart_type_selector,
                pn.Spacer(width=20),
                self.chart_controls,
                align='center',
                sizing_mode='stretch_width'
            )
            
            # Chart container
            chart_section = pn.Column(
                controls_row,
                self.chart_container,
                sizing_mode='stretch_width'
            )
            
            return chart_section
            
        except Exception as e:
            logger.error(f"Failed to create chart layout: {e}")
            return pn.pane.Markdown("**Chart Layout Error**")
    
    def get_chart_statistics(self) -> Dict[str, Any]:
        """Get chart manager statistics"""
        try:
            return {
                'current_chart_type': self.current_chart_type,
                'available_chart_types': len(self.chart_types),
                'charts_created': len(self.charts),
                'chart_updates': len(self.chart_history),
                'last_update': self.chart_history[-1]['timestamp'] if self.chart_history else None
            }
        except Exception as e:
            logger.error(f"Failed to get chart statistics: {e}")
            return {}
    
    def clear_charts(self):
        """Clear all charts and data"""
        try:
            self.charts.clear()
            self.chart_history.clear()
            self.chart_container.object = self._create_empty_chart()
            
            logger.info("🗑️ All charts cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear charts: {e}")
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'chart_type_selector': self.chart_type_selector,
            'chart_container': self.chart_container,
            'chart_controls': self.chart_controls
        }
