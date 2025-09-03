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
        """Update data statistics display"""
        if data is None or data.empty:
            return self.get_clear_statistics()
        
        try:
            stats_text = f"""
            ### 📊 Data Statistics
            - **Total Records**: {len(data)}
            - **Date Range**: {data['Date'].iloc[0]} to {data['Date'].iloc[-1]}
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
