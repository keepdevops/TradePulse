#!/usr/bin/env python3
"""
TradePulse M3 File Manager
Manages M3 hard drive file access and operations
"""

import os
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)

class M3FileManager:
    """Manages M3 hard drive file access and operations"""
    
    def __init__(self):
        self.supported_extensions = ['.csv', '.json', '.feather', '.parquet', '.duckdb', '.h5', '.hdf5']
        self.scan_directories = [
            "/Users/moose",
            "/Users/moose/Downloads",
            "/Users/moose/Documents",
            "/Users/moose/Desktop"
        ]
        
        logger.info("📁 M3 File Manager initialized")
    
    def get_m3_status(self) -> Dict[str, Any]:
        """Get M3 drive status and statistics"""
        try:
            accessible_paths = []
            total_files_found = 0
            total_size = 0
            file_types_found = {}
            
            for directory in self.scan_directories:
                if os.path.exists(directory):
                    accessible_paths.append(directory)
                    
                    # Count files in directory
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if any(file.endswith(ext) for ext in self.supported_extensions):
                                total_files_found += 1
                                file_path = os.path.join(root, file)
                                try:
                                    file_size = os.path.getsize(file_path)
                                    total_size += file_size
                                    
                                    # Count file types
                                    ext = Path(file).suffix.lower()
                                    file_types_found[ext] = file_types_found.get(ext, 0) + 1
                                except:
                                    pass
            
            return {
                'accessible_paths': accessible_paths,
                'total_files_found': total_files_found,
                'total_size': total_size,
                'file_types_found': file_types_found,
                'scan_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting M3 status: {e}")
            return {
                'accessible_paths': [],
                'total_files_found': 0,
                'total_size': 0,
                'file_types_found': {},
                'scan_time': datetime.now().isoformat(),
                'error': str(e)
            }
    
    def browse_directory(self, directory_path: str, file_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """Browse a specific directory"""
        try:
            if not os.path.exists(directory_path):
                return {
                    'error': f'Directory does not exist: {directory_path}'
                }
            
            files = []
            subdirectories = []
            total_files = 0
            total_subdirs = 0
            total_size = 0
            file_types_found = set()
            
            for item in os.listdir(directory_path):
                item_path = os.path.join(directory_path, item)
                
                if os.path.isdir(item_path):
                    # Count files in subdirectory
                    subdir_files = 0
                    subdir_size = 0
                    for root, dirs, files_list in os.walk(item_path):
                        for file in files_list:
                            if any(file.endswith(ext) for ext in self.supported_extensions):
                                subdir_files += 1
                                try:
                                    subdir_size += os.path.getsize(os.path.join(root, file))
                                except:
                                    pass
                    
                    subdirectories.append({
                        'name': item,
                        'path': item_path,
                        'file_count': subdir_files,
                        'size': subdir_size,
                        'last_modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                    })
                    total_subdirs += 1
                    
                elif os.path.isfile(item_path):
                    if any(item.endswith(ext) for ext in self.supported_extensions):
                        try:
                            file_size = os.path.getsize(item_path)
                            total_size += file_size
                            
                            files.append({
                                'name': item,
                                'path': item_path,
                                'size': file_size,
                                'extension': Path(item).suffix.lower(),
                                'last_modified': datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat(),
                                'readable': os.access(item_path, os.R_OK)
                            })
                            
                            file_types_found.add(Path(item).suffix.lower())
                            total_files += 1
                        except Exception as e:
                            logger.warning(f"⚠️ Error processing file {item_path}: {e}")
            
            return {
                'directory': directory_path,
                'files': files,
                'subdirectories': subdirectories,
                'total_files': total_files,
                'total_subdirs': total_subdirs,
                'total_size': total_size,
                'file_types_found': list(file_types_found)
            }
            
        except Exception as e:
            logger.error(f"❌ Error browsing directory {directory_path}: {e}")
            return {
                'error': str(e),
                'directory': directory_path
            }
    
    def search_files(self, search_path: str, pattern: str, file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search for files matching a pattern"""
        try:
            results = []
            
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if pattern.lower() in file.lower():
                        if file_types is None or any(file.endswith(ext) for ext in self.supported_extensions):
                            file_path = os.path.join(root, file)
                            try:
                                results.append({
                                    'name': file,
                                    'path': file_path,
                                    'size': os.path.getsize(file_path),
                                    'extension': Path(file).suffix.lower(),
                                    'last_modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                                    'readable': os.access(file_path, os.R_OK)
                                })
                            except Exception as e:
                                logger.warning(f"⚠️ Error processing file {file_path}: {e}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Error searching files: {e}")
            return []
    
    def copy_file_to_tradepulse(self, file_path: str) -> Dict[str, Any]:
        """Copy a file to the TradePulse upload directory"""
        try:
            if not os.path.exists(file_path):
                return {
                    'success': False,
                    'error': 'File does not exist'
                }
            
            # Create upload directory
            upload_dir = "uploads"
            os.makedirs(upload_dir, exist_ok=True)
            
            # Generate destination filename
            filename = Path(file_path).name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            destination = os.path.join(upload_dir, f"{timestamp}_{filename}")
            
            # Copy file
            import shutil
            shutil.copy2(file_path, destination)
            
            return {
                'success': True,
                'filename': f"{timestamp}_{filename}",
                'destination': destination,
                'size': os.path.getsize(destination)
            }
            
        except Exception as e:
            logger.error(f"❌ Error copying file {file_path}: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Global instance
m3_file_manager = M3FileManager()
