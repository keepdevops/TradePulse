#!/usr/bin/env python3
"""
TradePulse Data Manager - Operations
Data management operations including cleanup, export, and sample data generation
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class DataManagerOps:
    """Data management operations"""
    
    def __init__(self, core_manager):
        self.core = core_manager
    
    def cleanup_old_datasets(self, days_old: int = 30) -> int:
        """Clean up datasets older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        datasets_to_remove = []
        
        for dataset_id, info in self.core.uploaded_datasets.items():
            if info['upload_time'] < cutoff_date:
                datasets_to_remove.append(dataset_id)
        
        # Remove old datasets
        for dataset_id in datasets_to_remove:
            del self.core.uploaded_datasets[dataset_id]
            if dataset_id in self.core.dataset_registry:
                del self.core.dataset_registry[dataset_id]
            
            # Remove from active datasets
            for module_name in self.core.active_datasets:
                if dataset_id in self.core.active_datasets[module_name]:
                    del self.core.active_datasets[module_name][dataset_id]
        
        logger.info(f"🧹 Cleaned up {len(datasets_to_remove)} old datasets")
        return len(datasets_to_remove)
    
    def export_dataset(self, dataset_id: str, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        if dataset_id not in self.core.uploaded_datasets:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        data = self.core.uploaded_datasets[dataset_id]['data']
        
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"export_{dataset_id}_{timestamp}"
        
        try:
            if format.lower() == 'csv':
                data.to_csv(f"{filepath}.csv", index=False)
            elif format.lower() == 'json':
                data.to_json(f"{filepath}.json", orient='records')
            elif format.lower() == 'excel':
                data.to_excel(f"{filepath}.xlsx", index=False)
            elif format.lower() == 'feather':
                data.to_feather(f"{filepath}.feather")
            elif format.lower() == 'parquet':
                data.to_parquet(f"{filepath}.parquet")
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            logger.info(f"✅ Dataset {dataset_id} exported to {filepath}.{format}")
            return f"{filepath}.{format}"
            
        except Exception as e:
            logger.error(f"❌ Failed to export dataset {dataset_id}: {e}")
            raise
    
    def generate_sample_price_data(self, symbol: str) -> pd.DataFrame:
        """Generate sample price data for a symbol"""
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = []
        
        for date in dates:
            base_price = 100 + np.random.normal(0, 20)
            data.append({
                'Date': date,
                'Open': base_price + np.random.normal(0, 2),
                'High': base_price + np.random.normal(2, 3),
                'Low': base_price + np.random.normal(-2, 3),
                'Close': base_price + np.random.normal(0, 2),
                'Volume': int(1000000 + np.random.normal(0, 200000))
            })
        
        return pd.DataFrame(data)
    
    def generate_sample_portfolio_data(self) -> Dict[str, Any]:
        """Generate sample portfolio data"""
        return {
            'total_value': 100000,
            'positions': {
                'AAPL': {'shares': 100, 'avg_price': 150, 'current_price': 155},
                'GOOGL': {'shares': 50, 'avg_price': 2800, 'current_price': 2850}
            },
            'performance': {
                'daily_return': 0.02,
                'monthly_return': 0.15,
                'yearly_return': 0.25
            }
        }
    
    def generate_sample_ml_predictions(self) -> Dict[str, Any]:
        """Generate sample ML predictions"""
        return {
            'AAPL': {'prediction': 160, 'confidence': 0.85, 'model': 'ADM'},
            'GOOGL': {'prediction': 2900, 'confidence': 0.78, 'model': 'CIPO'},
            'MSFT': {'prediction': 400, 'confidence': 0.92, 'model': 'BICIPO'}
        }
    
    def get_price_data(self, symbol: str = None) -> Dict[str, pd.DataFrame]:
        """Get price data for symbols"""
        if symbol:
            return {symbol: self.core.price_data.get(symbol, pd.DataFrame())}
        return self.core.price_data
    
    def get_price_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        """Get price data for a specific symbol as DataFrame"""
        return self.core.price_data.get(symbol, pd.DataFrame())
    
    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get portfolio data"""
        return self.core.portfolio_data
    
    def get_ml_predictions(self) -> Dict[str, Any]:
        """Get ML predictions"""
        return self.core.ml_predictions
    
    def update_price_data(self, symbol: str, new_data: pd.DataFrame):
        """Update price data for a symbol"""
        self.core.price_data[symbol] = new_data
        logger.info(f"📊 Price data updated for {symbol}")
