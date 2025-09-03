#!/usr/bin/env python3
"""
TradePulse Data Metrics - Operations
Metrics-related operations for the data metrics
"""

import pandas as pd
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class DataMetricsOperations:
    """Metrics-related operations for data metrics"""
    
    def record_metrics_calculation(self, metrics_history: List[Dict], shape: tuple, metrics: Dict):
        """Record metrics calculation in history"""
        try:
            metrics_record = {
                'timestamp': datetime.now(),
                'dataset_shape': shape,
                'row_count': metrics.get('row_count', 0),
                'column_count': metrics.get('column_count', 0),
                'memory_mb': metrics.get('memory_usage_mb', 0.0)
            }
            
            metrics_history.append(metrics_record)
            
        except Exception as e:
            logger.error(f"Failed to record metrics calculation: {e}")
    
    def get_metrics_statistics(self, metrics_history: List[Dict]) -> Dict:
        """Get metrics calculation statistics"""
        try:
            if not metrics_history:
                return {'total_calculations': 0}
            
            total_calculations = len(metrics_history)
            total_rows_processed = sum(r['row_count'] for r in metrics_history)
            total_columns_processed = sum(r['column_count'] for r in metrics_history)
            total_memory_processed = sum(r['memory_mb'] for r in metrics_history)
            
            return {
                'total_calculations': total_calculations,
                'total_rows_processed': total_rows_processed,
                'total_columns_processed': total_columns_processed,
                'total_memory_processed_mb': total_memory_processed,
                'last_calculation': metrics_history[-1]['timestamp'] if metrics_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get metrics statistics: {e}")
            return {}
    
    def clear_metrics_history(self, metrics_history: List[Dict]) -> int:
        """Clear metrics history and return count"""
        try:
            count = len(metrics_history)
            metrics_history.clear()
            logger.info(f"🗑️ Cleared {count} metrics calculations from history")
            return count
        except Exception as e:
            logger.error(f"Failed to clear metrics history: {e}")
            return 0
    
    def validate_data_for_metrics(self, data: pd.DataFrame) -> bool:
        """Validate data for metrics calculation"""
        try:
            if data is None:
                return False
            
            if not isinstance(data, pd.DataFrame):
                return False
            
            if data.empty:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate data for metrics: {e}")
            return False
    
    def export_metrics_to_json(self, metrics: Dict, filename: str = None) -> str:
        """Export metrics to JSON file"""
        try:
            import json
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"data_metrics_{timestamp}.json"
            
            with open(filename, 'w') as f:
                json.dump(metrics, f, indent=2, default=str)
            
            logger.info(f"📤 Metrics exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export metrics to JSON: {e}")
            return None
    
    def export_metrics_to_csv(self, metrics: Dict, filename: str = None) -> str:
        """Export metrics to CSV file"""
        try:
            from datetime import datetime
            
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"data_metrics_{timestamp}.csv"
            
            # Flatten metrics for CSV export
            flat_metrics = self._flatten_metrics(metrics)
            
            # Convert to DataFrame and export
            df = pd.DataFrame([flat_metrics])
            df.to_csv(filename, index=False)
            
            logger.info(f"📤 Metrics exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export metrics to CSV: {e}")
            return None
    
    def _flatten_metrics(self, metrics: Dict) -> Dict:
        """Flatten nested metrics for CSV export"""
        flat_metrics = {}
        
        for key, value in metrics.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flat_metrics[f"{key}_{sub_key}"] = sub_value
            else:
                flat_metrics[key] = value
        
        return flat_metrics
    
    def get_metrics_summary_text(self, metrics: Dict) -> str:
        """Get text summary of metrics"""
        try:
            if not metrics or metrics.get('row_count', 0) == 0:
                return "No data available for analysis"
            
            summary_lines = [
                f"**Dataset Size**: {metrics.get('row_count', 0):,} rows × {metrics.get('column_count', 0)} columns",
                f"**Memory Usage**: {metrics.get('memory_usage_mb', 0.0):.2f} MB",
                f"**Data Types**: {metrics.get('numeric_columns', 0)} numeric, {metrics.get('categorical_columns', 0)} categorical",
                f"**Missing Values**: {metrics.get('missing_values', {}).get('total_missing', 0):,} ({metrics.get('missing_values', {}).get('missing_percentage', 0.0):.1f}%)",
                f"**Duplicates**: {metrics.get('duplicate_count', 0):,} rows"
            ]
            
            return "\n".join(summary_lines)
            
        except Exception as e:
            logger.error(f"Failed to create metrics summary: {e}")
            return "Error creating summary"

