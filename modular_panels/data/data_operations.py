#!/usr/bin/env python3
"""
TradePulse Data Panel - Operations
Data processing operations for the data panel
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class DataOperations:
    """Data processing operations"""
    
    def create_sample_data(self) -> pd.DataFrame:
        """Create sample data for preview"""
        dates = pd.date_range(start='2024-12-25', end='2024-12-31', freq='D')
        data = []
        
        for date in dates:
            data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Open': 150.0 + np.random.normal(0, 2),
                'High': 155.0 + np.random.normal(0, 2),
                'Low': 145.0 + np.random.normal(0, 2),
                'Close': 152.0 + np.random.normal(0, 2),
                'Volume': int(1000000 + np.random.normal(0, 200000))
            })
        
        return pd.DataFrame(data)
    
    def update_statistics(self, data: pd.DataFrame, symbol: str, timeframe: str, source: str):
        """Update data statistics display with enhanced date range info"""
        if data is None or data.empty:
            return self.get_clear_statistics()
        
        try:
            # Calculate date range duration with proper error handling
            start_date = pd.to_datetime(data['Date'].iloc[0])
            end_date = pd.to_datetime(data['Date'].iloc[-1])
            
            # Handle NaT values
            if pd.isna(start_date) or pd.isna(end_date):
                duration_days = 0
                duration_str = "Unknown"
                frequency = "Unknown"
            else:
                duration_days = (end_date - start_date).days
            
            # Format duration
            if duration_days == 0:
                duration_str = "Unknown"
                frequency = "Unknown"
            elif duration_days > 365:
                years = duration_days // 365
                remaining_days = duration_days % 365
                duration_str = f"{years} year{'s' if years > 1 else ''}"
                if remaining_days > 0:
                    duration_str += f" {remaining_days} days"
            elif duration_days > 30:
                months = duration_days // 30
                remaining_days = duration_days % 30
                duration_str = f"{months} month{'s' if months > 1 else ''}"
                if remaining_days > 0:
                    duration_str += f" {remaining_days} days"
            else:
                duration_str = f"{duration_days} day{'s' if duration_days > 1 else ''}"
            
            # Calculate data frequency
            if duration_days == 0 or len(data) <= 1:
                frequency = "Unknown"
            else:
                avg_interval = duration_days / (len(data) - 1)
                if avg_interval < 1:
                    frequency = "Intraday"
                elif avg_interval == 1:
                    frequency = "Daily"
                elif avg_interval == 7:
                    frequency = "Weekly"
                elif avg_interval == 30:
                    frequency = "Monthly"
                else:
                    frequency = f"Every {avg_interval:.1f} days"
            
            # Format date range safely
            if pd.isna(start_date) or pd.isna(end_date):
                date_range = "Unknown"
            else:
                date_range = f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
            
            stats_text = f"""
            ### 📊 Data Statistics
            - **Total Records**: {len(data):,}
            - **Date Range**: {date_range}
            - **Duration**: {duration_str}
            - **Frequency**: {frequency}
            - **Symbol**: {symbol}
            - **Timeframe**: {timeframe}
            - **Source**: {source}
            - **Last Updated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            return stats_text
        except Exception as e:
            logger.error(f"Failed to update statistics: {e}")
            return self.get_clear_statistics()
    
    def get_clear_statistics(self) -> str:
        """Get statistics for cleared data"""
        return """
        ### 📊 Data Statistics
        - **Total Records**: 0
        - **Date Range**: None
        - **Symbols**: 0
        - **Last Updated**: Data cleared
        """
    
    def validate_data(self, data: pd.DataFrame) -> bool:
        """Validate data structure"""
        if data is None or data.empty:
            return False
        
        required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        return all(col in data.columns for col in required_columns)
    
    def get_data_summary(self, data: pd.DataFrame) -> Dict:
        """Get data summary statistics"""
        if data is None or data.empty:
            return {}
        
        try:
            return {
                'total_records': len(data),
                'date_range': f"{data['Date'].iloc[0]} to {data['Date'].iloc[-1]}",
                'columns': list(data.columns),
                'numeric_columns': data.select_dtypes(include=[np.number]).columns.tolist(),
                'missing_values': data.isnull().sum().to_dict()
            }
        except Exception as e:
            logger.error(f"Failed to get data summary: {e}")
            return {}
