# 📁 TradePulse File Browser Component

## Overview

The TradePulse File Browser Component provides a comprehensive file browsing interface that allows users to navigate local PC directories and load data files directly into the TradePulse application. This component is designed to work seamlessly with the existing data management system.

## Features

### 🎯 Core Functionality
- **Directory Navigation**: Browse local directories with intuitive navigation
- **File Preview**: Preview data files before loading
- **Multiple Format Support**: Support for CSV, JSON, Excel, Feather, Parquet, and database files
- **File Information**: Display detailed file information including size, modification date, and format
- **Data Loading**: Load files directly into the TradePulse data manager
- **History Navigation**: Navigate back through visited directories

### 📊 Supported File Formats
- **CSV Files** (.csv) - Comma-separated values
- **JSON Files** (.json) - JavaScript Object Notation
- **Excel Files** (.xlsx, .xls) - Microsoft Excel spreadsheets
- **Feather Files** (.feather) - Fast binary format for data frames
- **Parquet Files** (.parquet) - Columnar storage format
- **Database Files** (.db, .sqlite, .duckdb) - SQLite and DuckDB databases
- **HDF5 Files** (.h5, .hdf5) - Hierarchical Data Format
- **Pickle Files** (.pkl, .pickle) - Python serialized objects

### 🎨 User Interface
- **Visual File Icons**: Different icons for different file types
- **File Size Display**: Human-readable file sizes (B, KB, MB, GB, TB)
- **Date Information**: File creation and modification dates
- **Status Updates**: Real-time status messages
- **Responsive Design**: Adapts to different screen sizes

## Usage

### Accessing the File Browser

#### Method 1: Through TradePulse Panel UI
1. Launch the TradePulse application: `python launch_panel_local.py`
2. Navigate to the **Data Panel**
3. Click on the **"📁 File Browser"** tab
4. Start browsing your local directories

#### Method 2: Standalone File Browser
1. Launch the standalone file browser: `python launch_file_browser.py`
2. Access directly at: http://localhost:5006

### Navigation Controls

#### 🏠 Home Button
- Click to return to your home directory
- Clears navigation history

#### ⬅️ Back Button
- Navigate to the previous directory
- Maintains navigation history
- Disabled when no history available

#### 🔄 Refresh Button
- Reload the current directory contents
- Useful for detecting new files

#### 📁 Path Input
- Manually enter a directory path
- Press Enter to navigate
- Supports both relative and absolute paths

### File Operations

#### Selecting Files
1. Click on a file in the directory contents table
2. File information will be displayed
3. A preview of the file will be loaded automatically
4. Action buttons will be enabled

#### Loading Files
1. Select a supported data file
2. Click **"📊 Load File"** to load the full file into memory
3. The file preview will be updated with more data
4. Status will show loading progress

#### Adding to Data Manager
1. Load a file using the **"📊 Load File"** button
2. Click **"➕ Add to Data Manager"** to add it to TradePulse's data manager
3. The file will be available for use in other panels
4. A dataset ID will be assigned and displayed

### File Preview Features

#### Data Files
- Shows first 10 rows of data
- Displays column names and data types
- Handles large files efficiently

#### Database Files
- Shows available tables
- Allows exploration of database structure
- Loads first table by default

#### Unsupported Files
- Shows basic file information
- Displays file size and type
- Indicates that preview is not available

## Integration with TradePulse

### Data Manager Integration
The File Browser Component integrates seamlessly with TradePulse's data management system:

```python
# Example: Adding a file to the data manager
dataset_id = data_manager.add_uploaded_data(filename, loaded_data, metadata)
```

### Callback Support
The component supports custom callbacks for file selection:

```python
def on_file_selected(file_path, data):
    # Custom handling when a file is selected
    print(f"File selected: {file_path}")
    print(f"Data shape: {data.shape}")

file_browser = FileBrowserComponent(data_manager, on_file_select=on_file_selected)
```

### API Access
Access the file browser component programmatically:

```python
# From the data panel
data_panel = DataPanelCore(data_manager)
file_browser = data_panel.get_file_browser()

# Set a specific directory
file_browser.set_current_path("/path/to/data")

# Get supported extensions
extensions = file_browser.get_supported_extensions()
```

## Technical Details

### Component Structure
```
FileBrowserComponent
├── Navigation Controls
│   ├── Back Button
│   ├── Home Button
│   ├── Refresh Button
│   └── Path Input
├── Directory Contents
│   ├── File/Directory Table
│   └── Selection Handling
├── File Information
│   ├── File Details Display
│   └── Status Updates
├── File Preview
│   ├── Data Preview Table
│   └── Format Detection
└── Action Buttons
    ├── Load File
    └── Add to Data Manager
```

### Error Handling
- **Permission Errors**: Gracefully handles inaccessible directories
- **File Format Errors**: Provides clear error messages for unsupported formats
- **Network Errors**: Handles file system access issues
- **Memory Errors**: Manages large file loading efficiently

### Performance Features
- **Lazy Loading**: Only loads file previews when needed
- **Pagination**: Handles large directories efficiently
- **Caching**: Maintains directory contents for faster navigation
- **Memory Management**: Efficient handling of large data files

## Configuration

### Supported Extensions
Customize supported file extensions:

```python
file_browser.supported_extensions = [
    '.csv', '.json', '.feather', '.parquet', 
    '.duckdb', '.db', '.sqlite', '.xlsx', '.xls'
]
```

### File Size Limits
The component handles files of various sizes:
- **Small Files** (< 1MB): Loaded immediately
- **Medium Files** (1MB - 100MB): Loaded with progress indication
- **Large Files** (> 100MB): Loaded with memory management

### Directory Starting Point
Set the initial directory:

```python
file_browser.set_current_path("/path/to/start/directory")
```

## Troubleshooting

### Common Issues

#### "Path does not exist" Error
- Verify the path is correct
- Check file permissions
- Ensure the directory is accessible

#### "Unsupported file type" Error
- Check if the file extension is supported
- Verify the file is not corrupted
- Try opening the file in another application

#### "Permission denied" Error
- Check file system permissions
- Ensure you have read access to the directory
- Try running with appropriate permissions

#### "Memory error" Error
- Close other applications to free memory
- Try loading a smaller file first
- Consider using the M3 File Browser for very large files

### Performance Tips
1. **Use SSD Drives**: Faster file access and loading
2. **Close Unused Applications**: Free up system memory
3. **Organize Files**: Keep data files in dedicated directories
4. **Use Appropriate Formats**: Choose efficient formats for large datasets

## Development

### Adding New File Formats
To add support for new file formats:

1. Add the extension to `supported_extensions`
2. Implement loading logic in `load_file_preview` and `load_selected_file`
3. Add appropriate file type icons
4. Update documentation

### Customizing the Interface
The component uses Panel widgets and can be customized:
- Modify the layout in `get_component`
- Add new controls to `create_components`
- Customize styling with CSS classes

### Testing
Test the component with various file types:
- Small and large files
- Different file formats
- Various directory structures
- Error conditions

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error logs
3. Test with different file types
4. Contact the development team

---

**Version**: 1.0.0  
**Last Updated**: September 3, 2025  
**Compatibility**: TradePulse v10.9+
