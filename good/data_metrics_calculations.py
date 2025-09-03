#!/usr/bin/env python3
"""
TradePulse Data Metrics - Calculations
Metric calculations for the data metrics
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class DataMetricsCalculations:
    """Metric calculations for data metrics"""
    
    def calculate_basic_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate basic dataset metrics"""
        try:
            return {
                'row_count': len(data),
                'column_count': len(data.columns),
                'total_cells': len(data) * len(data.columns),
                'data_types': data.dtypes.to_dict(),
                'column_names': data.columns.tolist(),
                'index_type': str(type(data.index)),
                'has_duplicates': data.duplicated().any(),
                'duplicate_count': data.duplicated().sum()
            }
        except Exception as e:
            logger.error(f"Failed to calculate basic metrics: {e}")
            return {}
    
    def calculate_statistical_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate statistical metrics for numeric columns"""
        try:
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            categorical_columns = data.select_dtypes(include=['object']).columns
            
            stats = {
                'numeric_columns': len(numeric_columns),
                'categorical_columns': len(categorical_columns),
                'numeric_column_names': numeric_columns.tolist(),
                'categorical_column_names': categorical_columns.tolist()
            }
            
            # Calculate statistics for numeric columns
            if len(numeric_columns) > 0:
                numeric_stats = {}
                for col in numeric_columns:
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        numeric_stats[col] = {
                            'mean': float(col_data.mean()),
                            'median': float(col_data.median()),
                            'std': float(col_data.std()),
                            'min': float(col_data.min()),
                            'max': float(col_data.max()),
                            'q25': float(col_data.quantile(0.25)),
                            'q75': float(col_data.quantile(0.75)),
                            'skewness': float(col_data.skew()),
                            'kurtosis': float(col_data.kurtosis())
                        }
                
                stats['numeric_statistics'] = numeric_stats
            
            # Calculate statistics for categorical columns
            if len(categorical_columns) > 0:
                categorical_stats = {}
                for col in categorical_columns:
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        value_counts = col_data.value_counts()
                        categorical_stats[col] = {
                            'unique_values': int(value_counts.nunique()),
                            'most_common': value_counts.index[0] if len(value_counts) > 0 else None,
                            'most_common_count': int(value_counts.iloc[0]) if len(value_counts) > 0 else 0,
                            'least_common': value_counts.index[-1] if len(value_counts) > 0 else None,
                            'least_common_count': int(value_counts.iloc[-1]) if len(value_counts) > 0 else 0
                        }
                
                stats['categorical_statistics'] = categorical_stats
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to calculate statistical metrics: {e}")
            return {}
    
    def calculate_quality_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate data quality metrics"""
        try:
            quality_metrics = {}
            
            # Missing value analysis
            missing_counts = data.isnull().sum()
            total_missing = missing_counts.sum()
            total_cells = len(data) * len(data.columns)
            
            quality_metrics['missing_values'] = {
                'total_missing': int(total_missing),
                'missing_percentage': float(total_missing / total_cells * 100) if total_cells > 0 else 0.0,
                'columns_with_missing': missing_counts[missing_counts > 0].to_dict(),
                'complete_rows': int((data.notna().all(axis=1)).sum()),
                'complete_columns': int((data.notna().all(axis=0)).sum())
            }
            
            # Data consistency checks
            quality_metrics['consistency'] = {
                'has_constant_columns': bool((data.nunique() == 1).any()),
                'constant_columns': data.columns[data.nunique() == 1].tolist(),
                'has_single_value_columns': bool((data.nunique() == 1).any()),
                'single_value_columns': data.columns[data.nunique() == 1].tolist()
            }
            
            # Data range checks for numeric columns
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) > 0:
                range_checks = {}
                for col in numeric_columns:
                    col_data = data[col].dropna()
                    if len(col_data) > 0:
                        range_checks[col] = {
                            'has_negative_values': bool((col_data < 0).any()),
                            'has_zero_values': bool((col_data == 0).any()),
                            'has_extreme_values': bool((col_data > col_data.mean() + 3 * col_data.std()).any())
                        }
                
                quality_metrics['range_checks'] = range_checks
            
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Failed to calculate quality metrics: {e}")
            return {}
    
    def calculate_memory_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate memory usage metrics"""
        try:
            memory_usage = data.memory_usage(deep=True)
            total_memory = memory_usage.sum()
            
            return {
                'memory_usage_bytes': int(total_memory),
                'memory_usage_mb': float(total_memory / (1024 * 1024)),
                'memory_usage_kb': float(total_memory / 1024),
                'memory_per_row_bytes': float(total_memory / len(data)) if len(data) > 0 else 0.0,
                'memory_per_column_bytes': float(total_memory / len(data.columns)) if len(data.columns) > 0 else 0.0,
                'column_memory_usage': memory_usage.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate memory metrics: {e}")
            return {}
    
    def create_empty_metrics(self) -> Dict:
        """Create empty metrics structure"""
        return {
            'row_count': 0,
            'column_count': 0,
            'total_cells': 0,
            'data_types': {},
            'column_names': [],
            'index_type': '',
            'has_duplicates': False,
            'duplicate_count': 0,
            'numeric_columns': 0,
            'categorical_columns': 0,
            'missing_values': {
                'total_missing': 0,
                'missing_percentage': 0.0,
                'columns_with_missing': {},
                'complete_rows': 0,
                'complete_columns': 0
            },
            'memory_usage_bytes': 0,
            'memory_usage_mb': 0.0
        }

