#!/usr/bin/env python3
"""
TradePulse Charts - Chart Layout
Handles chart panel layout creation
"""

import panel as pn
from typing import Dict

class ChartLayout:
    """Handles chart panel layout creation"""
    
    def __init__(self, components: Dict, dataset_selector):
        self.components = components
        self.dataset_selector = dataset_selector
    
    def create_panel_layout(self):
        """Create the enhanced charts panel layout"""
        # Chart controls
        chart_controls = pn.Column(
            pn.pane.Markdown("### 📊 Chart Controls"),
            pn.Row(
                self.components['chart_type'],
                self.components['time_range'],
                align='center'
            ),
            pn.Row(
                self.components['show_volume'],
                self.components['show_indicators'],
                align='center'
            ),
            pn.Row(
                self.components['update_chart'],
                self.components['export_chart'],
                self.components['save_chart'],
                align='center'
            ),
            sizing_mode='stretch_width'
        )
        
        # Chart display
        chart_display = pn.Column(
            pn.pane.Markdown("### 📈 Chart Visualization"),
            self.components['chart_display'],
            self.components['chart_stats'],
            sizing_mode='stretch_width'
        )
        
        # Dataset selector
        dataset_section = self.dataset_selector.get_component()
        
        # Main layout with tabs
        tabs = pn.Tabs(
            ('📊 Chart Controls', chart_controls),
            ('📈 Visualization', chart_display),
            ('📁 Data Sources', dataset_section),
            sizing_mode='stretch_width'
        )
        
        return pn.Column(
            pn.pane.Markdown("### 📊 Enhanced Chart Management"),
            pn.pane.Markdown("Create professional charts and visualizations from uploaded data"),
            tabs,
            sizing_mode='stretch_width'
        )
