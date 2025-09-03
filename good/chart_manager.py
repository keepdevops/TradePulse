#!/usr/bin/env python3
"""
TradePulse Charts - Chart Manager
Manages chart creation, configuration, and lifecycle
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class ChartManager:
    """Manages chart creation, configuration, and lifecycle"""
    
    def __init__(self):
        self.charts = {}
        self.chart_counter = 0
        self.supported_chart_types = [
            'Candlestick', 'Line', 'Bar', 'Scatter', 'Heatmap', '3D Surface'
        ]
    
    def create_chart(self, chart_config: Dict) -> str:
        """Create a new chart with the given configuration"""
        try:
            self.chart_counter += 1
            chart_id = f"chart_{self.chart_counter}"
            
            chart = {
                'id': chart_id,
                'type': chart_config.get('type', 'Candlestick'),
                'time_range': chart_config.get('time_range', '1M'),
                'show_volume': chart_config.get('show_volume', True),
                'show_indicators': chart_config.get('show_indicators', True),
                'datasets': chart_config.get('datasets', []),
                'created': pd.Timestamp.now(),
                'last_updated': pd.Timestamp.now(),
                'configuration': chart_config
            }
            
            self.charts[chart_id] = chart
            logger.info(f"✅ Chart created successfully: {chart_id}")
            return chart_id
            
        except Exception as e:
            logger.error(f"❌ Chart creation failed: {e}")
            raise
    
    def get_chart(self, chart_id: str) -> Optional[Dict]:
        """Get chart by ID"""
        return self.charts.get(chart_id)
    
    def update_chart(self, chart_id: str, updates: Dict) -> bool:
        """Update an existing chart"""
        try:
            chart = self.get_chart(chart_id)
            if chart:
                chart.update(updates)
                chart['last_updated'] = pd.Timestamp.now()
                logger.info(f"✅ Chart {chart_id} updated successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to update chart {chart_id}: {e}")
            return False
    
    def delete_chart(self, chart_id: str) -> bool:
        """Delete a chart"""
        try:
            if chart_id in self.charts:
                del self.charts[chart_id]
                logger.info(f"✅ Chart {chart_id} deleted successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to delete chart {chart_id}: {e}")
            return False
    
    def get_charts_by_type(self, chart_type: str) -> List[Dict]:
        """Get all charts of a specific type"""
        return [chart for chart in self.charts.values() if chart['type'] == chart_type]
    
    def get_charts_for_dataset(self, dataset_id: str) -> List[Dict]:
        """Get all charts that use a specific dataset"""
        return [chart for chart in self.charts.values() if dataset_id in chart['datasets']]
    
    def get_chart_statistics(self) -> Dict:
        """Get comprehensive chart statistics"""
        try:
            total_charts = len(self.charts)
            type_counts = {}
            
            for chart in self.charts.values():
                chart_type = chart['type']
                type_counts[chart_type] = type_counts.get(chart_type, 0) + 1
            
            # Count charts by time range
            time_range_counts = {}
            for chart in self.charts.values():
                time_range = chart['time_range']
                time_range_counts[time_range] = time_range_counts.get(time_range, 0) + 1
            
            return {
                'total_charts': total_charts,
                'type_distribution': type_counts,
                'time_range_distribution': time_range_counts,
                'charts_with_volume': sum(1 for c in self.charts.values() if c['show_volume']),
                'charts_with_indicators': sum(1 for c in self.charts.values() if c['show_indicators'])
            }
            
        except Exception as e:
            logger.error(f"Failed to get chart statistics: {e}")
            return {}
    
    def export_charts_to_dataframe(self) -> pd.DataFrame:
        """Export all charts to a pandas DataFrame"""
        try:
            if not self.charts:
                return pd.DataFrame()
            
            charts_data = []
            for chart in self.charts.values():
                charts_data.append({
                    'ID': chart['id'],
                    'Type': chart['type'],
                    'Time Range': chart['time_range'],
                    'Volume': 'Yes' if chart['show_volume'] else 'No',
                    'Indicators': 'Yes' if chart['show_indicators'] else 'No',
                    'Datasets': len(chart['datasets']),
                    'Created': chart['created'].strftime('%Y-%m-%d %H:%M:%S'),
                    'Last Updated': chart['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
                })
            
            return pd.DataFrame(charts_data)
            
        except Exception as e:
            logger.error(f"Failed to export charts to DataFrame: {e}")
            return pd.DataFrame()
    
    def validate_chart_config(self, chart_config: Dict) -> Tuple[bool, List[str]]:
        """Validate chart configuration and return errors if any"""
        errors = []
        
        # Check required fields
        if 'type' not in chart_config:
            errors.append("Missing required field: type")
        elif chart_config['type'] not in self.supported_chart_types:
            errors.append(f"Unsupported chart type: {chart_config['type']}")
        
        # Check time range
        valid_time_ranges = ['1D', '1W', '1M', '3M', '6M', '1Y', 'All']
        if 'time_range' in chart_config and chart_config['time_range'] not in valid_time_ranges:
            errors.append(f"Invalid time range: {chart_config['time_range']}")
        
        # Check boolean fields
        boolean_fields = ['show_volume', 'show_indicators']
        for field in boolean_fields:
            if field in chart_config and not isinstance(chart_config[field], bool):
                errors.append(f"{field} must be a boolean value")
        
        return len(errors) == 0, errors
    
    def get_supported_chart_types(self) -> List[str]:
        """Get list of supported chart types"""
        return self.supported_chart_types.copy()
    
    def get_supported_time_ranges(self) -> List[str]:
        """Get list of supported time ranges"""
        return ['1D', '1W', '1M', '3M', '6M', '1Y', 'All']
