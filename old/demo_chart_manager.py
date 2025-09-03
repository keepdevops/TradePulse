#!/usr/bin/env python3
"""
TradePulse Demo Panels - Demo Chart Manager
Handles demo chart creation and management
"""

import panel as pn
import pandas as pd
from typing import Dict, Any, Optional
import logging

from .chart_factory import ChartFactory

logger = logging.getLogger(__name__)

class DemoChartManager:
    """Handles demo chart creation and management"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.charts = {}
        
        # Initialize chart factory
        self.chart_factory = ChartFactory(data_generator)
        
        # Create all charts
        self.create_charts()
    
    def create_charts(self):
        """Create all demo charts"""
        try:
            logger.info("🔧 Creating demo charts")
            
            # Create charts using factory
            self.charts['candlestick'] = self.chart_factory.create_candlestick_chart()
            self.charts['volume'] = self.chart_factory.create_volume_chart()
            self.charts['line'] = self.chart_factory.create_line_chart()
            self.charts['bar'] = self.chart_factory.create_bar_chart()
            self.charts['portfolio_performance'] = self.chart_factory.create_portfolio_performance_chart()
            self.charts['trading_activity'] = self.chart_factory.create_trading_activity_chart()
            
            logger.info(f"✅ {len(self.charts)} demo charts created")
            
        except Exception as e:
            logger.error(f"Failed to create demo charts: {e}")
    
    def get_chart(self, chart_name: str) -> Optional[Any]:
        """Get a specific chart"""
        try:
            return self.charts.get(chart_name)
            
        except Exception as e:
            logger.error(f"Failed to get chart {chart_name}: {e}")
            return None
    
    def get_all_charts(self) -> Dict[str, Any]:
        """Get all charts"""
        try:
            return self.charts.copy()
            
        except Exception as e:
            logger.error(f"Failed to get all charts: {e}")
            return {}
    
    def refresh_chart(self, chart_name: str) -> bool:
        """Refresh a specific chart"""
        try:
            if chart_name in self.charts:
                # Recreate the chart
                if chart_name == 'candlestick':
                    self.charts[chart_name] = self.chart_factory.create_candlestick_chart()
                elif chart_name == 'volume':
                    self.charts[chart_name] = self.chart_factory.create_volume_chart()
                elif chart_name == 'line':
                    self.charts[chart_name] = self.chart_factory.create_line_chart()
                elif chart_name == 'bar':
                    self.charts[chart_name] = self.chart_factory.create_bar_chart()
                elif chart_name == 'portfolio_performance':
                    self.charts[chart_name] = self.chart_factory.create_portfolio_performance_chart()
                elif chart_name == 'trading_activity':
                    self.charts[chart_name] = self.chart_factory.create_trading_activity_chart()
                
                logger.info(f"✅ Chart {chart_name} refreshed")
                return True
            else:
                logger.warning(f"⚠️ Chart {chart_name} not found")
                return False
                
        except Exception as e:
            logger.error(f"Failed to refresh chart {chart_name}: {e}")
            return False
    
    def refresh_all_charts(self):
        """Refresh all charts"""
        try:
            logger.info("🔄 Refreshing all charts")
            
            for chart_name in self.charts.keys():
                self.refresh_chart(chart_name)
            
            logger.info("✅ All charts refreshed")
            
        except Exception as e:
            logger.error(f"Failed to refresh all charts: {e}")
    
    def get_chart_configs(self) -> Dict[str, Any]:
        """Get chart configurations"""
        try:
            return self.chart_factory.get_chart_configs()
            
        except Exception as e:
            logger.error(f"Failed to get chart configs: {e}")
            return {}
    
    def update_chart_config(self, chart_type: str, config: Dict[str, Any]):
        """Update chart configuration"""
        try:
            self.chart_factory.update_chart_config(chart_type, config)
            
            # Refresh the chart if it exists
            if chart_type in self.charts:
                self.refresh_chart(chart_type)
                
        except Exception as e:
            logger.error(f"Failed to update chart config: {e}")
    
    def get_available_chart_types(self) -> list:
        """Get list of available chart types"""
        try:
            return self.chart_factory.get_available_chart_types()
            
        except Exception as e:
            logger.error(f"Failed to get available chart types: {e}")
            return []
    
    def create_chart_display(self, chart_name: str) -> pn.pane.Plotly:
        """Create a Panel display for a chart"""
        try:
            chart = self.get_chart(chart_name)
            if chart:
                return pn.pane.Plotly(
                    chart,
                    height=400,
                    sizing_mode='stretch_width'
                )
            else:
                return pn.pane.Markdown(f"Chart {chart_name} not available")
                
        except Exception as e:
            logger.error(f"Failed to create chart display for {chart_name}: {e}")
            return pn.pane.Markdown(f"Error displaying chart {chart_name}")
    
    def create_charts_dashboard(self) -> pn.Column:
        """Create a dashboard with all charts"""
        try:
            # Create chart displays
            chart_displays = {}
            for chart_name in self.charts.keys():
                chart_displays[chart_name] = self.create_chart_display(chart_name)
            
            # Create dashboard layout
            dashboard = pn.Column(
                pn.pane.Markdown("# 📊 Demo Charts Dashboard"),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Candlestick Chart"),
                chart_displays.get('candlestick', pn.pane.Markdown("No chart")),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Volume Chart"),
                chart_displays.get('volume', pn.pane.Markdown("No chart")),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Line Chart"),
                chart_displays.get('line', pn.pane.Markdown("No chart")),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Bar Chart"),
                chart_displays.get('bar', pn.pane.Markdown("No chart")),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Portfolio Performance"),
                chart_displays.get('portfolio_performance', pn.pane.Markdown("No chart")),
                pn.Spacer(height=20),
                pn.pane.Markdown("## Trading Activity"),
                chart_displays.get('trading_activity', pn.pane.Markdown("No chart")),
                sizing_mode='stretch_width',
                background='#1e1e1e'
            )
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Failed to create charts dashboard: {e}")
            return pn.Column("Error: Failed to create charts dashboard")
    
    def get_chart_manager_status(self) -> Dict[str, Any]:
        """Get chart manager status"""
        try:
            return {
                'total_charts': len(self.charts),
                'available_charts': list(self.charts.keys()),
                'chart_configs_count': len(self.get_chart_configs()),
                'available_chart_types': self.get_available_chart_types(),
                'manager_type': 'Demo Chart Manager'
            }
            
        except Exception as e:
            logger.error(f"Failed to get chart manager status: {e}")
            return {}
