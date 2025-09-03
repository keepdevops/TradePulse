#!/usr/bin/env python3
"""
TradePulse Dataset Selector - Dataset Preview
Handles dataset preview, information display, and metadata
"""

import panel as pn
import pandas as pd
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class DatasetPreview:
    """Handles dataset preview, information display, and metadata"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.current_dataset_id = None
        self.preview_history = []
        
        # Create UI components
        self.dataset_info = pn.pane.Markdown("**Dataset Info:** Select a dataset to view details")
        
        self.preview_table = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='Dataset Preview'
        )
        
        self.metadata_display = pn.pane.Markdown("**Metadata:** No dataset selected")
        
        self.statistics_display = pn.pane.Markdown("**Statistics:** No dataset selected")
    
    def update_preview(self, dataset_id: str):
        """Update preview for the specified dataset"""
        try:
            if not dataset_id:
                self._clear_preview()
                return
            
            logger.info(f"📊 Updating preview for dataset: {dataset_id}")
            
            # Get dataset data
            dataset_data = self.data_manager.get_dataset(dataset_id)
            if dataset_data is None:
                logger.warning(f"⚠️ Could not retrieve dataset {dataset_id}")
                self._clear_preview()
                return
            
            # Get dataset info
            dataset_info = self.data_manager.get_dataset_info(dataset_id)
            
            # Update dataset info display
            self._update_dataset_info(dataset_info, dataset_data)
            
            # Update preview table
            self._update_preview_table(dataset_data)
            
            # Update metadata display
            self._update_metadata_display(dataset_info, dataset_data)
            
            # Update statistics display
            self._update_statistics_display(dataset_data)
            
            # Record preview
            self._record_preview(dataset_id, dataset_data.shape)
            
            self.current_dataset_id = dataset_id
            logger.info(f"✅ Preview updated for dataset {dataset_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to update preview: {e}")
            self._clear_preview()
    
    def _update_dataset_info(self, dataset_info: Dict, dataset_data: pd.DataFrame):
        """Update the dataset information display"""
        try:
            if not dataset_info:
                self.dataset_info.object = "**Dataset Info:** Information not available"
                return
            
            info_text = f"""
            **Dataset Info:**
            - **ID:** {dataset_info.get('id', 'Unknown')}
            - **Name:** {dataset_info.get('name', 'Unnamed')}
            - **Type:** {dataset_info.get('type', 'Unknown')}
            - **Shape:** {dataset_data.shape[0]} rows × {dataset_data.shape[1]} columns
            - **Registered:** {dataset_info.get('registered_at', 'Unknown')}
            - **Last Updated:** {dataset_info.get('last_updated', 'Unknown')}
            """
            
            self.dataset_info.object = info_text
            
        except Exception as e:
            logger.error(f"Failed to update dataset info: {e}")
            self.dataset_info.object = "**Dataset Info:** Error loading information"
    
    def _update_preview_table(self, dataset_data: pd.DataFrame):
        """Update the preview table with dataset data"""
        try:
            if dataset_data.empty:
                self.preview_table.value = pd.DataFrame()
                return
            
            # Show first 10 rows for preview
            preview_data = dataset_data.head(10)
            self.preview_table.value = preview_data
            
            # Add row count indicator
            if len(dataset_data) > 10:
                self.preview_table.name = f'Dataset Preview (showing first 10 of {len(dataset_data)} rows)'
            else:
                self.preview_table.name = f'Dataset Preview ({len(dataset_data)} rows)'
                
        except Exception as e:
            logger.error(f"Failed to update preview table: {e}")
            self.preview_table.value = pd.DataFrame()
    
    def _update_metadata_display(self, dataset_info: Dict, dataset_data: pd.DataFrame):
        """Update the metadata display"""
        try:
            metadata = dataset_info.get('metadata', {})
            
            if not metadata:
                metadata_text = "**Metadata:** No additional metadata available"
            else:
                metadata_text = "**Metadata:**\n"
                for key, value in metadata.items():
                    metadata_text += f"- **{key}:** {value}\n"
            
            # Add data type information
            metadata_text += f"\n**Data Types:**\n"
            for col, dtype in dataset_data.dtypes.items():
                metadata_text += f"- **{col}:** {dtype}\n"
            
            self.metadata_display.object = metadata_text
            
        except Exception as e:
            logger.error(f"Failed to update metadata display: {e}")
            self.metadata_display.object = "**Metadata:** Error loading metadata"
    
    def _update_statistics_display(self, dataset_data: pd.DataFrame):
        """Update the statistics display"""
        try:
            if dataset_data.empty:
                self.statistics_display.object = "**Statistics:** No data available"
                return
            
            # Calculate basic statistics
            numeric_columns = dataset_data.select_dtypes(include=['number']).columns
            categorical_columns = dataset_data.select_dtypes(include=['object']).columns
            
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
            
            self.statistics_display.object = stats_text
            
        except Exception as e:
            logger.error(f"Failed to update statistics display: {e}")
            self.statistics_display.object = "**Statistics:** Error calculating statistics"
    
    def _clear_preview(self):
        """Clear all preview displays"""
        try:
            self.dataset_info.object = "**Dataset Info:** Select a dataset to view details"
            self.preview_table.value = pd.DataFrame()
            self.preview_table.name = 'Dataset Preview'
            self.metadata_display.object = "**Metadata:** No dataset selected"
            self.statistics_display.object = "**Statistics:** No dataset selected"
            self.current_dataset_id = None
            
        except Exception as e:
            logger.error(f"Failed to clear preview: {e}")
    
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
            self.preview_history.append(preview_record)
            
        except Exception as e:
            logger.error(f"Failed to record preview: {e}")
    
    def get_current_dataset_id(self) -> Optional[str]:
        """Get the currently previewed dataset ID"""
        return self.current_dataset_id
    
    def get_preview_history(self) -> List[Dict]:
        """Get preview history"""
        return self.preview_history.copy()
    
    def get_preview_statistics(self) -> Dict:
        """Get preview statistics"""
        try:
            if not self.preview_history:
                return {'total_previews': 0}
            
            total_previews = len(self.preview_history)
            total_rows_previewed = sum(r['rows'] for r in self.preview_history)
            total_columns_previewed = sum(r['columns'] for r in self.preview_history)
            
            return {
                'total_previews': total_previews,
                'total_rows_previewed': total_rows_previewed,
                'total_columns_previewed': total_columns_previewed,
                'last_preview': self.preview_history[-1]['timestamp'] if self.preview_history else None,
                'current_dataset': self.current_dataset_id
            }
            
        except Exception as e:
            logger.error(f"Failed to get preview statistics: {e}")
            return {}
    
    def clear_preview_history(self) -> int:
        """Clear preview history and return count"""
        try:
            count = len(self.preview_history)
            self.preview_history.clear()
            logger.info(f"🗑️ Cleared {count} preview records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear preview history: {e}")
            return 0
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'dataset_info': self.dataset_info,
            'preview_table': self.preview_table,
            'metadata_display': self.metadata_display,
            'statistics_display': self.statistics_display
        }
