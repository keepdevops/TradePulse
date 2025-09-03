#!/usr/bin/env python3
"""
TradePulse Data - Data Metrics (Refactored)
Handles data metrics calculations and analysis
Refactored to be under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from .data_metrics_core import DataMetricsCore

logger = logging.getLogger(__name__)

class DataMetrics:
    """Handles data metrics calculations and analysis"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_metrics = DataMetricsCore()
    
    def calculate_dataset_metrics(self, data: pd.DataFrame) -> Dict:
        """Calculate comprehensive metrics for a dataset"""
        # Delegate to refactored implementation
        return self._refactored_metrics.calculate_dataset_metrics(data)
    
    def get_metrics_history(self) -> List[Dict]:
        """Get metrics calculation history"""
        # Delegate to refactored implementation
        return self._refactored_metrics.get_metrics_history()
    
    def get_metrics_statistics(self) -> Dict:
        """Get metrics calculation statistics"""
        # Delegate to refactored implementation
        return self._refactored_metrics.get_metrics_statistics()
    
    def clear_metrics_history(self) -> int:
        """Clear metrics history and return count"""
        # Delegate to refactored implementation
        return self._refactored_metrics.clear_metrics_history()
    
    def get_metrics_summary(self, data: pd.DataFrame) -> str:
        """Get metrics summary for display"""
        # Delegate to refactored implementation
        return self._refactored_metrics.get_metrics_summary(data)
    
    def validate_data_for_metrics(self, data: pd.DataFrame) -> bool:
        """Validate data for metrics calculation"""
        # Delegate to refactored implementation
        return self._refactored_metrics.validate_data_for_metrics(data)
    
    def get_metrics_report(self, data: pd.DataFrame) -> Dict:
        """Get comprehensive metrics report"""
        # Delegate to refactored implementation
        return self._refactored_metrics.get_metrics_report(data)



