#!/usr/bin/env python3
"""
TradePulse Charts Panel - Operations
Chart-related operations for the charts panel
"""

import pandas as pd
import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)

class ChartsOperations:
    """Chart-related operations for charts panel"""
    
    def validate_chart_config(self, config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate chart configuration"""
        errors = []
        
        # Check required fields
        required_fields = ['type', 'time_range']
        for field in required_fields:
            if field not in config or not config[field]:
                errors.append(f"Missing required field: {field}")
        
        # Validate chart type
        valid_types = ['Candlestick', 'Line', 'Bar', 'Scatter', 'Heatmap', '3D Surface']
        if 'type' in config and config['type'] not in valid_types:
            errors.append(f"Invalid chart type: {config['type']}")
        
        # Validate time range
        valid_ranges = ['1D', '1W', '1M', '3M', '6M', '1Y', 'All']
        if 'time_range' in config and config['time_range'] not in valid_ranges:
            errors.append(f"Invalid time range: {config['time_range']}")
        
        return len(errors) == 0, errors
    
    def create_chart_id(self, chart_type: str) -> str:
        """Create unique chart ID"""
        import uuid
        timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"{chart_type.replace(' ', '_').lower()}_{timestamp}_{unique_id}"
    
    def get_chart_info(self, chart_type: str) -> Dict[str, Any]:
        """Get information about a specific chart type"""
        chart_info = {
            'Candlestick': {
                'description': 'Price action chart with open, high, low, close',
                'best_for': 'Stock price analysis',
                'data_requirements': ['datetime', 'open', 'high', 'low', 'close']
            },
            'Line': {
                'description': 'Simple line chart connecting data points',
                'best_for': 'Trend analysis',
                'data_requirements': ['datetime', 'value']
            },
            'Bar': {
                'description': 'Bar chart showing discrete values',
                'best_for': 'Comparison analysis',
                'data_requirements': ['category', 'value']
            },
            'Scatter': {
                'description': 'Scatter plot showing correlation',
                'best_for': 'Correlation analysis',
                'data_requirements': ['x', 'y']
            },
            'Heatmap': {
                'description': 'Color-coded matrix visualization',
                'best_for': 'Matrix data analysis',
                'data_requirements': ['x', 'y', 'value']
            },
            '3D Surface': {
                'description': 'Three-dimensional surface plot',
                'best_for': '3D data visualization',
                'data_requirements': ['x', 'y', 'z']
            }
        }
        
        return chart_info.get(chart_type, {})
    
    def get_chart_statistics(self, chart_data: Dict) -> Dict[str, Any]:
        """Get statistics about chart data"""
        if not chart_data:
            return {
                'total_datasets': 0,
                'total_data_points': 0,
                'datasets_info': {}
            }
        
        stats = {
            'total_datasets': len(chart_data),
            'total_data_points': 0,
            'datasets_info': {}
        }
        
        # Calculate statistics for each dataset
        for dataset_id, data in chart_data.items():
            if isinstance(data, pd.DataFrame):
                rows, cols = data.shape
                stats['total_data_points'] += rows
                stats['datasets_info'][dataset_id] = {
                    'rows': rows,
                    'columns': cols,
                    'memory_usage': data.memory_usage(deep=True).sum()
                }
        
        return stats
    
    def filter_data_by_time_range(self, data: pd.DataFrame, time_range: str) -> pd.DataFrame:
        """Filter data by time range"""
        try:
            if data.empty or 'datetime' not in data.columns:
                return data
            
            # Convert datetime column if needed
            if not pd.api.types.is_datetime64_any_dtype(data['datetime']):
                data['datetime'] = pd.to_datetime(data['datetime'])
            
            # Calculate time delta
            now = pd.Timestamp.now()
            if time_range == '1D':
                delta = pd.Timedelta(days=1)
            elif time_range == '1W':
                delta = pd.Timedelta(weeks=1)
            elif time_range == '1M':
                delta = pd.Timedelta(days=30)
            elif time_range == '3M':
                delta = pd.Timedelta(days=90)
            elif time_range == '6M':
                delta = pd.Timedelta(days=180)
            elif time_range == '1Y':
                delta = pd.Timedelta(days=365)
            else:  # 'All'
                return data
            
            # Filter data
            cutoff_date = now - delta
            return data[data['datetime'] >= cutoff_date]
            
        except Exception as e:
            logger.error(f"Failed to filter data by time range: {e}")
            return data
    
    def get_chart_summary(self, chart_type: str, chart_data: Dict) -> Dict[str, Any]:
        """Get summary information for chart display"""
        stats = self.get_chart_statistics(chart_data)
        chart_info = self.get_chart_info(chart_type)
        
        return {
            'total_datasets': stats['total_datasets'],
            'total_data_points': stats['total_data_points'],
            'datasets_info': stats['datasets_info'],
            'chart_type': chart_type,
            'description': chart_info.get('description', ''),
            'best_for': chart_info.get('best_for', ''),
            'data_requirements': chart_info.get('data_requirements', [])
        }



