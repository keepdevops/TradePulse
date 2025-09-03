#!/usr/bin/env python3
"""
TradePulse Data - Main Data Manager
Refactored data manager using focused components
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json

from .dataset_registry import DatasetRegistry
from .data_processor import DataProcessor
from .data_metrics import DataMetrics

logger = logging.getLogger(__name__)

class DataManager:
    """Refactored data manager using focused components"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.portfolio_data = {}
        self.ml_predictions = {}
        self.alerts = []
        self.orders = []
        
        # Initialize focused components
        self.dataset_registry = DatasetRegistry()
        self.data_processor = DataProcessor()
        self.data_metrics = DataMetrics()
        
        # Enhanced data storage for uploaded files
        self.uploaded_datasets = {}  # Store uploaded data with metadata
        
        self.load_initial_data()
        logger.info("📊 Refactored DataManager initialized with focused components")
    
    def load_initial_data(self):
        """Load initial data for the system"""
        logger.info("📊 Loading initial data...")
        
        # Generate sample price data
        for symbol in self.symbols:
            self.price_data[symbol] = self.generate_sample_price_data(symbol)
        
        # Generate sample portfolio data
        self.portfolio_data = self.generate_sample_portfolio_data()
        
        # Generate sample ML predictions
        self.ml_predictions = self.generate_sample_ml_predictions()
        
        logger.info("✅ Initial data loaded successfully")
    
    def add_uploaded_data(self, key: str, data: pd.DataFrame, metadata: Optional[Dict] = None) -> str:
        """Add uploaded data to the data manager for use by all modules"""
        try:
            # Generate unique dataset ID
            dataset_id = f"dataset_{key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Store the data with metadata
            self.uploaded_datasets[dataset_id] = {
                'data': data.copy(),
                'metadata': metadata or {},
                'upload_time': datetime.now(),
                'shape': data.shape,
                'columns': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum(),
                'access_count': 0,
                'last_accessed': datetime.now()
            }
            
            # Register dataset using dataset registry
            self.dataset_registry.register_dataset(dataset_id, key, 'uploaded')
            
            # Process data using data processor
            processed_data = self.data_processor.process_uploaded_data(data, metadata)
            
            # Calculate metrics using data metrics
            metrics = self.data_metrics.calculate_dataset_metrics(data)
            
            logger.info(f"✅ Uploaded data added: {dataset_id} ({data.shape[0]} rows, {data.shape[1]} cols)")
            return dataset_id
            
        except Exception as e:
            logger.error(f"❌ Failed to add uploaded data: {e}")
            raise
    
    def get_dataset(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset by ID"""
        if dataset_id in self.uploaded_datasets:
            # Update access statistics
            self.uploaded_datasets[dataset_id]['access_count'] += 1
            self.uploaded_datasets[dataset_id]['last_accessed'] = datetime.now()
            
            # Validate access using dataset registry
            if self.dataset_registry.validate_dataset_access(dataset_id, 'system'):
                return self.uploaded_datasets[dataset_id]['data']
            else:
                logger.warning(f"Access denied to dataset: {dataset_id}")
                return None
        return None
    
    def get_available_datasets(self, module: str = None) -> List[Dict]:
        """Get available datasets for a specific module or all modules"""
        if module:
            return self.dataset_registry.get_datasets_for_module(module)
        else:
            return self.dataset_registry.get_all_datasets()
    
    def get_dataset_info(self, dataset_id: str) -> Optional[Dict]:
        """Get dataset information"""
        return self.dataset_registry.get_dataset_info(dataset_id)
    
    def get_dataset_metrics(self, dataset_id: str) -> Dict:
        """Get metrics for a specific dataset"""
        if dataset_id in self.uploaded_datasets:
            data = self.uploaded_datasets[dataset_id]['data']
            return self.data_metrics.calculate_dataset_metrics(data)
        return {}
    
    def get_all_dataset_metrics(self) -> Dict:
        """Get metrics for all datasets"""
        all_metrics = {}
        for dataset_id in self.uploaded_datasets:
            all_metrics[dataset_id] = self.get_dataset_metrics(dataset_id)
        return all_metrics
    
    def search_datasets(self, query: str) -> List[Dict]:
        """Search datasets by query"""
        return self.dataset_registry.search_datasets(query)
    
    def get_data_statistics(self) -> Dict:
        """Get comprehensive data statistics"""
        try:
            # Get registry statistics
            registry_stats = self.dataset_registry.get_registry_statistics()
            
            # Get data metrics
            data_metrics = self.get_all_dataset_metrics()
            
            # Calculate total data volume
            total_rows = sum(metrics.get('row_count', 0) for metrics in data_metrics.values())
            total_columns = sum(metrics.get('column_count', 0) for metrics in data_metrics.values())
            total_memory = sum(metrics.get('memory_usage_mb', 0) for metrics in data_metrics.values())
            
            return {
                'registry': registry_stats,
                'data_volume': {
                    'total_datasets': len(self.uploaded_datasets),
                    'total_rows': total_rows,
                    'total_columns': total_columns,
                    'total_memory_mb': total_memory
                },
                'data_metrics': data_metrics
            }
            
        except Exception as e:
            logger.error(f"Failed to get data statistics: {e}")
            return {}
    
    def clear_dataset(self, dataset_id: str) -> bool:
        """Clear a specific dataset"""
        try:
            if dataset_id in self.uploaded_datasets:
                del self.uploaded_datasets[dataset_id]
                self.dataset_registry.unregister_dataset(dataset_id)
                logger.info(f"✅ Dataset cleared: {dataset_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to clear dataset: {e}")
            return False
    
    def clear_all_datasets(self) -> int:
        """Clear all datasets and return count"""
        try:
            count = len(self.uploaded_datasets)
            self.uploaded_datasets.clear()
            self.dataset_registry.clear_registry()
            logger.info(f"🗑️ Cleared {count} datasets")
            return count
        except Exception as e:
            logger.error(f"Failed to clear all datasets: {e}")
            return 0
    
    # Legacy methods for backward compatibility
    def generate_sample_price_data(self, symbol: str) -> pd.DataFrame:
        """Generate sample price data for a symbol"""
        try:
            dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
            np.random.seed(hash(symbol) % 2**32)
            
            # Generate realistic price data
            base_price = 100 + np.random.uniform(50, 200)
            returns = np.random.normal(0, 0.02, len(dates))
            prices = [base_price]
            
            for ret in returns[1:]:
                new_price = prices[-1] * (1 + ret)
                prices.append(max(new_price, 1))  # Ensure price doesn't go below 1
            
            data = pd.DataFrame({
                'Date': dates,
                'Open': [p * (1 + np.random.uniform(-0.01, 0.01)) for p in prices],
                'High': [p * (1 + np.random.uniform(0, 0.02)) for p in prices],
                'Low': [p * (1 - np.random.uniform(0, 0.02)) for p in prices],
                'Close': prices,
                'Volume': np.random.randint(1000000, 10000000, len(dates))
            })
            
            return data
            
        except Exception as e:
            logger.error(f"Failed to generate sample price data for {symbol}: {e}")
            return pd.DataFrame()
    
    def generate_sample_portfolio_data(self) -> Dict:
        """Generate sample portfolio data"""
        try:
            return {
                'total_value': 100000.0,
                'cash': 25000.0,
                'positions': {
                    'AAPL': {'shares': 100, 'avg_price': 150.0, 'current_price': 155.0},
                    'GOOGL': {'shares': 50, 'avg_price': 2800.0, 'current_price': 2850.0}
                },
                'performance': {
                    'daily_return': 0.02,
                    'weekly_return': 0.08,
                    'monthly_return': 0.15,
                    'yearly_return': 0.25,
                    'total_return': 0.25
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate sample portfolio data: {e}")
            return {}
    
    def generate_sample_ml_predictions(self) -> Dict:
        """Generate sample ML predictions"""
        try:
            return {
                'AAPL': {
                    'next_day': 156.5,
                    'next_week': 158.2,
                    'next_month': 162.0,
                    'confidence': 0.85
                },
                'GOOGL': {
                    'next_day': 2860.0,
                    'next_week': 2880.0,
                    'next_month': 2920.0,
                    'confidence': 0.78
                }
            }
        except Exception as e:
            logger.error(f"Failed to generate sample ML predictions: {e}")
            return {}
    
    def get_price_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Get price data for a symbol"""
        return self.price_data.get(symbol)
    
    def get_portfolio_data(self) -> Dict:
        """Get portfolio data"""
        return self.portfolio_data.copy()
    
    def get_ml_predictions(self) -> Dict:
        """Get ML predictions"""
        return self.ml_predictions.copy()
