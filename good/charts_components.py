#!/usr/bin/env python3
"""
TradePulse Charts Panel - Components
UI components for the charts panel
"""

import panel as pn
import logging

logger = logging.getLogger(__name__)

class ChartsComponents:
    """UI components for charts panel"""
    
    def __init__(self):
        self.chart_type = None
        self.time_range = None
        self.show_volume = None
        self.show_indicators = None
        self.update_chart = None
        self.export_chart = None
        self.save_chart = None
        self.chart_display = None
        self.chart_stats = None
    
    def create_basic_components(self, chart_manager):
        """Create basic UI components"""
        # Chart type selector
        self.chart_type = pn.widgets.Select(
            name='Chart Type',
            options=chart_manager.get_supported_chart_types(),
            value='Candlestick',
            width=150
        )
        
        # Time range selector
        self.time_range = pn.widgets.Select(
            name='Time Range',
            options=chart_manager.get_supported_time_ranges(),
            value='1M',
            width=100
        )
        
        # Chart controls
        self.show_volume = pn.widgets.Checkbox(
            name='Show Volume',
            value=True,
            width=120
        )
        
        self.show_indicators = pn.widgets.Checkbox(
            name='Show Indicators',
            value=True,
            width=120
        )
        
        # Action buttons
        self.update_chart = pn.widgets.Button(
            name='🔄 Update Chart',
            button_type='primary',
            width=150
        )
        
        self.export_chart = pn.widgets.Button(
            name='📤 Export Chart',
            button_type='success',
            width=150
        )
        
        self.save_chart = pn.widgets.Button(
            name='💾 Save Chart',
            button_type='warning',
            width=150
        )
        
        # Chart display area
        self.chart_display = pn.pane.Markdown("""
        ### 📊 Chart Display
        Select a dataset and chart type to visualize your data
        """)
        
        # Chart statistics
        self.chart_stats = pn.pane.Markdown("""
        **Chart Statistics:**
        - **Data Points**: 0
        - **Date Range**: None
        - **Chart Type**: None
        """)

