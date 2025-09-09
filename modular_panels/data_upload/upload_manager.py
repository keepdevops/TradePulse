#!/usr/bin/env python3
"""
TradePulse Data Upload - Upload Manager
Manages file uploads and data processing
"""

import os
import shutil
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import panel as pn

logger = logging.getLogger(__name__)

class UploadManager:
    """Manages file uploads and data processing"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.upload_history = []
        self.upload_dir = "uploads"
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        
        # Create upload directory if it doesn't exist
        os.makedirs(self.upload_dir, exist_ok=True)
        
        # Create file input widget for compatibility
        self.file_input = pn.widgets.FileInput(
            name='📁 Upload File',
            accept='.csv,.json,.feather,.parquet,.duckdb,.h5,.hdf5',
            width=300
        )
        
        logger.info("📁 Upload manager initialized")
    
    def upload_file(self, file_path: str, file_type: str = "upload") -> Dict[str, Any]:
        """Upload a file and process it"""
        try:
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': 'File does not exist',
                    'file_path': file_path
                }
            
            # Validate file size
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return {
                    'success': False,
                    'error': f'File too large ({file_size} bytes > {self.max_file_size} bytes)',
                    'file_path': file_path
                }
            
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = Path(file_path).name
            new_filename = f"{timestamp}_{filename}"
            destination = os.path.join(self.upload_dir, new_filename)
            
            # Copy file to upload directory
            shutil.copy2(file_path, destination)
            
            # Record upload
            upload_record = {
                'original_path': file_path,
                'uploaded_path': destination,
                'filename': new_filename,
                'file_type': file_type,
                'size': file_size,
                'upload_time': datetime.now(),
                'status': 'uploaded'
            }
            
            self.upload_history.append(upload_record)
            
            logger.info(f"✅ File uploaded: {filename} -> {new_filename}")
            
            return {
                'success': True,
                'file_path': destination,
                'filename': new_filename,
                'size': file_size,
                'upload_time': upload_record['upload_time']
            }
            
        except Exception as e:
            logger.error(f"❌ Upload failed for {file_path}: {e}")
            return {
                'success': False,
                'error': str(e),
                'file_path': file_path
            }
    
    def get_upload_history(self) -> List[Dict[str, Any]]:
        """Get upload history"""
        return self.upload_history.copy()
    
    def get_upload_stats(self) -> Dict[str, Any]:
        """Get upload statistics"""
        if not self.upload_history:
            return {
                'total_uploads': 0,
                'total_size': 0,
                'file_types': {},
                'recent_uploads': []
            }
        
        total_size = sum(record['size'] for record in self.upload_history)
        file_types = {}
        
        for record in self.upload_history:
            file_type = record['file_type']
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        recent_uploads = sorted(
            self.upload_history, 
            key=lambda x: x['upload_time'], 
            reverse=True
        )[:5]
        
        return {
            'total_uploads': len(self.upload_history),
            'total_size': total_size,
            'total_size_human': self._format_size(total_size),
            'file_types': file_types,
            'recent_uploads': recent_uploads
        }
    
    def clear_upload_history(self) -> int:
        """Clear upload history and return count"""
        count = len(self.upload_history)
        self.upload_history.clear()
        logger.info(f"🗑️ Cleared {count} upload records")
        return count
    
    def get_uploaded_files(self) -> List[str]:
        """Get list of uploaded files"""
        try:
            files = []
            for filename in os.listdir(self.upload_dir):
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.isfile(file_path):
                    files.append(file_path)
            return files
        except Exception as e:
            logger.error(f"❌ Error getting uploaded files: {e}")
            return []
    
    def delete_uploaded_file(self, filename: str) -> bool:
        """Delete an uploaded file"""
        try:
            file_path = os.path.join(self.upload_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"🗑️ Deleted uploaded file: {filename}")
                return True
            else:
                logger.warning(f"⚠️ File not found: {filename}")
                return False
        except Exception as e:
            logger.error(f"❌ Error deleting file {filename}: {e}")
            return False
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
