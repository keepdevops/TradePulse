#!/usr/bin/env python3
"""
TradePulse Integrated Performance Display - Core Functionality
Core performance display class with basic functionality
"""

import panel as pn
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import logging

from .performance_display_components import PerformanceDisplayComponents
from .performance_display_operations import PerformanceDisplayOperations
from .performance_display_management import PerformanceDisplayManagement
from .performance_display_charts import PerformanceDisplayCharts

logger = logging.getLogger(__name__)

class PerformanceDisplayCore:
    """Core performance display functionality"""
    
    def __init__(self, performance_metrics):
        self.performance_metrics = performance_metrics
        self.display_components = {}
        
        # Initialize components
        self.components = PerformanceDisplayComponents()
        self.operations = PerformanceDisplayOperations()
        self.management = PerformanceDisplayManagement()
        self.charts = PerformanceDisplayCharts()
        
        # Create display components
        self.create_display_components()
    
    def create_display_components(self):
        """Create all display components"""
        try:
            logger.info("🔧 Creating performance display components")
            
            # Create metrics summary
            self.display_components['metrics_summary'] = self.create_metrics_summary()
            
            # Create performance charts
            self.display_components['response_time_chart'] = self.create_response_time_chart()
            self.display_components['system_usage_chart'] = self.create_system_usage_chart()
            
            # Create alerts display
            self.display_components['alerts_display'] = self.create_alerts_display()
            
            # Create operations table
            self.display_components['operations_table'] = self.create_operations_table()
            
            # Create control buttons
            self.display_components['control_buttons'] = self.create_control_buttons()
            
            logger.info("✅ Performance display components created")
            
        except Exception as e:
            logger.error(f"Failed to create display components: {e}")
    
    def create_metrics_summary(self) -> pn.Column:
        """Create metrics summary display"""
        return self.components.create_metrics_summary(self.performance_metrics)
    
    def create_response_time_chart(self) -> pn.pane.Plotly:
        """Create response time chart"""
        return self.charts.create_response_time_chart(self.performance_metrics)
    
    def create_system_usage_chart(self) -> pn.pane.Plotly:
        """Create system usage chart"""
        return self.charts.create_system_usage_chart(self.performance_metrics)
    
    def create_alerts_display(self) -> pn.Column:
        """Create performance alerts display"""
        return self.components.create_alerts_display(self.performance_metrics)
    
    def create_operations_table(self) -> pn.widgets.Tabulator:
        """Create operations history table"""
        return self.components.create_operations_table(self.performance_metrics)
    
    def create_control_buttons(self) -> pn.Row:
        """Create control buttons"""
        return self.components.create_control_buttons(self)
    
    def refresh_display(self, event=None):
        """Refresh all display components"""
        return self.operations.refresh_display(self)
    
    def export_data(self, event=None):
        """Export performance data"""
        return self.operations.export_data(self.performance_metrics)
    
    def reset_metrics(self, event=None):
        """Reset performance metrics"""
        return self.operations.reset_metrics(self)
    
    def get_display_layout(self) -> pn.Column:
        """Get the complete display layout"""
        return self.management.get_display_layout(self.display_components)



