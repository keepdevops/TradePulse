#!/usr/bin/env python3
"""
TradePulse Dataset Preview - Statistics
Statistics calculation and history management for dataset preview
"""

import pandas as pd
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class DatasetPreviewStats:
    """Statistics calculation and history management for dataset preview"""
    
    def __init__(self, core_preview):
        self.core = core_preview
    
    def _update_statistics_display(self, dataset_data: pd.DataFrame):
        """Update the statistics display"""
        try:
            if dataset_data is None or dataset_data.empty:
                self.core.statistics_display.object = "**Statistics:** No data available"
                return
            
            # Calculate basic statistics
            numeric_columns = dataset_data.select_dtypes(include=['number']).columns.tolist()
            categorical_columns = dataset_data.select_dtypes(include=['object', 'category']).columns.tolist()
            
            stats_text = f"""
            **Statistics:**
            - **Total Rows:** {len(dataset_data):,}
            - **Total Columns:** {len(dataset_data.columns)}
            - **Numeric Columns:** {len(numeric_columns)}
            - **Categorical Columns:** {len(categorical_columns)}
            - **Memory Usage:** {dataset_data.memory_usage(deep=True).sum() / (1024*1024):.2f} MB
            """
            
            # Add column statistics
            if len(numeric_columns) > 0:
                stats_text += f"\n**Numeric Columns:** {', '.join(numeric_columns[:5])}"
                if len(numeric_columns) > 5:
                    stats_text += f" (+{len(numeric_columns) - 5} more)"
            
            if len(categorical_columns) > 0:
                stats_text += f"\n**Categorical Columns:** {', '.join(categorical_columns[:5])}"
                if len(categorical_columns) > 5:
                    stats_text += f" (+{len(categorical_columns) - 5} more)"
            
            self.core.statistics_display.object = stats_text
            
        except Exception as e:
            logger.error(f"Failed to update statistics display: {e}")
            self.core.statistics_display.object = "**Statistics:** Error calculating statistics"
    
    def _record_preview(self, dataset_id: str, shape: tuple):
        """Record preview operation"""
        try:
            preview_record = {
                'timestamp': pd.Timestamp.now(),
                'dataset_id': dataset_id,
                'shape': shape,
                'rows': shape[0],
                'columns': shape[1]
            }
            self.core.preview_history.append(preview_record)
            
        except Exception as e:
            logger.error(f"Failed to record preview: {e}")
    
    def get_preview_history(self) -> List[Dict]:
        """Get preview history"""
        return self.core.preview_history.copy()
    
    def get_preview_statistics(self) -> Dict:
        """Get preview statistics"""
        try:
            if not self.core.preview_history:
                return {'total_previews': 0}
            
            total_previews = len(self.core.preview_history)
            total_rows_previewed = sum(r['rows'] for r in self.core.preview_history)
            total_columns_previewed = sum(r['columns'] for r in self.core.preview_history)
            
            return {
                'total_previews': total_previews,
                'total_rows_previewed': total_rows_previewed,
                'total_columns_previewed': total_columns_previewed,
                'last_preview': self.core.preview_history[-1]['timestamp'] if self.core.preview_history else None,
                'current_dataset': self.core.current_dataset_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get preview statistics: {e}")
            return {}
    
    def clear_preview_history(self) -> int:
        """Clear preview history and return count"""
        try:
            count = len(self.core.preview_history)
            self.core.preview_history.clear()
            logger.info(f"🗑️ Cleared {count} preview records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear preview history: {e}")
            return 0
