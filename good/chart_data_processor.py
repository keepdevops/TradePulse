#!/usr/bin/env python3
"""
TradePulse Charts - Chart Data Processor
Handles chart data processing and filtering
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class ChartDataProcessor:
    """Handles chart data processing and filtering"""
    
    def __init__(self):
        pass
    
    def generate_chart_data(self, chart_type: str, active_datasets: Dict, time_range: str) -> Dict:
        """Generate chart data from uploaded datasets"""
        chart_data = {}
        
        for dataset_id, data in active_datasets.items():
            logger.info(f"📊 Processing dataset {dataset_id}: {data.shape[0]} rows × {data.shape[1]} cols")
            
            # Filter data based on time range
            filtered_data = self.filter_data_by_time(data, time_range)
            
            # Process data based on chart type
            if chart_type == 'Candlestick':
                chart_data[dataset_id] = self.process_candlestick_data(filtered_data)
            elif chart_type == 'Line':
                chart_data[dataset_id] = self.process_line_data(filtered_data)
            elif chart_type == 'Bar':
                chart_data[dataset_id] = self.process_bar_data(filtered_data)
            elif chart_type == 'Scatter':
                chart_data[dataset_id] = self.process_scatter_data(filtered_data)
            else:
                chart_data[dataset_id] = filtered_data
        
        return chart_data
    
    def filter_data_by_time(self, data: pd.DataFrame, time_range: str) -> pd.DataFrame:
        """Filter data based on selected time range"""
        try:
            if 'Date' in data.columns:
                # Convert to datetime if needed
                if not pd.api.types.is_datetime64_any_dtype(data['Date']):
                    data['Date'] = pd.to_datetime(data['Date'])
                
                # Apply time filtering
                if time_range == '1D':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(days=1)
                elif time_range == '1W':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(weeks=1)
                elif time_range == '1M':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
                elif time_range == '3M':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(days=90)
                elif time_range == '6M':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(days=180)
                elif time_range == '1Y':
                    cutoff = pd.Timestamp.now() - pd.Timedelta(days=365)
                else:  # All
                    return data
                
                filtered_data = data[data['Date'] >= cutoff]
                return filtered_data
            else:
                return data
        except Exception as e:
            logger.error(f"Failed to filter data by time: {e}")
            return data
    
    def process_candlestick_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data for candlestick charts"""
        try:
            if all(col in data.columns for col in ['Open', 'High', 'Low', 'Close']):
                return data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].copy()
            else:
                # Generate sample OHLC data if not available
                sample_data = pd.DataFrame({
                    'Date': pd.date_range('2024-01-01', periods=len(data), freq='D'),
                    'Open': np.random.normal(100, 20, len(data)),
                    'High': np.random.normal(105, 25, len(data)),
                    'Low': np.random.normal(95, 15, len(data)),
                    'Close': np.random.normal(100, 20, len(data)),
                    'Volume': np.random.randint(1000000, 10000000, len(data))
                })
                return sample_data
        except Exception as e:
            logger.error(f"Failed to process candlestick data: {e}")
            return data
    
    def process_line_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data for line charts"""
        try:
            # Find numeric columns for line chart
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                return data[['Date'] + list(numeric_cols[:3])].copy()
            else:
                return data
        except Exception as e:
            logger.error(f"Failed to process line data: {e}")
            return data
    
    def process_bar_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data for bar charts"""
        try:
            # Find categorical and numeric columns for bar chart
            categorical_cols = data.select_dtypes(include=['object']).columns
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            
            if len(categorical_cols) > 0 and len(numeric_cols) > 0:
                return data[list(categorical_cols[:2]) + list(numeric_cols[:2])].copy()
            else:
                return data
        except Exception as e:
            logger.error(f"Failed to process bar data: {e}")
            return data
    
    def process_scatter_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Process data for scatter plots"""
        try:
            # Find numeric columns for scatter plot
            numeric_cols = data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                return data[list(numeric_cols[:2])].copy()
            else:
                return data
        except Exception as e:
            logger.error(f"Failed to process scatter data: {e}")
            return data
