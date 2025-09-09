#!/usr/bin/env python3
"""
TradePulse M3 File Manager - Search & Metadata
Search and metadata functionality for M3 hard drive access
"""

import os
import glob
import logging
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class M3FileManagerSearch:
    """M3 file manager search and metadata functionality"""
    
    def __init__(self, core_manager):
        self.core = core_manager
    
    def search_files(self, search_path: str, filename_pattern: str, 
                    file_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Search for files matching pattern"""
        try:
            if not os.path.exists(search_path):
                raise ValueError(f"Search path does not exist: {search_path}")
            
            found_files = []
            
            # Determine extensions to search
            if file_types:
                extensions = []
                for file_type in file_types:
                    if file_type in self.core.supported_extensions:
                        extensions.extend(self.core.supported_extensions[file_type])
            else:
                extensions = [ext for exts in self.core.supported_extensions.values() for ext in exts]
            
            for ext in extensions:
                # Create search pattern
                if '*' in filename_pattern:
                    search_pattern = os.path.join(search_path, filename_pattern)
                else:
                    search_pattern = os.path.join(search_path, f"*{filename_pattern}*{ext.replace('*', '')}")
                
                try:
                    matches = glob.glob(search_pattern, recursive=True)
                    for match in matches:
                        if os.path.isfile(match):
                            found_files.append({
                                'name': os.path.basename(match),
                                'path': match,
                                'size': os.path.getsize(match),
                                'extension': Path(match).suffix.lower(),
                                'last_modified': datetime.fromtimestamp(os.path.getmtime(match)).isoformat(),
                                'readable': os.access(match, os.R_OK)
                            })
                except Exception as e:
                    logger.debug(f"⚠️ Error searching with pattern {search_pattern}: {e}")
                    continue
            
            # Remove duplicates
            unique_files = []
            seen_paths = set()
            for file_info in found_files:
                if file_info['path'] not in seen_paths:
                    unique_files.append(file_info)
                    seen_paths.add(file_info['path'])
            
            logger.info(f"🔍 Found {len(unique_files)} files matching '{filename_pattern}' in {search_path}")
            return unique_files
            
        except Exception as e:
            logger.error(f"❌ Failed to search files: {e}")
            return []
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get detailed metadata for a specific file"""
        try:
            if not os.path.exists(file_path):
                raise ValueError(f"File does not exist: {file_path}")
            
            if not os.path.isfile(file_path):
                raise ValueError(f"Path is not a file: {file_path}")
            
            stat = os.stat(file_path)
            path_obj = Path(file_path)
            
            metadata = {
                'name': path_obj.name,
                'path': file_path,
                'size': stat.st_size,
                'size_human': self.core._format_file_size(stat.st_size),
                'extension': path_obj.suffix.lower(),
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'accessed': datetime.fromtimestamp(stat.st_atime).isoformat(),
                'readable': os.access(file_path, os.R_OK),
                'writable': os.access(file_path, os.W_OK),
                'executable': os.access(file_path, os.X_OK),
                'owner': stat.st_uid,
                'group': stat.st_gid,
                'permissions': oct(stat.st_mode)[-3:]
            }
            
            # Try to get additional info for data files
            if metadata['extension'] in ['.csv', '.json', '.feather', '.parquet']:
                try:
                    metadata['data_info'] = self._get_data_file_info(file_path)
                except Exception as e:
                    metadata['data_info'] = {'error': str(e)}
            
            logger.info(f"📄 Retrieved metadata for {file_path}")
            return metadata
            
        except Exception as e:
            logger.error(f"❌ Failed to get file metadata for {file_path}: {e}")
            return {}
    
    def _get_data_file_info(self, file_path: str) -> Dict[str, Any]:
        """Get basic info about data files without loading full content"""
        try:
            extension = Path(file_path).suffix.lower()
            
            if extension == '.csv':
                # Read first few lines to get column info
                df_sample = pd.read_csv(file_path, nrows=5)
                return {
                    'columns': list(df_sample.columns),
                    'sample_rows': len(df_sample),
                    'estimated_total_rows': sum(1 for line in open(file_path)) - 1
                }
            
            elif extension == '.json':
                # Read JSON structure
                with open(file_path, 'r') as f:
                    data = json.load(f)
                if isinstance(data, list):
                    return {
                        'type': 'list',
                        'length': len(data),
                        'sample_keys': list(data[0].keys()) if data else []
                    }
                else:
                    return {
                        'type': 'object',
                        'keys': list(data.keys())
                    }
            
            elif extension == '.feather':
                # Get Feather file info
                df = pd.read_feather(file_path)
                return {
                    'columns': list(df.columns),
                    'rows': len(df),
                    'dtypes': df.dtypes.to_dict()
                }
            
            elif extension == '.parquet':
                # Get Parquet file info
                df = pd.read_parquet(file_path)
                return {
                    'columns': list(df.columns),
                    'rows': len(df),
                    'dtypes': df.dtypes.to_dict()
                }
            
            else:
                return {'type': 'unknown'}
                
        except Exception as e:
            return {'error': str(e)}
    
    def get_m3_status(self) -> Dict[str, Any]:
        """Get overall M3 drive status and statistics"""
        try:
            status = {
                'accessible_paths': [],
                'total_files_found': 0,
                'file_types_found': {},
                'total_size': 0,
                'scan_time': datetime.now().isoformat()
            }
            
            for path in self.core.m3_root_paths:
                if os.path.exists(path):
                    status['accessible_paths'].append(path)
                    
                    # Quick scan for statistics
                    try:
                        for ext_list in self.core.supported_extensions.values():
                            for ext in ext_list:
                                pattern = os.path.join(path, ext)
                                files = glob.glob(pattern, recursive=True)
                                
                                for file_path in files:
                                    if os.path.isfile(file_path):
                                        status['total_files_found'] += 1
                                        status['total_size'] += os.path.getsize(file_path)
                                        
                                        ext_name = Path(file_path).suffix.lower()
                                        status['file_types_found'][ext_name] = status['file_types_found'].get(ext_name, 0) + 1
                    except Exception as e:
                        logger.debug(f"⚠️ Error scanning {path}: {e}")
                        continue
            
            logger.info(f"📊 M3 Status: {status['total_files_found']} files, {len(status['accessible_paths'])} accessible paths")
            return status
            
        except Exception as e:
            logger.error(f"❌ Failed to get M3 status: {e}")
            return {}
