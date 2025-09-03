# TradePulse Unified Data Access System

## Overview
The Unified Data Access System provides a consistent interface for all modules to access both API data and uploaded data, while maintaining the constraint of keeping each file under 200 lines.

## Architecture

### Core Components

#### 1. DataAccessManager (`ui_components/data_access.py`)
- **Purpose**: Central data access orchestrator
- **Lines**: ~180 lines
- **Features**:
  - Unified API data fetching (Yahoo Finance, Alpha Vantage, IEX Cloud, Mock Data)
  - Caching system with TTL
  - Combined data access (API + Uploaded)
  - Error handling and logging

#### 2. ModuleDataAccess (`ui_components/module_data_access.py`)
- **Purpose**: Module-specific data access wrapper
- **Lines**: ~150 lines
- **Features**:
  - Module-specific data access
  - Dataset activation/deactivation
  - Data summary and statistics
  - Cache management

#### 3. DataManager (`ui_components/data_manager.py`)
- **Purpose**: Core data storage and management
- **Lines**: ~330 lines (existing)
- **Features**:
  - Uploaded dataset storage
  - Dataset registry and metadata
  - Module-specific data access permissions

## Usage Examples

### For Data Panel
```python
# Get API data
api_data = self.data_access.get_api_data(['AAPL', 'GOOGL'], 'yahoo', '1d')

# Get uploaded data
uploaded_data = self.data_access.get_uploaded_data(['dataset_123'])

# Get combined data
combined_data = self.data_access.get_combined_data(
    symbols=['AAPL', 'GOOGL'],
    dataset_ids=['dataset_123', 'dataset_456'],
    source='yahoo'
)
```

### For Portfolio Panel
```python
# Activate a dataset for portfolio analysis
self.data_access.activate_dataset('dataset_portfolio_data')

# Get active datasets
active_data = self.data_access.get_active_datasets()

# Get available datasets
available = self.data_access.get_available_datasets()
```

### For AI Panel
```python
# Get training data from multiple sources
training_data = self.data_access.get_combined_data(
    symbols=['AAPL', 'GOOGL', 'MSFT'],
    dataset_ids=['dataset_technical_indicators'],
    source='yahoo'
)
```

## Data Sources

### API Sources
1. **Yahoo Finance** (`yahoo`)
   - Real-time and historical data
   - Multiple timeframes
   - Free tier available

2. **Alpha Vantage** (`alpha_vantage`)
   - Technical indicators
   - Fundamental data
   - API key required

3. **IEX Cloud** (`iex`)
   - Real-time quotes
   - Financial statements
   - API key required

4. **Mock Data** (`mock`)
   - Generated test data
   - Consistent across runs
   - No API dependencies

### Uploaded Data Sources
- **Feather** (.feather)
- **CSV** (.csv)
- **JSON** (.json)
- **Excel** (.xlsx/.xls)
- **Parquet** (.parquet)
- **SQLite** (.db/.sqlite)
- **DuckDB** (.duckdb)

## Module Integration

### Updated Panels
1. **Data Panel** - Uses unified data access for fetching and displaying data
2. **Portfolio Panel** - Uses unified data access for portfolio analysis
3. **AI Panel** - Uses unified data access for model training data
4. **Charts Panel** - Uses unified data access for visualization data
5. **Alerts Panel** - Uses unified data access for alert conditions
6. **Models Panel** - Uses unified data access for model evaluation

### Benefits
- **Consistency**: All modules use the same data access interface
- **Flexibility**: Easy to switch between data sources
- **Caching**: Built-in caching reduces API calls
- **Error Handling**: Centralized error handling and logging
- **Scalability**: Easy to add new data sources
- **Maintainability**: Each component under 200 lines

## File Structure
```
ui_components/
├── data_access.py          # Main data access orchestrator (~180 lines)
├── module_data_access.py   # Module-specific wrapper (~150 lines)
└── data_manager.py         # Core data storage (~330 lines)

modular_panels/
├── data_panel.py           # Updated to use unified access
├── portfolio_panel.py      # Updated to use unified access
├── ai_panel.py            # Updated to use unified access
├── charts_panel.py        # Updated to use unified access
├── alerts_panel.py        # Updated to use unified access
└── models_panel.py        # Updated to use unified access
```

## Configuration

### Data Source Configuration
```python
# In data_access.py
self.api_sources = {
    'yahoo': self._fetch_yahoo_data,
    'alpha_vantage': self._fetch_alpha_vantage_data,
    'iex': self._fetch_iex_data,
    'mock': self._generate_mock_data
}
```

### Cache Configuration
```python
# Cache TTL in seconds
self.cache_ttl = 300  # 5 minutes

# Clear cache
data_access_manager.clear_cache()
```

### Module Permissions
```python
# In data_manager.py
self.module_data_access = {
    'portfolio': ['price_data', 'uploaded_datasets'],
    'models': ['price_data', 'uploaded_datasets'],
    'ai': ['price_data', 'uploaded_datasets', 'ml_predictions'],
    'charts': ['price_data', 'uploaded_datasets'],
    'alerts': ['price_data', 'uploaded_datasets', 'alerts'],
    'system': ['uploaded_datasets', 'system_metrics']
}
```

## Future Enhancements
1. **Real-time Data**: WebSocket connections for live data
2. **Data Validation**: Schema validation for uploaded data
3. **Data Transformation**: Built-in data cleaning and preprocessing
4. **Advanced Caching**: Redis-based distributed caching
5. **Data Versioning**: Version control for datasets
6. **API Rate Limiting**: Intelligent rate limiting for API calls
