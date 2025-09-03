#!/usr/bin/env python3
"""
TradePulse Charts Panel - Callbacks Manager
Callback management for the charts panel
"""

import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ChartsCallbacks:
    """Callback management for charts panel"""
    
    def __init__(self, core_panel):
        self.core_panel = core_panel
    
    def update_chart(self, event):
        """Update the chart using the chart manager and data processor"""
        try:
            chart_type = self.core_panel.components.chart_type.value
            time_range = self.core_panel.components.time_range.value
            show_volume = self.core_panel.components.show_volume.value
            show_indicators = self.core_panel.components.show_indicators.value
            
            # Get active datasets for charting
            active_datasets = self.core_panel.dataset_selector.get_active_datasets()
            
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
                is_valid, errors = self.core_panel.chart_manager.validate_chart_config(chart_config)
                if not is_valid:
                    logger.error(f"❌ Invalid chart configuration: {errors}")
                    return
                
                # Process data for chart
                processed_data = self.core_panel.data_processor.process_data_for_chart(
                    chart_type, active_datasets, time_range
                )
                
                # Create or update chart
                chart_id = self.core_panel.chart_manager.create_chart(chart_config)
                
                # Update chart display
                self.core_panel._update_chart_display(chart_type, processed_data, show_volume, show_indicators)
                
                # Update chart statistics
                self.core_panel._update_chart_statistics(chart_type, processed_data, time_range)
                
                logger.info(f"✅ Chart updated successfully: {chart_id}")
            else:
                logger.info("⚠️ No active datasets - using default chart data")
                
        except Exception as e:
            logger.error(f"❌ Chart update failed: {e}")
    
    def export_chart(self, event):
        """Export the current chart"""
        try:
            chart_type = self.core_panel.components.chart_type.value
            
            logger.info(f"📤 Exporting {chart_type} chart")
            
            # Here you would implement actual chart export
            # For now, just log the action
            
        except Exception as e:
            logger.error(f"❌ Chart export failed: {e}")
    
    def save_chart(self, event):
        """Save the current chart configuration"""
        try:
            chart_type = self.core_panel.components.chart_type.value
            time_range = self.core_panel.components.time_range.value
            
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
            self.core_panel._update_chart_display(
                self.core_panel.components.chart_type.value, {}, 
                self.core_panel.components.show_volume.value, 
                self.core_panel.components.show_indicators.value
            )
            
        elif change_type == 'deactivated':
            # Dataset is no longer available
            logger.info(f"❌ Dataset {dataset_id} deactivated for chart visualization")
            
            # Update chart display
            self.core_panel._update_chart_display(
                self.core_panel.components.chart_type.value, {}, 
                self.core_panel.components.show_volume.value, 
                self.core_panel.components.show_indicators.value
            )

