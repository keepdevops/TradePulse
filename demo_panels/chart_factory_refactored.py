#!/usr/bin/env python3
"""
TradePulse Demo Panels - Chart Factory (Refactored)
Handles creation of different chart types
Refactored to be under 200 lines
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
import logging

from .chart_factory_core import ChartFactoryCore

logger = logging.getLogger(__name__)

class ChartFactory:
    """Handles creation of different chart types"""
    
    def __init__(self, data_generator):
        # Use the refactored implementation
        self._refactored_factory = ChartFactoryCore(data_generator)
    
    def create_candlestick_chart(self) -> go.Figure:
        """Create candlestick chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_candlestick_chart()
    
    def create_volume_chart(self) -> go.Figure:
        """Create volume chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_volume_chart()
    
    def create_line_chart(self) -> go.Figure:
        """Create line chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_line_chart()
    
    def create_bar_chart(self) -> go.Figure:
        """Create bar chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_bar_chart()
    
    def create_portfolio_performance_chart(self) -> go.Figure:
        """Create portfolio performance chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_portfolio_performance_chart()
    
    def create_trading_activity_chart(self) -> go.Figure:
        """Create trading activity chart"""
        # Delegate to refactored implementation
        return self._refactored_factory.create_trading_activity_chart()
    
    def get_chart_configs(self) -> Dict[str, Any]:
        """Get chart configurations"""
        # Delegate to refactored implementation
        return self._refactored_factory.get_chart_configs()
    
    def update_chart_config(self, chart_type: str, config: Dict[str, Any]):
        """Update chart configuration"""
        # Delegate to refactored implementation
        return self._refactored_factory.update_chart_config(chart_type, config)
    
    def get_available_chart_types(self) -> List[str]:
        """Get list of available chart types"""
        # Delegate to refactored implementation
        return self._refactored_factory.get_available_chart_types()
    
    def validate_chart_config(self, chart_type: str, config: Dict[str, Any]) -> bool:
        """Validate chart configuration"""
        # Delegate to refactored implementation
        return self._refactored_factory.validate_chart_config(chart_type, config)



