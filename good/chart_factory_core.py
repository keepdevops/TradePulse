#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Core Functionality
Core chart factory class with basic functionality
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

from .chart_factory_components import ChartFactoryComponents
from .chart_factory_operations import ChartFactoryOperations
from .chart_factory_management import ChartFactoryManagement
from .chart_factory_charts import ChartFactoryCharts

logger = logging.getLogger(__name__)

class ChartFactoryCore:
    """Core chart factory functionality"""
    
    def __init__(self, data_generator):
        self.data_generator = data_generator
        self.chart_configs = {}
        
        # Initialize components
        self.components = ChartFactoryComponents()
        self.operations = ChartFactoryOperations()
        self.management = ChartFactoryManagement()
        self.charts = ChartFactoryCharts()
        
        # Initialize chart configurations
        self.init_chart_configs()
    
    def init_chart_configs(self):
        """Initialize chart configurations"""
        try:
            logger.info("🔧 Initializing chart configurations")
            
            # Candlestick chart configuration
            self.chart_configs['candlestick'] = {
                'height': 400,
                'template': 'plotly_dark',
                'show_volume': True,
                'show_indicators': False,
                'timeframe': '1D'
            }
            
            # Volume chart configuration
            self.chart_configs['volume'] = {
                'height': 200,
                'template': 'plotly_dark',
                'color_scheme': 'green_red',
                'show_ma': True
            }
            
            # Line chart configuration
            self.chart_configs['line'] = {
                'height': 300,
                'template': 'plotly_dark',
                'show_ma': True,
                'ma_periods': [20, 50]
            }
            
            # Bar chart configuration
            self.chart_configs['bar'] = {
                'height': 300,
                'template': 'plotly_dark',
                'orientation': 'v',
                'show_values': True
            }
            
            logger.info("✅ Chart configurations initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize chart configurations: {e}")
    
    def create_candlestick_chart(self) -> go.Figure:
        """Create candlestick chart"""
        return self.charts.create_candlestick_chart(self.data_generator, self.chart_configs)
    
    def create_volume_chart(self) -> go.Figure:
        """Create volume chart"""
        return self.charts.create_volume_chart(self.data_generator, self.chart_configs)
    
    def create_line_chart(self) -> go.Figure:
        """Create line chart"""
        return self.charts.create_line_chart(self.data_generator, self.chart_configs)
    
    def create_bar_chart(self) -> go.Figure:
        """Create bar chart"""
        return self.charts.create_bar_chart(self.data_generator, self.chart_configs)
    
    def create_portfolio_performance_chart(self) -> go.Figure:
        """Create portfolio performance chart"""
        return self.charts.create_portfolio_performance_chart(self.data_generator)
    
    def create_trading_activity_chart(self) -> go.Figure:
        """Create trading activity chart"""
        return self.charts.create_trading_activity_chart(self.data_generator)
    
    def get_chart_configs(self) -> Dict[str, Any]:
        """Get chart configurations"""
        return self.chart_configs.copy()
    
    def update_chart_config(self, chart_type: str, config: Dict[str, Any]):
        """Update chart configuration"""
        return self.operations.update_chart_config(self.chart_configs, chart_type, config)
    
    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types"""
        return list(self.chart_configs.keys())
    
    def validate_chart_config(self, chart_type: str, config: Dict[str, Any]) -> bool:
        """Validate chart configuration"""
        return self.operations.validate_chart_config(chart_type, config)

