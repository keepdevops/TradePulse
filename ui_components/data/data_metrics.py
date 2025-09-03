#!/usr/bin/env python3
"""
TradePulse Data - Data Metrics
Handles data metrics calculations and analysis
REFACTORED: Now uses modular components to stay under 200 lines
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

from .data_metrics_refactored import DataMetrics as RefactoredDataMetrics

logger = logging.getLogger(__name__)

class DataMetrics:
    """Handles data metrics calculations and analysis"""
    
    def __init__(self):
        # Use the refactored implementation
        self._refactored_metrics = RefactoredDataMetrics()
    
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
