#!/usr/bin/env python3
"""
TradePulse Charts - Chart Callbacks
Handles chart callback operations and event handling
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class ChartCallbacks:
    """Handles chart callback operations and event handling"""
    
    def __init__(self, chart_data_processor, chart_display, dataset_selector, components: Dict):
        self.chart_data_processor = chart_data_processor
        self.chart_display = chart_display
        self.dataset_selector = dataset_selector
        self.components = components
    
    def update_chart(self, event):
        """Update the chart with selected data and settings"""
        try:
            chart_type = self.components['chart_type'].value
            time_range = self.components['time_range'].value
            show_volume = self.components['show_volume'].value
            show_indicators = self.components['show_indicators'].value
            
            # Get active datasets for charting
            active_datasets = self.dataset_selector.get_active_datasets()
            
            if active_datasets:
                logger.info(f"🔄 Updating {chart_type} chart with {len(active_datasets)} active datasets")
                
                # Generate chart from uploaded data
                chart_data = self.chart_data_processor.generate_chart_data(chart_type, active_datasets, time_range)
                
                # Update chart display
                self.chart_display.update_chart_display(chart_type, chart_data, show_volume, show_indicators)
                
                # Update chart statistics
                self.chart_display.update_chart_statistics(chart_type, chart_data, time_range)
                
                logger.info(f"✅ Chart updated successfully")
            else:
                logger.info("⚠️ No active datasets - using default chart data")
                # Fall back to default chart
                
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
    
    def on_dataset_change(self, change_type: str, dataset_id: str):
        """Handle dataset changes for chart operations"""
        logger.info(f"🔄 Dataset {change_type}: {dataset_id} for charts module")
        
        if change_type == 'activated':
            # Dataset is now available for charting
            logger.info(f"✅ Dataset {dataset_id} activated for chart visualization")
            
            # Update chart display to show available data
            self.chart_display.update_chart_display(
                self.components['chart_type'].value, {}, 
                self.components['show_volume'].value, 
                self.components['show_indicators'].value
            )
            
        elif change_type == 'deactivated':
            # Dataset is no longer available
            logger.info(f"❌ Dataset {dataset_id} deactivated for chart visualization")
            
            # Update chart display
            self.chart_display.update_chart_display(
                self.components['chart_type'].value, {}, 
                self.components['show_volume'].value, 
                self.components['show_indicators'].value
            )
