#!/usr/bin/env python3
"""
TradePulse Demo Chart Factory - Operations
Chart-related operations for the chart factory
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class ChartFactoryOperations:
    """Chart-related operations for chart factory"""
    
    def update_chart_config(self, chart_configs: Dict, chart_type: str, config: Dict[str, Any]):
        """Update chart configuration"""
        try:
            if chart_type in chart_configs:
                chart_configs[chart_type].update(config)
                logger.info(f"✅ Updated configuration for {chart_type} chart")
            else:
                logger.warning(f"⚠️ Chart type {chart_type} not found")
                
        except Exception as e:
            logger.error(f"Failed to update chart config: {e}")
    
    def validate_chart_config(self, chart_type: str, config: Dict[str, Any]) -> bool:
        """Validate chart configuration"""
        try:
            # Check required fields based on chart type
            if chart_type == 'candlestick':
                required_fields = ['height', 'template']
            elif chart_type == 'volume':
                required_fields = ['height', 'template', 'color_scheme']
            elif chart_type == 'line':
                required_fields = ['height', 'template', 'ma_periods']
            elif chart_type == 'bar':
                required_fields = ['height', 'template', 'orientation']
            else:
                required_fields = ['height', 'template']
            
            # Check if all required fields are present
            for field in required_fields:
                if field not in config:
                    return False
            
            # Validate height
            if 'height' in config and not isinstance(config['height'], int):
                return False
            
            # Validate template
            valid_templates = ['plotly_dark', 'plotly_white', 'plotly_light']
            if 'template' in config and config['template'] not in valid_templates:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate chart config: {e}")
            return False
    
    def export_chart_configs(self, chart_configs: Dict, filename: str = None) -> str:
        """Export chart configurations to JSON file"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"chart_configs_export_{timestamp}.json"
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(chart_configs, f, indent=2)
            
            logger.info(f"📤 Chart configurations exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export chart configurations to JSON: {e}")
            return None
    
    def import_chart_configs(self, chart_configs: Dict, filename: str) -> int:
        """Import chart configurations from JSON file"""
        try:
            import json
            
            with open(filename, 'r') as f:
                import_data = json.load(f)
            
            imported_count = 0
            for chart_type, config in import_data.items():
                if self.validate_chart_config(chart_type, config):
                    chart_configs[chart_type] = config
                    imported_count += 1
            
            logger.info(f"📥 Imported {imported_count} chart configurations from {filename}")
            return imported_count
            
        except Exception as e:
            logger.error(f"Failed to import chart configurations from JSON: {e}")
            return 0
    
    def get_chart_summary(self, chart_type: str, config: Dict[str, Any]) -> str:
        """Get text summary of chart configuration"""
        try:
            if not config:
                return "No configuration available"
            
            summary_lines = [
                f"**Chart Type**: {chart_type}",
                f"**Height**: {config.get('height', 'N/A')}",
                f"**Template**: {config.get('template', 'N/A')}"
            ]
            
            # Add type-specific fields
            if chart_type == 'candlestick':
                summary_lines.append(f"**Show Volume**: {config.get('show_volume', 'N/A')}")
                summary_lines.append(f"**Show Indicators**: {config.get('show_indicators', 'N/A')}")
            elif chart_type == 'line':
                summary_lines.append(f"**Show MA**: {config.get('show_ma', 'N/A')}")
                summary_lines.append(f"**MA Periods**: {config.get('ma_periods', 'N/A')}")
            elif chart_type == 'bar':
                summary_lines.append(f"**Orientation**: {config.get('orientation', 'N/A')}")
                summary_lines.append(f"**Show Values**: {config.get('show_values', 'N/A')}")
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create chart summary: {e}")
            return "Error creating summary"
    
    def create_error_chart(self, error_message: str) -> go.Figure:
        """Create error chart when chart creation fails"""
        try:
            fig = go.Figure()
            fig.add_annotation(
                text=error_message,
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16, color="red")
            )
            fig.update_layout(
                title='Chart Error',
                template='plotly_dark',
                height=300
            )
            return fig
            
        except Exception as e:
            logger.error(f"Failed to create error chart: {e}")
            # Return minimal figure
            return go.Figure()



