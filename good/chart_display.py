#!/usr/bin/env python3
"""
TradePulse Charts - Chart Display
Handles chart display updates and statistics
"""

import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class ChartDisplay:
    """Handles chart display updates and statistics"""
    
    def __init__(self, components: Dict):
        self.components = components
    
    def update_chart_display(self, chart_type: str, chart_data: Dict, show_volume: bool, show_indicators: bool):
        """Update the chart display area"""
        try:
            if chart_data:
                total_points = sum(len(data) for data in chart_data.values())
                
                chart_text = f"""
                ### 📊 {chart_type} Chart
                
                **Active Datasets:** {len(chart_data)}
                **Total Data Points:** {total_points}
                **Chart Type:** {chart_type}
                **Volume Display:** {'On' if show_volume else 'Off'}
                **Indicators:** {'On' if show_indicators else 'Off'}
                
                **Datasets:**
                """
                
                for dataset_id, data in chart_data.items():
                    chart_text += f"- **{dataset_id}**: {len(data)} rows, {data.shape[1]} columns\n"
                
                chart_text += f"\n*Chart would be rendered here using Plotly/Matplotlib*"
                
                self.components['chart_display'].object = chart_text
            else:
                self.components['chart_display'].object = """
                ### 📊 Chart Display
                No data available. Please activate datasets to create charts.
                """
                
        except Exception as e:
            logger.error(f"Failed to update chart display: {e}")
    
    def update_chart_statistics(self, chart_type: str, chart_data: Dict, time_range: str):
        """Update the chart statistics display"""
        try:
            if chart_data:
                total_points = sum(len(data) for data in chart_data.values())
                
                stats_text = f"""
                **Chart Statistics:**
                - **Data Points**: {total_points}
                - **Datasets**: {len(chart_data)}
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
