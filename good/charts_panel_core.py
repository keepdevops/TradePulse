#!/usr/bin/env python3
"""
TradePulse Charts Panel - Core Functionality
Core charts panel class with basic functionality
"""

import panel as pn
import pandas as pd
import logging
from typing import Dict

from .. import BasePanel
from .charts_components import ChartsComponents
from .charts_operations import ChartsOperations
from .charts_management import ChartsManagement
from .charts_callbacks import ChartsCallbacks
from ..dataset_selector_component import DatasetSelectorComponent
from .chart_manager import ChartManager
from .chart_data_processor import ChartDataProcessor

logger = logging.getLogger(__name__)

class ChartsPanelCore(BasePanel):
    """Core charts panel functionality"""
    
    def __init__(self, data_manager):
        super().__init__("Charts", data_manager)
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'charts')
        self.chart_manager = ChartManager()
        self.data_processor = ChartDataProcessor()
        
        # Initialize components
        self.components = ChartsComponents()
        self.operations = ChartsOperations()
        self.management = ChartsManagement()
        self.callbacks = ChartsCallbacks(self)
        
        self.init_panel()
    
    def init_panel(self):
        """Initialize core panel components"""
        self.components.create_basic_components(self.chart_manager)
        self.setup_callbacks()
    
    def setup_callbacks(self):
        """Setup component callbacks"""
        self.components.update_chart.on_click(self.callbacks.update_chart)
        self.components.export_chart.on_click(self.callbacks.export_chart)
        self.components.save_chart.on_click(self.callbacks.save_chart)
        
        # Dataset selector callback
        self.dataset_selector.add_dataset_change_callback(self.callbacks.on_dataset_change)
    
    def get_panel(self):
        """Get the core panel layout"""
        return self.management.create_panel_layout(
            self.components,
            self.dataset_selector
        )
    
    def update_chart(self, event):
        """Update the chart using the chart manager and data processor"""
        return self.callbacks.update_chart(event)
    
    def export_chart(self, event):
        """Export the current chart"""
        return self.callbacks.export_chart(event)
    
    def save_chart(self, event):
        """Save the current chart configuration"""
        return self.callbacks.save_chart(event)
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for chart operations"""
        return self.callbacks.on_dataset_change(change_type, dataset_id)
    
    def _update_chart_display(self, chart_type: str, chart_data: Dict, 
                             show_volume: bool, show_indicators: bool):
        """Update the chart display area"""
        try:
            if chart_data:
                # Get chart summary from data processor
                summary = self.data_processor.get_chart_summary(chart_type, chart_data)
                
                chart_text = f"""
                ### 📊 {chart_type} Chart
                
                **Active Datasets:** {summary['total_datasets']}
                **Total Data Points:** {summary['total_data_points']}
                **Chart Type:** {chart_type}
                **Volume Display:** {'On' if show_volume else 'Off'}
                **Indicators:** {'On' if show_indicators else 'Off'}
                
                **Datasets:**
                """
                
                for dataset_id, info in summary.get('datasets_info', {}).items():
                    chart_text += f"- **{dataset_id}**: {info['rows']} rows, {info['columns']} columns\n"
                
                chart_text += f"\n*Chart would be rendered here using Plotly/Matplotlib*"
                
                self.components.chart_display.object = chart_text
            else:
                self.components.chart_display.object = """
                ### 📊 Chart Display
                No data available. Please activate datasets to create charts.
                """
                
        except Exception as e:
            logger.error(f"Failed to update chart display: {e}")
    
    def _update_chart_statistics(self, chart_type: str, chart_data: Dict, time_range: str):
        """Update the chart statistics display"""
        try:
            if chart_data:
                # Get chart summary from data processor
                summary = self.data_processor.get_chart_summary(chart_type, chart_data)
                
                stats_text = f"""
                **Chart Statistics:**
                - **Data Points**: {summary['total_data_points']}
                - **Datasets**: {summary['total_datasets']}
                - **Chart Type**: {chart_type}
                - **Time Range**: {time_range}
                - **Last Updated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
                """
                
                self.components.chart_stats.object = stats_text
            else:
                self.components.chart_stats.object = """
                **Chart Statistics:**
                - **Data Points**: 0
                - **Datasets**: 0
                - **Chart Type**: None
                - **Time Range**: None
                """
                
        except Exception as e:
            logger.error(f"Failed to update chart statistics: {e}")

