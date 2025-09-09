#!/usr/bin/env python3
"""
TradePulse M3 File Manager - Core
Core file management functionality for M3 hard drive access
"""

import os
import glob
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import shutil

logger = logging.getLogger(__name__)

class M3FileManagerCore:
    """Core M3 file manager with basic functionality"""
    
    def __init__(self):
        self.m3_root_paths = [
            "/Volumes",
            "/Users/moose/Desktop",
            "/Users/moose/Documents", 
            "/Users/moose/Downloads",
            "/Users/moose/Data",
            "/Users/moose/Trading",
            "/Users/moose/Stocks"
        ]
        
        self.supported_extensions = {
            'csv': ['*.csv'],
            'json': ['*.json'],
            'feather': ['*.feather'],
            'parquet': ['*.parquet'],
            'duckdb': ['*.duckdb'],
            'keras': ['*.h5', '*.hdf5'],
            'excel': ['*.xlsx', '*.xls'],
            'text': ['*.txt', '*.log']
        }
        
        self.file_cache = {}
        self.directory_cache = {}
    
    def get_m3_directories(self, base_path: Optional[str] = None) -> Dict[str, Any]:
        """Get available directories on M3 drive"""
        try:
            directories = {}
            
            if base_path:
                paths_to_scan = [base_path]
            else:
                paths_to_scan = self.m3_root_paths
            
            for path in paths_to_scan:
                if os.path.exists(path):
                    try:
                        # Get immediate subdirectories
                        subdirs = []
                        for item in os.listdir(path):
                            item_path = os.path.join(path, item)
                            if os.path.isdir(item_path):
                                subdirs.append({
                                    'name': item,
                                    'path': item_path,
                                    'size': self._get_directory_size(item_path),
                                    'file_count': self._count_files_in_directory(item_path),
                                    'last_modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                                })
                        
                        directories[path] = {
                            'path': path,
                            'subdirectories': subdirs,
                            'total_subdirs': len(subdirs),
                            'total_size': sum(d['size'] for d in subdirs),
                            'total_files': sum(d['file_count'] for d in subdirs)
                        }
                        
                    except Exception as e:
                        logger.warning(f"⚠️ Could not scan directory {path}: {e}")
                        continue
            
            logger.info(f"📁 Found {len(directories)} accessible directories")
            return directories
            
        except Exception as e:
            logger.error(f"❌ Failed to get M3 directories: {e}")
            return {}
    
    def browse_directory(self, directory_path: str, file_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Browse specific directory with file filtering"""
        try:
            if not os.path.exists(directory_path):
                raise ValueError(f"Directory does not exist: {directory_path}")
            
            if not os.path.isdir(directory_path):
                raise ValueError(f"Path is not a directory: {directory_path}")
            
            # Determine file extensions to scan
            if file_types:
                extensions = []
                for file_type in file_types:
                    if file_type in self.supported_extensions:
                        extensions.extend(self.supported_extensions[file_type])
            else:
                extensions = [ext for exts in self.supported_extensions.values() for ext in exts]
            
            files = []
            subdirectories = []
            
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                
                if os.path.isdir(item_path):
                    subdirectories.append({
                        'name': item,
                        'path': item_path,
                        'type': 'directory',
                        'size': self._get_directory_size(item_path),
                        'file_count': self._count_files_in_directory(item_path),
                        'last_modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                    })
                
                elif os.path.isfile(item_path):
                    # Check if file matches any of our extensions
                    if any(item.lower().endswith(ext.replace('*', '')) for ext in extensions):
                        files.append({
                            'name': item,
                            'path': item_path,
                            'type': 'file',
                            'size': os.path.getsize(item_path),
                            'extension': Path(item).suffix.lower(),
                            'last_modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat(),
                            'readable': os.access(item_path, os.R_OK)
                        })
            
            result = {
                'directory': directory_path,
                'files': files,
                'subdirectories': subdirectories,
                'total_files': len(files),
                'total_subdirs': len(subdirectories),
                'total_size': sum(f['size'] for f in files) + sum(d['size'] for d in subdirectories),
                'file_types_found': list(set(f['extension'] for f in files))
            }
            
            logger.info(f"📂 Browsed {directory_path}: {len(files)} files, {len(subdirectories)} subdirs")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to browse directory {directory_path}: {e}")
            return {}
    
    def copy_file_to_tradepulse(self, source_path: str, destination_dir: str = "upload_data") -> Dict[str, Any]:
        """Copy file from M3 to TradePulse upload directory"""
        try:
            if not os.path.exists(source_path):
                raise ValueError(f"Source file does not exist: {source_path}")
            
            # Create destination directory if it doesn't exist
            os.makedirs(destination_dir, exist_ok=True)
            
            # Generate destination filename
            filename = os.path.basename(source_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_filename = f"{timestamp}_{filename}"
            dest_path = os.path.join(destination_dir, dest_filename)
            
            # Copy file
            shutil.copy2(source_path, dest_path)
            
            result = {
                'source_path': source_path,
                'destination_path': dest_path,
                'filename': dest_filename,
                'size': os.path.getsize(dest_path),
                'copied_at': datetime.now().isoformat(),
                'success': True
            }
            
            logger.info(f"📥 Copied {source_path} to {dest_path}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to copy file {source_path}: {e}")
            return {
                'source_path': source_path,
                'error': str(e),
                'success': False
            }
    
    def _get_directory_size(self, directory_path: str) -> int:
        """Calculate directory size recursively"""
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(directory_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    try:
                        total_size += os.path.getsize(file_path)
                    except (OSError, FileNotFoundError):
                        continue
            return total_size
        except Exception:
            return 0
    
    def _count_files_in_directory(self, directory_path: str) -> int:
        """Count files in directory recursively"""
        try:
            count = 0
            for dirpath, dirnames, filenames in os.walk(directory_path):
                count += len(filenames)
            return count
        except Exception:
            return 0
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"

# Global instance
m3_file_manager_core = M3FileManagerCore()
