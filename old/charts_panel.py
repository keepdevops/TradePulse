#!/usr/bin/env python3
"""
TradePulse Charts - Main Panel
Refactored charts panel using focused components
"""

import panel as pn
import pandas as pd
from typing import Dict
import logging

from .. import BasePanel
from ..dataset_selector_component import DatasetSelectorComponent
from .chart_manager import ChartManager
from .chart_data_processor import ChartDataProcessor

logger = logging.getLogger(__name__)

class ChartsPanel(BasePanel):
    """Refactored charts panel using focused components"""
    
    def __init__(self, data_manager):
        self.dataset_selector = DatasetSelectorComponent(data_manager, 'charts')
        self.chart_manager = ChartManager()
        self.data_processor = ChartDataProcessor()
        super().__init__("Charts", data_manager)
    
    def init_panel(self):
        """Initialize refactored charts panel components"""
        self._init_ui_components()
        self._setup_callbacks()
    
    def _init_ui_components(self):
        """Initialize UI components"""
        # Chart type selector
        self.components['chart_type'] = pn.widgets.Select(
            name='Chart Type',
            options=self.chart_manager.get_supported_chart_types(),
            value='Candlestick',
            width=150
        )
        
        # Time range selector
        self.components['time_range'] = pn.widgets.Select(
            name='Time Range',
            options=self.chart_manager.get_supported_time_ranges(),
            value='1M',
            width=100
        )
        
        # Chart controls
        self.components['show_volume'] = pn.widgets.Checkbox(
            name='Show Volume',
            value=True,
            width=120
        )
        
        self.components['show_indicators'] = pn.widgets.Checkbox(
            name='Show Indicators',
            value=True,
            width=120
        )
        
        # Action buttons
        self.components['update_chart'] = pn.widgets.Button(
            name='🔄 Update Chart',
            button_type='primary',
            width=150
        )
        
        self.components['export_chart'] = pn.widgets.Button(
            name='📤 Export Chart',
            button_type='success',
            width=150
        )
        
        self.components['save_chart'] = pn.widgets.Button(
            name='💾 Save Chart',
            button_type='warning',
            width=150
        )
        
        # Chart display area
        self.components['chart_display'] = pn.pane.Markdown("""
        ### 📊 Chart Display
        Select a dataset and chart type to visualize your data
        """)
        
        # Chart statistics
        self.components['chart_stats'] = pn.pane.Markdown("""
        **Chart Statistics:**
        - **Data Points**: 0
        - **Date Range**: None
        - **Chart Type**: None
        """)
    
    def _setup_callbacks(self):
        """Setup component callbacks"""
        self.components['update_chart'].on_click(self.update_chart)
        self.components['export_chart'].on_click(self.export_chart)
        self.components['save_chart'].on_click(self.save_chart)
        
        # Dataset selector callback
        self.dataset_selector.add_dataset_change_callback(self.on_dataset_change)
    
    def get_panel(self):
        """Get the refactored charts panel layout"""
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
    
    def update_chart(self, event):
        """Update the chart using the chart manager and data processor"""
        try:
            chart_type = self.components['chart_type'].value
            time_range = self.components['time_range'].value
            show_volume = self.components['show_volume'].value
            show_indicators = self.components['show_indicators'].value
            
            # Get active datasets for charting
            active_datasets = self.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"🔄 Updating {chart_type} chart with {len(active_datasets)} active datasets")
                
                # Create chart configuration
                chart_config = {
                    'type': chart_type,
                    'time_range': time_range,
                    'show_volume': show_volume,
                    'show_indicators': show_indicators,
                    'datasets': list(active_datasets.keys())
                }
                
                # Validate chart configuration
                is_valid, errors = self.chart_manager.validate_chart_config(chart_config)
                if not is_valid:
                    logger.error(f"❌ Invalid chart configuration: {errors}")
                    return
                
                # Process data for chart
                processed_data = self.data_processor.process_data_for_chart(
                    chart_type, active_datasets, time_range
                )
                
                # Create or update chart
                chart_id = self.chart_manager.create_chart(chart_config)
                
                # Update chart display
                self._update_chart_display(chart_type, processed_data, show_volume, show_indicators)
                
                # Update chart statistics
                self._update_chart_statistics(chart_type, processed_data, time_range)
                
                logger.info(f"✅ Chart updated successfully: {chart_id}")
            else:
                logger.info("⚠️ No active datasets - using default chart data")
                
        except Exception as e:
            logger.error(f"❌ Chart update failed: {e}")
    
    def export_chart(self, event):
        """Export the current chart"""
        try:
            chart_type = self.components['chart_type'].value
            
            logger.info(f"📤 Exporting {chart_type} chart")
            
            # Here you would implement actual chart export
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"❌ Chart export failed: {e}")
    
    def save_chart(self, event):
        """Save the current chart configuration"""
        try:
            chart_type = self.components['chart_type'].value
            time_range = self.components['time_range'].value
            
            logger.info(f"💾 Saving {chart_type} chart configuration with {time_range} time range")
            
            # Here you would implement actual chart saving
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"❌ Chart save failed: {e}")
    
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
                
                self.components['chart_display'].object = chart_text
            else:
                self.components['chart_display'].object = """
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
                
                self.components['chart_stats'].object = stats_text
            else:
                self.components['chart_stats'].object = """
                **Chart Statistics:**
                - **Data Points**: 0
                - **Datasets**: 0
                - **Chart Type**: None
                - **Time Range**: None
                """
                
        except Exception as e:
            logger.error(f"Failed to update chart statistics: {e}")
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for chart operations"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for charts module")
        
        if change_type == 'activated':
            # Dataset is now available for charting
            logger.info(f"✅ Dataset {dataset_id} activated for chart visualization")
            
            # Update chart display to show available data
            self._update_chart_display(self.components['chart_type'].value, {}, 
                                     self.components['show_volume'].value, 
                                     self.components['show_indicators'].value)
            
        elif change_type == 'deactivated':
            # Dataset is no longer available
            logger.info(f"❌ Dataset {dataset_id} deactivated for chart visualization")
            
            # Update chart display
            self._update_chart_display(self.components['chart_type'].value, {}, 
                                     self.components['show_volume'].value, 
                                     self.components['show_indicators'].value)
