#!/usr/bin/env python3
"""
TradePulse UI Data Manager
Enhanced data manager with upload support for all modules
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime, timedelta
import json
from .global_data_store import get_global_data_store

logger = logging.getLogger(__name__)

class DataManager:
    """Enhanced data manager for the UI with upload support"""
    
    def __init__(self):
        self.symbols = ["AAPL", "GOOGL", "MSFT", "TSLA", "AMZN", "NVDA", "META", "NFLX"]
        self.price_data = {}
        self.portfolio_data = {}
        self.ml_predictions = {}
        self.alerts = []
        self.orders = []
        
        # Use global data store for uploaded datasets to ensure persistence across instances
        self.global_store = get_global_data_store()
        
        # Local references to global data for backward compatibility
        # These will now reference the global store
        self._uploaded_datasets = None  # Will be replaced by property
        self.dataset_registry = {}   # Registry of available datasets
        self.active_datasets = {}    # Currently active datasets for each module
        
        # Module-specific data access
        self.module_data_access = {
            'portfolio': ['price_data', 'uploaded_datasets'],
            'models': ['price_data', 'uploaded_datasets'],
            'ai': ['price_data', 'uploaded_datasets', 'ml_predictions'],
            'charts': ['price_data', 'uploaded_datasets'],
            'alerts': ['price_data', 'uploaded_datasets', 'alerts'],
            'system': ['uploaded_datasets', 'system_metrics']
        }
        
        self.load_initial_data()
        logger.info("📊 Enhanced DataManager initialized with upload support")
    
    @property
    def uploaded_datasets(self):
        """Access uploaded datasets from global store"""
        return self.global_store.uploaded_datasets
    
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
        """Add uploaded data to the global store for use by all modules across all instances"""
        try:
            # Generate unique dataset ID
            dataset_id = f"dataset_{key}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Prepare metadata with enhanced information
            enhanced_metadata = {
                **(metadata or {}),
                'upload_time': datetime.now(),
                'shape': data.shape,
                'columns': data.columns.tolist(),
                'dtypes': data.dtypes.to_dict(),
                'memory_usage': data.memory_usage(deep=True).sum(),
                'access_count': 0,
                'last_accessed': datetime.now()
            }
            
            # Add to global store (this will be shared across all DataManager instances)
            success = self.global_store.add_uploaded_data(dataset_id, data, enhanced_metadata)
            
            if success:
                # Add to local dataset registry for this instance
                self.dataset_registry[dataset_id] = {
                    'name': key,
                    'type': 'uploaded',
                    'available': True,
                    'modules': list(self.module_data_access.keys())
                }
                
                logger.info(f"✅ Uploaded data added: {dataset_id} ({data.shape[0]} rows, {data.shape[1]} cols)")
                return dataset_id
            else:
                raise Exception("Failed to add data to global store")
            
        except Exception as e:
            logger.error(f"❌ Failed to add uploaded data: {e}")
            raise
    
    def get_dataset(self, dataset_id: str) -> Optional[pd.DataFrame]:
        """Get a specific dataset by ID from global store"""
        # Get data from global store
        datasets = self.global_store.get_uploaded_data(dataset_id)
        if dataset_id in datasets:
            return datasets[dataset_id]
        return None
    
    def get_available_datasets(self, module_name: str = None) -> Dict[str, Any]:
        """Get available datasets for a specific module or all modules from global store"""
        # Get available datasets from global store
        return self.global_store.get_available_datasets(module_name)
    
    def activate_dataset_for_module(self, dataset_id: str, module_name: str) -> bool:
        """Activate a dataset for use by a specific module"""
        try:
            # Get dataset from global store
            datasets = self.global_store.get_uploaded_data(dataset_id)
            if dataset_id in datasets:
                if module_name not in self.active_datasets:
                    self.active_datasets[module_name] = {}
                
                data = datasets[dataset_id]
                self.active_datasets[module_name][dataset_id] = {
                    'activated_time': datetime.now(),
                    'data_shape': data.shape
                }
                
                logger.info(f"✅ Dataset {dataset_id} activated for {module_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Failed to activate dataset {dataset_id} for {module_name}: {e}")
            return False
    
    def get_active_datasets_for_module(self, module_name: str) -> Dict[str, pd.DataFrame]:
        """Get all active datasets for a specific module"""
        active_data = {}
        if module_name in self.active_datasets:
            for dataset_id in self.active_datasets[module_name]:
                # Get data from global store
                datasets = self.global_store.get_uploaded_data(dataset_id)
                if dataset_id in datasets:
                    active_data[dataset_id] = datasets[dataset_id].copy()
        return active_data
    
    def get_data_for_module(self, module_name: str, data_type: str = 'all') -> Dict[str, Any]:
        """Get all relevant data for a specific module"""
        module_data = {}
        
        if module_name in self.module_data_access:
            allowed_data_types = self.module_data_access[module_name]
            
            for data_type_name in allowed_data_types:
                if data_type == 'all' or data_type == data_type_name:
                    if data_type_name == 'price_data':
                        module_data['price_data'] = self.price_data
                    elif data_type_name == 'uploaded_datasets':
                        module_data['uploaded_datasets'] = self.get_active_datasets_for_module(module_name)
                    elif data_type_name == 'ml_predictions':
                        module_data['ml_predictions'] = self.ml_predictions
                    elif data_type_name == 'alerts':
                        module_data['alerts'] = self.alerts
                    elif data_type_name == 'portfolio_data':
                        module_data['portfolio_data'] = self.portfolio_data
        
        return module_data
    
    def search_datasets(self, query: str, module_name: str = None) -> Dict[str, Any]:
        """Search datasets by name, columns, or content"""
        results = {}
        query_lower = query.lower()
        
        # Get available datasets from global store
        available_datasets = self.global_store.get_available_datasets(module_name)
        
        for dataset_id, metadata in available_datasets.items():
            # Check if dataset is available for the module
            if module_name and dataset_id in self.dataset_registry:
                if module_name not in self.dataset_registry[dataset_id]['modules']:
                    continue
            
            # Search in dataset name
            if query_lower in metadata.get('name', '').lower():
                results[dataset_id] = metadata
                continue
            
            # Search in column names
            if 'columns' in metadata and any(query_lower in col.lower() for col in metadata['columns']):
                results[dataset_id] = metadata
                continue
            
            # Search in metadata
            if query_lower in str(metadata).lower():
                results[dataset_id] = metadata
                continue
        
        return results
    
    def get_dataset_statistics(self) -> Dict[str, Any]:
        """Get comprehensive statistics about all datasets"""
        # Get available datasets from global store
        available_datasets = self.global_store.get_available_datasets()
        uploaded_data = self.global_store.get_uploaded_data()
        
        stats = {
            'total_datasets': len(available_datasets),
            'total_rows': sum(data.shape[0] for data in uploaded_data.values()),
            'total_columns': sum(data.shape[1] for data in uploaded_data.values()),
            'total_memory': sum(metadata.get('memory_usage', 0) for metadata in available_datasets.values()),
            'dataset_types': {},
            'module_usage': {module: len(self.active_datasets.get(module, {})) for module in self.module_data_access.keys()}
        }
        
        # Count dataset types
        for metadata in available_datasets.values():
            dataset_type = metadata.get('type', 'unknown')
            stats['dataset_types'][dataset_type] = stats['dataset_types'].get(dataset_type, 0) + 1
        
        return stats
    
    def cleanup_old_datasets(self, days_old: int = 30) -> int:
        """Clean up datasets older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        datasets_to_remove = []
        
        for dataset_id, info in self.uploaded_datasets.items():
            if info['upload_time'] < cutoff_date:
                datasets_to_remove.append(dataset_id)
        
        # Remove old datasets
        for dataset_id in datasets_to_remove:
            del self.uploaded_datasets[dataset_id]
            if dataset_id in self.dataset_registry:
                del self.dataset_registry[dataset_id]
            
            # Remove from active datasets
            for module_name in self.active_datasets:
                if dataset_id in self.active_datasets[module_name]:
                    del self.active_datasets[module_name][dataset_id]
        
        logger.info(f"🧹 Cleaned up {len(datasets_to_remove)} old datasets")
        return len(datasets_to_remove)
    
    def export_dataset(self, dataset_id: str, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        if dataset_id not in self.uploaded_datasets:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        data = self.uploaded_datasets[dataset_id]['data']
        
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
    
    # Existing methods for backward compatibility
    def get_price_data(self, symbol: str = None) -> Dict[str, pd.DataFrame]:
        """Get price data for symbols"""
        if symbol:
            return {symbol: self.price_data.get(symbol, pd.DataFrame())}
        return self.price_data
    
    def get_price_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        """Get price data for a specific symbol as DataFrame"""
        return self.price_data.get(symbol, pd.DataFrame())
    
    def get_portfolio_data(self) -> Dict[str, Any]:
        """Get portfolio data"""
        return self.portfolio_data
    
    def get_ml_predictions(self) -> Dict[str, Any]:
        """Get ML predictions"""
        return self.ml_predictions
    
    def update_price_data(self, symbol: str, new_data: pd.DataFrame):
        """Update price data for a symbol"""
        self.price_data[symbol] = new_data
        logger.info(f"📊 Price data updated for {symbol}")
    
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
