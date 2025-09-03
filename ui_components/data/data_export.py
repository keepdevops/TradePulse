#!/usr/bin/env python3
"""
TradePulse Data Manager - Export
Dataset export functionality
"""

import pandas as pd
import logging
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class DataExport:
    """Dataset export functionality"""
    
    def export_dataset(self, dataset_id: str, uploaded_datasets: Dict, format: str = 'csv', filepath: str = None) -> str:
        """Export a dataset to various formats"""
        if dataset_id not in uploaded_datasets:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        data = uploaded_datasets[dataset_id]['data']
        
        if not filepath:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filepath = f"export_{dataset_id}_{timestamp}"
        
        try:
            if format.lower() == 'csv':
                data.to_csv(f"{filepath}.csv", index=False)
            elif format.lower() == 'json':
                data.to_json(f"{filepath}.json", orient='records')
            elif format.lower() == 'excel':
                data.to_excel(f"{filepath}.xlsx", index=False)
            elif format.lower() == 'feather':
                data.to_feather(f"{filepath}.feather")
            elif format.lower() == 'parquet':
                data.to_parquet(f"{filepath}.parquet")
            else:
                raise ValueError(f"Unsupported export format: {format}")
            
            logger.info(f"✅ Dataset {dataset_id} exported to {filepath}.{format}")
            return f"{filepath}.{format}"
            
        except Exception as e:
            logger.error(f"❌ Failed to export dataset {dataset_id}: {e}")
            raise
    
    def get_supported_formats(self) -> Dict[str, str]:
        """Get supported export formats"""
        return {
            'csv': 'Comma Separated Values',
            'json': 'JavaScript Object Notation',
            'excel': 'Microsoft Excel',
            'feather': 'Apache Feather (Fast)',
            'parquet': 'Apache Parquet (Compressed)'
        }
    
    def validate_export_format(self, format: str) -> bool:
        """Validate export format"""
        supported_formats = self.get_supported_formats()
        return format.lower() in supported_formats
    
    def get_export_preview(self, dataset_id: str, uploaded_datasets: Dict, rows: int = 5) -> Dict:
        """Get preview of dataset for export"""
        if dataset_id not in uploaded_datasets:
            return {}
        
        data = uploaded_datasets[dataset_id]['data']
        
        return {
            'dataset_id': dataset_id,
            'shape': data.shape,
            'columns': list(data.columns),
            'preview': data.head(rows).to_dict('records'),
            'dtypes': data.dtypes.to_dict()
        }
    
    def batch_export(self, dataset_ids: list, uploaded_datasets: Dict, format: str = 'csv') -> Dict[str, str]:
        """Export multiple datasets"""
        results = {}
        
        for dataset_id in dataset_ids:
            try:
                filepath = self.export_dataset(dataset_id, format, None, uploaded_datasets)
                results[dataset_id] = filepath
            except Exception as e:
                results[dataset_id] = f"Error: {str(e)}"
        
        return results
