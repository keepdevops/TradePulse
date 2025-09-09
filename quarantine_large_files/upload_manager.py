#!/usr/bin/env python3
"""
TradePulse Data Upload - Upload Manager
Handles upload operations and management
"""

import panel as pn
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Callable
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UploadManager:
    """Handles upload operations and management"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.uploaded_data = {}
        self.upload_history = []
        self.upload_callbacks = []
        
        # Create UI components
        self.file_input = pn.widgets.FileInput(
            name='📁 Upload Data File',
            accept='.feather,.duckdb,.db,.csv,.json,.xlsx,.xls,.parquet',
            width=300
        )
        
        self.upload_button = pn.widgets.Button(
            name='🚀 Process File',
            button_type='primary',
            width=150,
            disabled=True
        )
        
        self.status_display = pn.pane.Markdown("**Status:** Ready to upload")
        
        self.data_info = pn.pane.Markdown("**Data Info:** No data loaded")
        
        # Setup callbacks
        self.file_input.param.watch(self.on_file_selected, 'value')
        self.upload_button.on_click(self.process_uploaded_file)
    
    def on_file_selected(self, event):
        """Handle file selection"""
        try:
            if event.new is not None:
                filename = event.old if event.old else "unknown"
                self.status_display.object = f"**Status:** File selected: {filename}"
                self.upload_button.disabled = False
                logger.info(f"📁 File selected: {filename}")
            else:
                self.upload_button.disabled = True
                self.status_display.object = "**Status:** Ready to upload"
                self.data_info.object = "**Data Info:** No data loaded"
                
        except Exception as e:
            logger.error(f"Failed to handle file selection: {e}")
            self.status_display.object = "**Status:** Error handling file selection"
    
    def process_uploaded_file(self, event):
        """Process the uploaded file"""
        try:
            if self.file_input.value is None:
                logger.warning("⚠️ No file selected for processing")
                return
            
            # Get file content and name
            file_content = self.file_input.value
            filename = self.file_input.filename or "unknown"
            
            logger.info(f"🚀 Processing uploaded file: {filename}")
            
            # Update status
            self.status_display.object = f"**Status:** Processing {filename}..."
            self.upload_button.disabled = True
            
            # Process the file (this will be handled by the main component)
            # For now, just record the upload attempt
            self._record_upload_attempt(filename, len(file_content), True)
            
            # Update status
            self.status_display.object = f"**Status:** File {filename} processed successfully"
            
            # Clear file input
            self.file_input.value = None
            self.upload_button.disabled = True
            
            logger.info(f"✅ File {filename} processed successfully")
            
        except Exception as e:
            logger.error(f"❌ File processing failed: {e}")
            self.status_display.object = f"**Status:** Error processing file - {str(e)}"
            self.upload_button.disabled = False
    
    def add_upload_callback(self, callback: Callable):
        """Add callback for upload events"""
        if callback not in self.upload_callbacks:
            self.upload_callbacks.append(callback)
            logger.info(f"✅ Added upload callback")
    
    def remove_upload_callback(self, callback: Callable):
        """Remove upload callback"""
        if callback in self.upload_callbacks:
            self.upload_callbacks.remove(callback)
            logger.info(f"✅ Removed upload callback")
    
    def notify_upload_callbacks(self, event_type: str, data: Dict):
        """Notify all upload callbacks"""
        try:
            for callback in self.upload_callbacks:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"Callback notification failed: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify upload callbacks: {e}")
    
    def update_data_info(self, data: pd.DataFrame, metadata: Dict):
        """Update the data info display"""
        try:
            if data is None or data.empty:
                self.data_info.object = "**Data Info:** No data loaded"
                return
            
            info_text = f"""
            **Data Info:**
            - **Filename:** {metadata.get('filename', 'Unknown')}
            - **Format:** {metadata.get('format', 'Unknown')}
            - **Shape:** {data.shape[0]:,} rows × {data.shape[1]} columns
            - **Memory Usage:** {data.memory_usage(deep=True).sum() / (1024*1024):.2f} MB
            - **Columns:** {', '.join(data.columns[:5])}{'...' if len(data.columns) > 5 else ''}
            """
            
            # Add format-specific info
            if metadata.get('format') == 'excel':
                info_text += f"\n- **Sheets:** {', '.join(metadata.get('sheets', []))}"
            elif metadata.get('format') in ['duckdb', 'sqlite']:
                info_text += f"\n- **Tables:** {', '.join(metadata.get('tables', []))}"
            
            self.data_info.object = info_text
            
        except Exception as e:
            logger.error(f"Failed to update data info: {e}")
            self.data_info.object = "**Data Info:** Error updating information"
    
    def clear_upload_data(self):
        """Clear uploaded data and reset UI"""
        try:
            self.uploaded_data.clear()
            self.file_input.value = None
            self.upload_button.disabled = True
            self.status_display.object = "**Status:** Ready to upload"
            self.data_info.object = "**Data Info:** No data loaded"
            
            logger.info("🗑️ Upload data cleared")
            
        except Exception as e:
            logger.error(f"Failed to clear upload data: {e}")
    
    def _record_upload_attempt(self, filename: str, file_size: int, success: bool, error: str = None):
        """Record upload attempt"""
        try:
            upload_record = {
                'timestamp': datetime.now(),
                'filename': filename,
                'file_size_bytes': file_size,
                'file_size_mb': file_size / (1024 * 1024),
                'success': success,
                'error': error
            }
            
            self.upload_history.append(upload_record)
            
        except Exception as e:
            logger.error(f"Failed to record upload attempt: {e}")
    
    def get_uploaded_data(self) -> Dict:
        """Get all uploaded data"""
        return self.uploaded_data.copy()
    
    def get_upload_history(self) -> List[Dict]:
        """Get upload history"""
        return self.upload_history.copy()
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """Get upload statistics"""
        try:
            if not self.upload_history:
                return {'total_uploads': 0}
            
            total_uploads = len(self.upload_history)
            successful_uploads = sum(1 for u in self.upload_history if u['success'])
            failed_uploads = total_uploads - successful_uploads
            
            # Calculate total data uploaded
            total_size_bytes = sum(u['file_size_bytes'] for u in self.upload_history if u['success'])
            total_size_mb = total_size_bytes / (1024 * 1024)
            
            return {
                'total_uploads': total_uploads,
                'successful_uploads': successful_uploads,
                'failed_uploads': failed_uploads,
                'success_rate': (successful_uploads / total_uploads * 100) if total_uploads > 0 else 0,
                'total_size_bytes': total_size_bytes,
                'total_size_mb': total_size_mb,
                'callbacks_registered': len(self.upload_callbacks),
                'last_upload': self.upload_history[-1]['timestamp'] if self.upload_history else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get upload statistics: {e}")
            return {}
    
    def clear_upload_history(self) -> int:
        """Clear upload history and return count"""
        try:
            count = len(self.upload_history)
            self.upload_history.clear()
            logger.info(f"🗑️ Cleared {count} upload records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear upload history: {e}")
            return 0
    
    def get_components(self) -> Dict:
        """Get UI components for external use"""
        return {
            'file_input': self.file_input,
            'upload_button': self.upload_button,
            'status_display': self.status_display,
            'data_info': self.data_info
        }
