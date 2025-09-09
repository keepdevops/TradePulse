#!/usr/bin/env python3
"""
TradePulse Dataset Browser - History
History management for dataset browser
"""

import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class DatasetBrowserHistory:
    """History management for dataset browser"""
    
    def __init__(self, core_browser):
        self.core = core_browser
    
    def _record_search(self, query: str):
        """Record search operation"""
        try:
            search_record = {
                'timestamp': pd.Timestamp.now(),
                'query': query,
                'module': self.core.module_name
            }
            self.core.search_history.append(search_record)
            
        except Exception as e:
            logger.error(f"Failed to record search: {e}")
    
    def _record_filter(self, filter_type: str):
        """Record filter operation"""
        try:
            filter_record = {
                'timestamp': pd.Timestamp.now(),
                'filter_type': filter_type,
                'module': self.core.module_name
            }
            self.core.filter_history.append(filter_record)
            
        except Exception as e:
            logger.error(f"Failed to record filter: {e}")
    
    def get_search_history(self) -> List[Dict]:
        """Get search history"""
        return self.core.search_history.copy()
    
    def get_filter_history(self) -> List[Dict]:
        """Get filter history"""
        return self.core.filter_history.copy()
    
    def get_browser_statistics(self) -> Dict:
        """Get browser statistics"""
        try:
            return {
                'total_searches': len(self.core.search_history),
                'total_filters': len(self.core.filter_history),
                'available_datasets': len(self.core.data_manager.get_available_datasets(self.core.module_name)),
                'last_search': self.core.search_history[-1]['timestamp'] if self.core.search_history else None,
                'last_filter': self.core.filter_history[-1]['timestamp'] if self.core.filter_history else None
            }
        except Exception as e:
            logger.error(f"Failed to get browser statistics: {e}")
            return {}
    
    def clear_history(self) -> int:
        """Clear search and filter history"""
        try:
            search_count = len(self.core.search_history)
            filter_count = len(self.core.filter_history)
            
            self.core.search_history.clear()
            self.core.filter_history.clear()
            
            logger.info(f"🗑️ Cleared {search_count} searches and {filter_count} filters")
            return search_count + filter_count
            
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
            return 0
