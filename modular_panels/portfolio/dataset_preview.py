#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Preview
Handles dataset preview, information display, and metadata
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any
import logging

from .dataset_preview_core import dataset_preview_core
from .dataset_preview_stats import DatasetPreviewStats

logger = logging.getLogger(__name__)

class DatasetPreview:
    """Handles dataset preview, information display, and metadata"""
    
    def __init__(self, data_manager):
        self.core = dataset_preview_core
        self.core.data_manager = data_manager
        self.stats = DatasetPreviewStats(self.core)
        
        # Update core methods to use stats module
        self.core._update_statistics_display = self.stats._update_statistics_display
        self.core._record_preview = self.stats._record_preview
    
    def update_preview(self, dataset_id: str):
        """Update preview for the specified dataset"""
        return self.core.update_preview(dataset_id)
    
    def get_current_dataset_id(self) -> Optional[str]:
        """Get the currently previewed dataset ID"""
        return self.core.get_current_dataset_id()
    
    def get_preview_history(self) -> List[Dict]:
        """Get preview history"""
        return self.stats.get_preview_history()
    
    def get_preview_statistics(self) -> Dict:
        """Get preview statistics"""
        return self.stats.get_preview_statistics()
    
    def clear_preview_history(self) -> int:
        """Clear preview history and return count"""
        return self.stats.clear_preview_history()
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return self.core.get_components()
