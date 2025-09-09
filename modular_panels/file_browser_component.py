#!/usr/bin/env python3
"""
TradePulse File Browser Component
Allows users to browse local PC directories and files for data import
"""

import panel as pn
import pandas as pd
import os
import glob
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Callable
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class FileBrowserComponent:
    """Component for browsing local directories and files"""
    
    def __init__(self, data_manager, on_file_select: Optional[Callable] = None):
        self.data_manager = data_manager
        self.on_file_select = on_file_select
        self.current_path = str(Path.home())  # Start from user's home directory
        self.selected_file = None
        self.file_history = []
        self.supported_extensions = [
            '.csv', '.json', '.feather', '.parquet', '.duckdb', '.db', '.sqlite',
            '.xlsx', '.xls', '.h5', '.hdf5', '.pkl', '.pickle'
        ]
        
        self.create_components()
        self.load_directory_contents()
    
    def create_components(self):
        """Create the file browser interface components"""
        # Current path display
        self.path_display = pn.pane.Markdown(f"**Current Path:** {self.current_path}")
        
        # Navigation buttons
        self.back_button = pn.widgets.Button(
            name='⬅️ Back',
            button_type='default',
            width=80,
            disabled=True
        )
        
        self.home_button = pn.widgets.Button(
            name='🏠 Home',
            button_type='default',
            width=80
        )
        
        self.refresh_button = pn.widgets.Button(
            name='🔄 Refresh',
            button_type='default',
            width=80
        )
        
        # Path input for manual navigation
        self.path_input = pn.widgets.TextInput(
            name='📁 Enter Path:',
            value=self.current_path,
            width=400
        )
        
        # Directory contents display
        self.directory_contents = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=300,
            name='Directory Contents',
            selectable='checkbox',
            page_size=20
        )
        
        # File preview
        self.file_preview = pn.widgets.Tabulator(
            pd.DataFrame(),
            height=200,
            name='File Preview'
        )
        
        # File info display
        self.file_info = pn.pane.Markdown("**File Info:** No file selected")
        
        # Action buttons
        self.load_button = pn.widgets.Button(
            name='📊 Load File',
            button_type='primary',
            width=120,
            disabled=True
        )
        
        self.add_to_data_button = pn.widgets.Button(
            name='➕ Add to Data Manager',
            button_type='success',
            width=150,
            disabled=True
        )
        
        self.refresh_symbols_button = pn.widgets.Button(
            name='🔄 Refresh Symbols',
            button_type='warning',
            width=120
        )
        
        # Status display
        self.status_display = pn.pane.Markdown("**Status:** Ready to browse")
        
        # Setup callbacks
        self.back_button.on_click(self.go_back)
        self.home_button.on_click(self.go_home)
        self.refresh_button.on_click(self.refresh_directory)
        self.path_input.param.watch(self.on_path_change, 'value')
        self.directory_contents.param.watch(self.on_file_selection, 'selection')
        self.load_button.on_click(self.load_selected_file)
        self.add_to_data_button.on_click(self.add_file_to_data_manager)
        self.refresh_symbols_button.on_click(self.refresh_symbol_list)
    
    def load_directory_contents(self):
        """Load and display the contents of the current directory"""
        try:
            path = Path(self.current_path)
            if not path.exists():
                self.status_display.object = f"**Status:** ❌ Path does not exist: {self.current_path}"
                return
            
            if not path.is_dir():
                self.status_display.object = f"**Status:** ❌ Not a directory: {self.current_path}"
                return
            
            # Get directory contents
            contents = []
            
            # Add parent directory entry
            if path.parent != path:
                contents.append({
                    'Name': '..',
                    'Type': 'Directory',
                    'Size': '',
                    'Modified': '',
                    'Path': str(path.parent),
                    'Is Directory': True
                })
            
            # Add directories
            for item in sorted(path.iterdir()):
                if item.is_dir():
                    try:
                        stat = item.stat()
                        contents.append({
                            'Name': f"📁 {item.name}",
                            'Type': 'Directory',
                            'Size': '',
                            'Modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'Path': str(item),
                            'Is Directory': True
                        })
                    except (PermissionError, OSError):
                        continue
            
            # Add files
            for item in sorted(path.iterdir()):
                if item.is_file():
                    try:
                        stat = item.stat()
                        file_ext = item.suffix.lower()
                        
                        # Determine file type icon
                        if file_ext in self.supported_extensions:
                            icon = "📊"  # Data file
                        elif file_ext in ['.txt', '.md', '.log']:
                            icon = "📄"  # Text file
                        elif file_ext in ['.py', '.js', '.html', '.css']:
                            icon = "💻"  # Code file
                        elif file_ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg']:
                            icon = "🖼️"  # Image file
                        else:
                            icon = "📄"  # Generic file
                        
                        contents.append({
                            'Name': f"{icon} {item.name}",
                            'Type': 'File',
                            'Size': self.format_file_size(stat.st_size),
                            'Modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M'),
                            'Path': str(item),
                            'Is Directory': False,
                            'Extension': file_ext
                        })
                    except (PermissionError, OSError):
                        continue
            
            # Create DataFrame and display
            df = pd.DataFrame(contents)
            if not df.empty:
                # Reorder columns for display
                display_columns = ['Name', 'Type', 'Size', 'Modified']
                df_display = df[display_columns].copy()
                self.directory_contents.value = df_display
                # Store full data for selection handling
                self.directory_contents._full_data = df
            else:
                self.directory_contents.value = pd.DataFrame(columns=['Name', 'Type', 'Size', 'Modified'])
                self.directory_contents._full_data = pd.DataFrame()
            
            # Update path display
            self.path_display.object = f"**Current Path:** {self.current_path}"
            self.path_input.value = self.current_path
            
            # Update back button state
            self.back_button.disabled = len(self.file_history) == 0
            
            self.status_display.object = f"**Status:** ✅ Loaded {len(contents)} items from {self.current_path}"
            logger.info(f"Loaded directory contents: {len(contents)} items from {self.current_path}")
            
        except Exception as e:
            logger.error(f"Error loading directory contents: {e}")
            self.status_display.object = f"**Status:** ❌ Error loading directory: {str(e)}"
    
    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def go_back(self, event=None):
        """Navigate back in history"""
        if self.file_history:
            previous_path = self.file_history.pop()
            self.current_path = previous_path
            self.load_directory_contents()
    
    def go_home(self, event=None):
        """Navigate to home directory"""
        self.current_path = str(Path.home())
        self.file_history.clear()
        self.load_directory_contents()
    
    def refresh_directory(self, event=None):
        """Refresh the current directory contents"""
        self.load_directory_contents()
    
    def on_path_change(self, event):
        """Handle manual path input change"""
        new_path = event.new
        if new_path and new_path != self.current_path:
            # Store current path in history
            self.file_history.append(self.current_path)
            self.current_path = new_path
            self.load_directory_contents()
    
    def on_file_selection(self, event):
        """Handle file selection in the directory contents"""
        try:
            if not event.new or not hasattr(self.directory_contents, '_full_data'):
                self.selected_file = None
                self.load_button.disabled = True
                self.add_to_data_button.disabled = True
                self.file_info.object = "**File Info:** No file selected"
                return
            
            # Get selected row
            selected_indices = event.new
            if not selected_indices:
                self.selected_file = None
                self.load_button.disabled = True
                self.add_to_data_button.disabled = True
                self.file_info.object = "**File Info:** No file selected"
                return
            
            # Get the first selected item
            selected_index = selected_indices[0]
            full_data = self.directory_contents._full_data
            
            if selected_index >= len(full_data):
                return
            
            selected_item = full_data.iloc[selected_index]
            
            if selected_item['Is Directory']:
                # Navigate to directory
                if selected_item['Name'] == '..':
                    self.go_back()
                else:
                    # Store current path in history
                    self.file_history.append(self.current_path)
                    self.current_path = selected_item['Path']
                    self.load_directory_contents()
            else:
                # File selected
                self.selected_file = selected_item
                self.load_button.disabled = False
                self.add_to_data_button.disabled = False
                
                # Update file info
                self.update_file_info(selected_item)
                
                # Try to load preview
                self.load_file_preview(selected_item['Path'])
                
        except Exception as e:
            logger.error(f"Error handling file selection: {e}")
            self.status_display.object = f"**Status:** ❌ Error selecting file: {str(e)}"
    
    def update_file_info(self, file_item):
        """Update the file information display"""
        try:
            path = Path(file_item['Path'])
            stat = path.stat()
            
            info_text = f"""
            **File Information**
            - **Name:** {path.name}
            - **Path:** {file_item['Path']}
            - **Size:** {file_item['Size']}
            - **Type:** {file_item['Type']}
            - **Extension:** {file_item.get('Extension', 'None')}
            - **Modified:** {file_item['Modified']}
            - **Created:** {datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M')}
            - **Supported:** {'✅' if file_item.get('Extension', '') in self.supported_extensions else '❌'}
            """
            self.file_info.object = info_text
            
        except Exception as e:
            logger.error(f"Error updating file info: {e}")
            self.file_info.object = f"**File Info:** Error displaying info - {str(e)}"
    
    def load_file_preview(self, file_path: str):
        """Load a preview of the selected file"""
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                self.file_preview.value = pd.DataFrame()
                return
            
            file_ext = path.suffix.lower()
            
            # Load preview based on file type
            preview_data = None
            
            if file_ext == '.csv':
                preview_data = pd.read_csv(file_path, nrows=10)
            elif file_ext == '.json':
                preview_data = pd.read_json(file_path, lines=True, nrows=10)
            elif file_ext == '.xlsx' or file_ext == '.xls':
                preview_data = pd.read_excel(file_path, nrows=10)
            elif file_ext == '.feather':
                preview_data = pd.read_feather(file_path)
                preview_data = preview_data.head(10)
            elif file_ext == '.parquet':
                preview_data = pd.read_parquet(file_path)
                preview_data = preview_data.head(10)
            elif file_ext in ['.db', '.sqlite', '.duckdb']:
                # For database files, show available tables
                import sqlite3
                try:
                    conn = sqlite3.connect(file_path)
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
                    conn.close()
                    preview_data = tables
                except:
                    preview_data = pd.DataFrame({'Note': ['Database file - use Load File to explore tables']})
            else:
                # For unsupported files, show basic info
                preview_data = pd.DataFrame({
                    'File': [path.name],
                    'Size': [self.format_file_size(path.stat().st_size)],
                    'Type': [file_ext or 'Unknown'],
                    'Note': ['Preview not available for this file type']
                })
            
            self.file_preview.value = preview_data
            self.status_display.object = f"**Status:** ✅ Loaded preview of {path.name}"
            
        except Exception as e:
            logger.error(f"Error loading file preview: {e}")
            self.file_preview.value = pd.DataFrame({
                'Error': [f'Could not load preview: {str(e)}']
            })
            self.status_display.object = f"**Status:** ❌ Error loading preview: {str(e)}"
    
    def load_selected_file(self, event=None):
        """Load the selected file into memory"""
        if self.selected_file is None:
            self.status_display.object = "**Status:** ❌ No file selected"
            return
        
        try:
            file_path = self.selected_file['Path']
            path = Path(file_path)
            
            if not path.exists():
                self.status_display.object = f"**Status:** ❌ File does not exist: {file_path}"
                return
            
            # Load the full file
            file_ext = path.suffix.lower()
            loaded_data = None
            
            if file_ext == '.csv':
                loaded_data = pd.read_csv(file_path)
            elif file_ext == '.json':
                loaded_data = pd.read_json(file_path)
            elif file_ext == '.xlsx' or file_ext == '.xls':
                loaded_data = pd.read_excel(file_path)
            elif file_ext == '.feather':
                loaded_data = pd.read_feather(file_path)
            elif file_ext == '.parquet':
                loaded_data = pd.read_parquet(file_path)
            elif file_ext in ['.db', '.sqlite', '.duckdb']:
                # For database files, load first table
                import sqlite3
                conn = sqlite3.connect(file_path)
                tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
                if not tables.empty:
                    first_table = tables.iloc[0]['name']
                    loaded_data = pd.read_sql_query(f"SELECT * FROM {first_table}", conn)
                conn.close()
            else:
                self.status_display.object = f"**Status:** ❌ Unsupported file type: {file_ext}"
                return
            
            # Store loaded data
            self.loaded_data = loaded_data
            
            # Update preview
            self.file_preview.value = loaded_data.head(20)
            
            # Update status
            self.status_display.object = f"**Status:** ✅ Loaded {path.name} ({loaded_data.shape[0]} rows, {loaded_data.shape[1]} columns)"
            
            # Call callback if provided
            if self.on_file_select:
                self.on_file_select(file_path, loaded_data)
            
            logger.info(f"Loaded file: {file_path} ({loaded_data.shape[0]} rows, {loaded_data.shape[1]} columns)")
            
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            self.status_display.object = f"**Status:** ❌ Error loading file: {str(e)}"
    
    def add_file_to_data_manager(self, event=None):
        """Add the loaded file to the data manager"""
        if not hasattr(self, 'loaded_data') or self.loaded_data is None:
            self.status_display.object = "**Status:** ❌ No file loaded"
            return
        
        try:
            file_path = self.selected_file['Path']
            filename = Path(file_path).name
            
            # Process the data to convert ticker to symbol if needed
            processed_data = self.process_data_for_upload(self.loaded_data.copy())
            
            # Add to data manager
            dataset_id = self.data_manager.add_uploaded_data(filename, processed_data, {
                'source': 'file_browser',
                'file_path': file_path,
                'loaded_at': datetime.now().isoformat(),
                'original_columns': list(self.loaded_data.columns),
                'processed_columns': list(processed_data.columns)
            })
            
            # Update symbol list if the data contains symbol information
            self.update_symbol_list_from_data(processed_data)
            
            self.status_display.object = f"**Status:** ✅ Added {filename} to data manager as dataset {dataset_id}"
            logger.info(f"Added file to data manager: {filename} -> {dataset_id}")
            
        except Exception as e:
            logger.error(f"Error adding file to data manager: {e}")
            self.status_display.object = f"**Status:** ❌ Error adding to data manager: {str(e)}"
    
    def update_symbol_list_from_data(self, data):
        """Update the symbol list based on loaded data"""
        try:
            if data is None or data.empty:
                return
            
            # Extract symbols using the improved extraction method
            found_symbols = self.extract_symbols_from_data(data)
            
            # Update the data manager's symbol list
            if found_symbols:
                # Convert to list and sort
                unique_symbols = sorted(list(found_symbols))
                
                # Update the data manager's symbols
                if hasattr(self.data_manager, 'core') and hasattr(self.data_manager.core, 'symbols'):
                    # Add new symbols to existing list
                    existing_symbols = set(self.data_manager.core.symbols)
                    new_symbols = [s for s in unique_symbols if s not in existing_symbols]
                    
                    if new_symbols:
                        self.data_manager.core.symbols.extend(new_symbols)
                        self.data_manager.core.symbols.sort()
                        logger.info(f"Updated symbol list with {len(new_symbols)} new symbols: {new_symbols}")
                        
                        # Trigger symbol list update callback if available
                        if hasattr(self.data_manager, 'on_symbols_updated'):
                            self.data_manager.on_symbols_updated(new_symbols)
                
                self.status_display.object = f"**Status:** ✅ Updated symbol list with {len(unique_symbols)} symbols"
            else:
                self.status_display.object = f"**Status:** ℹ️ No symbols detected in data"
                
        except Exception as e:
            logger.error(f"Error updating symbol list: {e}")
            # Don't fail the entire operation if symbol update fails
    
    def refresh_symbol_list(self, event=None):
        """Refresh the symbol list from all loaded datasets"""
        try:
            if not hasattr(self.data_manager, 'core') or not hasattr(self.data_manager.core, 'symbols'):
                self.status_display.object = "**Status:** ❌ Data manager not properly initialized"
                return
            
            # Get all uploaded datasets
            uploaded_datasets = getattr(self.data_manager, 'uploaded_datasets', {})
            if not uploaded_datasets:
                self.status_display.object = "**Status:** ℹ️ No uploaded datasets found"
                return
            
            all_symbols = set()
            
            # Extract symbols from all datasets
            for dataset_id, dataset_info in uploaded_datasets.items():
                if 'data' in dataset_info and dataset_info['data'] is not None:
                    data = dataset_info['data']
                    symbols = self.extract_symbols_from_data(data)
                    all_symbols.update(symbols)
            
            # Update the symbol list
            if all_symbols:
                unique_symbols = sorted(list(all_symbols))
                self.data_manager.core.symbols = unique_symbols
                self.status_display.object = f"**Status:** ✅ Refreshed symbol list with {len(unique_symbols)} symbols"
                logger.info(f"Refreshed symbol list with {len(unique_symbols)} symbols: {unique_symbols}")
            else:
                self.status_display.object = "**Status:** ℹ️ No symbols found in uploaded datasets"
                
        except Exception as e:
            logger.error(f"Error refreshing symbol list: {e}")
            self.status_display.object = f"**Status:** ❌ Error refreshing symbol list: {str(e)}"
    
    def extract_symbols_from_data(self, data):
        """Extract symbols from a dataset"""
        symbols = set()
        
        if data is None or data.empty:
            return symbols
        
        # Look for common symbol column names (prioritize ticker for redline data)
        symbol_columns = ['ticker', 'Ticker', 'TICKER', 'symbol', 'Symbol', 'SYMBOL', 'code', 'Code', 'CODE']
        
        # Check if any column contains symbol data
        for col in data.columns:
            if col in symbol_columns:
                # Found a symbol column
                column_symbols = data[col].dropna().unique().tolist()
                symbols.update(column_symbols)
                logger.info(f"Found symbols in column '{col}': {column_symbols}")
                break
        
        # If no dedicated symbol column, try to infer from other columns
        if not symbols:
            # Look for columns that might contain stock symbols
            for col in data.columns:
                if data[col].dtype == 'object':  # String columns
                    sample_values = data[col].dropna().head(100)
                    if len(sample_values) > 0:
                        # Check if values look like stock symbols (including .US suffix for redline data)
                        symbol_like = sample_values.str.match(r'^[A-Z]{1,5}(\.US)?$')
                        if symbol_like.any():
                            inferred_symbols = sample_values[symbol_like].unique().tolist()
                            symbols.update(inferred_symbols)
                            logger.info(f"Inferred symbols from column '{col}': {inferred_symbols}")
                            break
        
        # Clean and validate symbols - convert ticker to symbol format
        cleaned_symbols = set()
        for symbol in symbols:
            if symbol and isinstance(symbol, str):
                # Remove any extra whitespace and convert to uppercase
                cleaned_symbol = symbol.strip().upper()
                if cleaned_symbol:
                    # Convert ticker format to symbol format if needed
                    # For redline data, ticker might be like 'COIN.US' - keep as is
                    # For other formats, ensure proper symbol format
                    if cleaned_symbol.endswith('.US'):
                        # Keep .US suffix for redline data
                        cleaned_symbols.add(cleaned_symbol)
                    elif len(cleaned_symbol) <= 5 and cleaned_symbol.isalpha():
                        # Standard stock symbol format
                        cleaned_symbols.add(cleaned_symbol)
                    else:
                        # Try to extract valid symbol part
                        import re
                        symbol_match = re.match(r'^([A-Z]{1,5})(\.US)?$', cleaned_symbol)
                        if symbol_match:
                            cleaned_symbols.add(cleaned_symbol)
        
        logger.info(f"Extracted and cleaned symbols: {cleaned_symbols}")
        return cleaned_symbols
    
    def process_data_for_upload(self, data):
        """Process data before upload to convert ticker to symbol format"""
        if data is None or data.empty:
            return data
        
        processed_data = data.copy()
        
        # Check if there's a ticker column that should be converted to symbol
        ticker_columns = ['ticker', 'Ticker', 'TICKER']
        symbol_columns = ['symbol', 'Symbol', 'SYMBOL']
        
        # If we have a ticker column but no symbol column, create a symbol column
        ticker_col = None
        for col in ticker_columns:
            if col in processed_data.columns:
                ticker_col = col
                break
        
        if ticker_col and 'symbol' not in processed_data.columns:
            # Create a symbol column from ticker
            processed_data['symbol'] = processed_data[ticker_col].apply(
                lambda x: self.convert_ticker_to_symbol(x) if pd.notna(x) else x
            )
            logger.info(f"Created 'symbol' column from '{ticker_col}' column")
        
        # Also ensure the ticker column is properly formatted
        if ticker_col:
            processed_data[ticker_col] = processed_data[ticker_col].apply(
                lambda x: self.clean_ticker_value(x) if pd.notna(x) else x
            )
            logger.info(f"Cleaned '{ticker_col}' column values")
        
        return processed_data
    
    def convert_ticker_to_symbol(self, ticker_value):
        """Convert a ticker value to symbol format"""
        if not ticker_value or not isinstance(ticker_value, str):
            return ticker_value
        
        # Clean and standardize the ticker value
        cleaned = ticker_value.strip().upper()
        
        # For redline data with .US suffix, keep as is
        if cleaned.endswith('.US'):
            return cleaned
        
        # For standard stock symbols, ensure proper format
        if len(cleaned) <= 5 and cleaned.isalpha():
            return cleaned
        
        # Try to extract valid symbol part
        import re
        symbol_match = re.match(r'^([A-Z]{1,5})(\.US)?$', cleaned)
        if symbol_match:
            return cleaned
        
        # If no match, return as is
        return cleaned
    
    def clean_ticker_value(self, ticker_value):
        """Clean a ticker value for consistency"""
        if not ticker_value or not isinstance(ticker_value, str):
            return ticker_value
        
        # Remove whitespace and convert to uppercase
        cleaned = ticker_value.strip().upper()
        
        # Ensure proper format
        if cleaned.endswith('.US'):
            return cleaned
        elif len(cleaned) <= 5 and cleaned.isalpha():
            return cleaned
        else:
            return cleaned
    
    def get_component(self):
        """Get the file browser component layout"""
        return pn.Column(
            pn.pane.Markdown("### 📁 File Browser"),
            pn.pane.Markdown("**Browse local directories and load data files**"),
            
            # Navigation controls
            pn.Row(
                self.back_button,
                self.home_button,
                self.refresh_button,
                align='center'
            ),
            
            # Path display and input
            self.path_display,
            self.path_input,
            
            # Directory contents
            pn.pane.Markdown("### 📂 Directory Contents"),
            self.directory_contents,
            
            # File information and actions
            pn.Row(
                pn.Column(
                    pn.pane.Markdown("### 📄 File Information"),
                    self.file_info,
                    pn.Row(
                        self.load_button,
                        self.add_to_data_button,
                        self.refresh_symbols_button,
                        align='center'
                    )
                ),
                pn.Column(
                    pn.pane.Markdown("### 📊 File Preview"),
                    self.file_preview
                ),
                align='start'
            ),
            
            # Status
            self.status_display,
            
            sizing_mode='stretch_width'
        )
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions"""
        return self.supported_extensions.copy()
    
    def set_current_path(self, path: str):
        """Set the current directory path"""
        self.current_path = path
        self.file_history.clear()
        self.load_directory_contents()
