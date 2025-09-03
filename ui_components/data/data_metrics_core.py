#!/usr/bin/env python3
"""
TradePulse Data Metrics - Core Functionality
Core data metrics class with basic functionality
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from .data_metrics_components import DataMetricsComponents
from .data_metrics_operations import DataMetricsOperations
from .data_metrics_management import DataMetricsManagement
from .data_metrics_calculations import DataMetricsCalculations

logger = logging.getLogger(__name__)

class DataMetricsCore:
    """Core data metrics functionality"""
    
    def __init__(self):
        self.metrics_history = []
        
        # Initialize components
        self.components = DataMetricsComponents()
        self.operations = DataMetricsOperations()
        self.management = DataMetricsManagement()
        self.calculations = DataMetricsCalculations()
    
    def calculate_dataset_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive metrics for a dataset"""
        try:
            if data.empty:
                return self.calculations.create_empty_metrics()
            
            logger.info(f"📊 Calculating metrics for dataset: {data.shape[0]} rows, {data.shape[1]} columns")
            
            # Calculate all metric types
            basic_metrics = self.calculations.calculate_basic_metrics(data)
            statistical_metrics = self.calculations.calculate_statistical_metrics(data)
            quality_metrics = self.calculations.calculate_quality_metrics(data)
            memory_metrics = self.calculations.calculate_memory_metrics(data)
            
            # Combine all metrics
            all_metrics = {
                **basic_metrics,
                **statistical_metrics,
                **quality_metrics,
                **memory_metrics
            }
            
            # Record metrics calculation
            self.operations.record_metrics_calculation(self.metrics_history, data.shape, all_metrics)
            
            logger.info("✅ Dataset metrics calculated successfully")
            return all_metrics
            
        except Exception as e:
            logger.error(f"❌ Failed to calculate dataset metrics: {e}")
            return self.calculations.create_empty_metrics()
    
    def get_metrics_history(self) -> List[Dict]:
        """Get metrics calculation history"""
        return self.metrics_history.copy()
    
    def get_metrics_statistics(self) -> Dict:
        """Get metrics calculation statistics"""
        return self.operations.get_metrics_statistics(self.metrics_history)
    
    def clear_metrics_history(self) -> int:
        """Clear metrics history and return count"""
        return self.operations.clear_metrics_history(self.metrics_history)
    
    def get_metrics_summary(self, data: pd.DataFrame) -> str:
        """Get metrics summary for display"""
        metrics = self.calculate_dataset_metrics(data)
        return self.management.create_metrics_summary(metrics)
    
    def validate_data_for_metrics(self, data: pd.DataFrame) -> bool:
        """Validate data for metrics calculation"""
        return self.operations.validate_data_for_metrics(data)
    
    def get_metrics_report(self, data: pd.DataFrame) -> Dict:
        """Get comprehensive metrics report"""
        metrics = self.calculate_dataset_metrics(data)
        return self.management.create_metrics_report(metrics, data)



