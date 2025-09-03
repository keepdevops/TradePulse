#!/usr/bin/env python3
"""
TradePulse Integrated Panels - Metrics Exporter
Handles metrics export functionality
"""

import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class MetricsExporter:
    """Handles metrics export functionality"""
    
    def __init__(self, metrics: Dict[str, Any], history: List[Dict[str, Any]]):
        self.metrics = metrics
        self.history = history
    
    def export_metrics(self, filename: str = None) -> str:
        """Export metrics to file"""
        try:
            if filename is None:
                filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Create export data
            export_data = []
            
            # Add current metrics
            for key, value in self.metrics.items():
                if isinstance(value, datetime):
                    export_data.append({'metric': key, 'value': value.isoformat()})
                else:
                    export_data.append({'metric': key, 'value': value})
            
            # Add history
            for record in self.history:
                export_data.append({
                    'metric': f"operation_{record['operation']}",
                    'value': record['duration'],
                    'success': record['success'],
                    'timestamp': record['timestamp'].isoformat()
                })
            
            # Export to CSV
            df = pd.DataFrame(export_data)
            df.to_csv(filename, index=False)
            
            logger.info(f"✅ Metrics exported to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")
            return ""
