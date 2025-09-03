#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Performance Display (Refactored)
Handles performance data visualization and display
Refactored to be under 200 lines
"""

import panel as pn
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import logging

from .performance_display_core import PerformanceDisplayCore

logger = logging.getLogger(__name__)

class PerformanceDisplay:
    """Handles performance data visualization and display"""
    
    def __init__(self, performance_metrics):
        # Use the refactored implementation
        self._refactored_display = PerformanceDisplayCore(performance_metrics)
    
    def create_metrics_summary(self) -> pn.Column:
        """Create metrics summary display"""
        # Delegate to refactored implementation
        return self._refactored_display.create_metrics_summary()
    
    def create_response_time_chart(self) -> pn.pane.Plotly:
        """Create response time chart"""
        # Delegate to refactored implementation
        return self._refactored_display.create_response_time_chart()
    
    def create_system_usage_chart(self) -> pn.pane.Plotly:
        """Create system usage chart"""
        # Delegate to refactored implementation
        return self._refactored_display.create_system_usage_chart()
    
    def create_alerts_display(self) -> pn.Column:
        """Create performance alerts display"""
        # Delegate to refactored implementation
        return self._refactored_display.create_alerts_display()
    
    def create_operations_table(self) -> pn.widgets.Tabulator:
        """Create operations history table"""
        # Delegate to refactored implementation
        return self._refactored_display.create_operations_table()
    
    def create_control_buttons(self) -> pn.Row:
        """Create control buttons"""
        # Delegate to refactored implementation
        return self._refactored_display.create_control_buttons()
    
    def refresh_display(self, event=None):
        """Refresh all display components"""
        # Delegate to refactored implementation
        return self._refactored_display.refresh_display(event)
    
    def export_data(self, event=None):
        """Export performance data"""
        # Delegate to refactored implementation
        return self._refactored_display.export_data(event)
    
    def reset_metrics(self, event=None):
        """Reset performance metrics"""
        # Delegate to refactored implementation
        return self._refactored_display.reset_metrics(event)
    
    def get_display_layout(self) -> pn.Column:
        """Get the complete display layout"""
        # Delegate to refactored implementation
        return self._refactored_display.get_display_layout()



