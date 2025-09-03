#!/usr/bin/env python3
"""
TradePulse Data Upload - Processing History
Handles file processing history and statistics
"""

import pandas as pd
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class ProcessingHistory:
    """Handles file processing history and statistics"""
    
    def __init__(self):
        self.processing_history = []
    
    def record_processing(self, filename: str, format_type: str, shape: tuple, success: bool, error: str = None):
        """Record file processing operation"""
        try:
            processing_record = {
                'timestamp': pd.Timestamp.now(),
                'filename': filename,
                'format_type': format_type,
                'shape': shape,
                'rows': shape[0],
                'columns': shape[1],
                'success': success,
                'error': error
            }
            
            self.processing_history.append(processing_record)
            
        except Exception as e:
            logger.error(f"Failed to record processing: {e}")
    
    def get_processing_history(self) -> List[Dict]:
        """Get file processing history"""
        return self.processing_history.copy()
    
    def get_processing_statistics(self) -> Dict[str, Any]:
        """Get file processing statistics"""
        try:
            if not self.processing_history:
                return {'total_files': 0}
            
            total_files = len(self.processing_history)
            successful_files = sum(1 for p in self.processing_history if p['success'])
            failed_files = total_files - successful_files
            
            # Count by format
            format_counts = {}
            for processing in self.processing_history:
                format_type = processing['format_type']
                format_counts[format_type] = format_counts.get(format_type, 0) + 1
            
            # Calculate total data processed
            total_rows = sum(p['rows'] for p in self.processing_history if p['success'])
            total_columns = sum(p['columns'] for p in self.processing_history if p['success'])
            
            return {
                'total_files': total_files,
                'successful_files': successful_files,
                'failed_files': failed_files,
                'success_rate': (successful_files / total_files * 100) if total_files > 0 else 0,
                'format_distribution': format_counts,
                'total_rows_processed': total_rows,
                'total_columns_processed': total_columns,
                'last_processing': self.processing_history[-1]['timestamp'] if self.processing_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get processing statistics: {e}")
            return {}
    
    def clear_processing_history(self) -> int:
        """Clear processing history and return count"""
        try:
            count = len(self.processing_history)
            self.processing_history.clear()
            logger.info(f"🗑️ Cleared {count} processing records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear processing history: {e}")
            return 0
