#!/usr/bin/env python3
"""
TradePulse M3 File Browser - UI Operations
UI display and formatting operations for M3 file browser
"""

import panel as pn
import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class M3FileBrowserUI:
    """UI operations for M3 file browser"""
    
    def __init__(self, core_browser):
        self.core = core_browser
    
    def _load_m3_status(self):
        """Load M3 drive status"""
        try:
            from m3_file_manager import m3_file_manager
            status = m3_file_manager.get_m3_status()
            
            status_text = f"""
            ## 📊 M3 Drive Status
            
            **Accessible Paths:** {len(status.get('accessible_paths', []))}
            **Total Files Found:** {status.get('total_files_found', 0):,}
            **Total Size:** {self._format_size(status.get('total_size', 0))}
            **Scan Time:** {status.get('scan_time', 'Unknown')}
            
            ### 📁 Accessible Directories:
            """
            
            for path in status.get('accessible_paths', []):
                file_count = status.get('file_types_found', {}).get('.csv', 0) + \
                           status.get('file_types_found', {}).get('.json', 0) + \
                           status.get('file_types_found', {}).get('.feather', 0)
                status_text += f"- **{path}** ({file_count} data files)\n"
            
            self.core.status_display.object = status_text
            
        except Exception as e:
            logger.error(f"❌ Failed to load M3 status: {e}")
            self.core.status_display.object = f"❌ Failed to load M3 status: {e}"
    
    def _update_directory_display(self, directory_data: Dict[str, Any]):
        """Update directory display"""
        try:
            dir_text = f"""
            ## 📁 Directory Contents
            
            **Path:** `{directory_data['directory']}`
            **Files:** {directory_data['total_files']}
            **Subdirectories:** {directory_data['total_subdirs']}
            **Total Size:** {self._format_size(directory_data['total_size'])}
            **File Types:** {', '.join(directory_data['file_types_found']) if directory_data['file_types_found'] else 'None'}
            
            ### 📂 Subdirectories:
            """
            
            for subdir in directory_data['subdirectories'][:10]:  # Limit to 10
                size_str = self._format_size(subdir['size'])
                dir_text += f"""
                **📁 {subdir['name']}**
                - Path: `{subdir['path']}`
                - Size: {size_str}
                - Files: {subdir['file_count']}
                - Modified: {subdir['last_modified'][:19]}
                """
            
            dir_text += "\n### 📄 Files:\n"
            
            for file_info in directory_data['files'][:15]:  # Limit to 15
                size_str = self._format_size(file_info['size'])
                dir_text += f"""
                **📄 {file_info['name']}**
                - Size: {size_str}
                - Type: {file_info['extension']}
                - Modified: {file_info['last_modified'][:19]}
                - Readable: {'✅' if file_info['readable'] else '❌'}
                """
            
            if len(directory_data['files']) > 15:
                dir_text += f"\n... and {len(directory_data['files']) - 15} more files"
            
            self.core.directory_display.object = dir_text
            
        except Exception as e:
            logger.error(f"❌ Update directory display error: {e}")
            self.core.directory_display.object = f"❌ Update directory display error: {e}"
    
    def _update_file_details(self, file_info: Dict[str, Any]):
        """Update file details display"""
        try:
            if not file_info:
                self.core.file_details_display.object = "## 📄 File Details\n\nNo file selected"
                return
            
            details_text = f"""
            ## 📄 File Details
            
            **Name:** {file_info.get('name', 'Unknown')}
            **Path:** `{file_info.get('path', 'Unknown')}`
            **Size:** {file_info.get('size_human', 'Unknown')}
            **Type:** {file_info.get('extension', 'Unknown')}
            **Created:** {file_info.get('created', 'Unknown')[:19]}
            **Modified:** {file_info.get('modified', 'Unknown')[:19]}
            **Permissions:** {file_info.get('permissions', 'Unknown')}
            **Readable:** {'✅' if file_info.get('readable', False) else '❌'}
            **Writable:** {'✅' if file_info.get('writable', False) else '❌'}
            """
            
            # Add data file specific info
            if 'data_info' in file_info:
                data_info = file_info['data_info']
                if 'error' not in data_info:
                    details_text += "\n### 📊 Data File Information:\n"
                    
                    if 'columns' in data_info:
                        details_text += f"**Columns:** {', '.join(data_info['columns'])}\n"
                    if 'rows' in data_info:
                        details_text += f"**Rows:** {data_info['rows']:,}\n"
                    if 'type' in data_info:
                        details_text += f"**Type:** {data_info['type']}\n"
                    if 'length' in data_info:
                        details_text += f"**Length:** {data_info['length']:,}\n"
                else:
                    details_text += f"\n### ⚠️ Data Info Error: {data_info['error']}\n"
            
            self.core.file_details_display.object = details_text
            
        except Exception as e:
            logger.error(f"❌ Update file details error: {e}")
            self.core.file_details_display.object = f"❌ Update file details error: {e}"
    
    def _update_status(self, message: str):
        """Update status display"""
        try:
            current_status = self.core.status_display.object
            new_status = f"{current_status}\n\n**Latest:** {message}"
            self.core.status_display.object = new_status
        except Exception as e:
            logger.error(f"❌ Update status error: {e}")
    
    def _format_size(self, size_bytes: int) -> str:
        """Format file size"""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f}{size_names[i]}"
    
    def _create_search_results_display(self, results: List[Dict], pattern: str, search_path: str):
        """Create search results display"""
        try:
            search_text = f"""
            ## 🔍 Search Results
            
            **Pattern:** {pattern}
            **Location:** {search_path}
            **Files Found:** {len(results)}
            
            ### 📄 Found Files:
            """
            
            for i, file_info in enumerate(results[:20]):  # Limit to 20 results
                size_str = self._format_size(file_info['size'])
                search_text += f"""
                **{i+1}. {file_info['name']}**
                - Path: `{file_info['path']}`
                - Size: {size_str}
                - Type: {file_info['extension']}
                - Modified: {file_info['last_modified'][:19]}
                - Readable: {'✅' if file_info['readable'] else '❌'}
                """
            
            if len(results) > 20:
                search_text += f"\n... and {len(results) - 20} more files"
            
            return search_text
            
        except Exception as e:
            logger.error(f"❌ Create search results display error: {e}")
            return f"❌ Create search results display error: {e}"
