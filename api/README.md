# TradePulse FastAPI Integration

High-performance API server for TradePulse modular trading system using FastAPI.

## Features

- **RESTful API**: Modern REST API with automatic documentation
- **Async Support**: Full async/await support for high performance
- **Data Validation**: Pydantic models for request/response validation
- **Modular Design**: Organized endpoint modules under 200 lines each
- **Background Tasks**: Support for long-running operations
- **CORS Support**: Cross-origin resource sharing enabled
- **Error Handling**: Comprehensive error handling and logging

## Quick Start

### Install Dependencies

#### Option 1: Using Conda (Recommended)

**macOS/Linux:**
```bash
./install_fastapi_conda.sh
```

**Windows:**
```cmd
install_fastapi_conda.bat
```

**Manual conda installation:**
```bash
conda env create -f environment_fastapi.yml
conda activate tradepulse-fastapi
```

#### Option 2: Using pip

```bash
pip install -r requirements_fastapi.txt
```

### Start the API Server

**If using conda:**
```bash
conda activate tradepulse-fastapi
python launch_fastapi_server.py
```

**If using pip:**
```bash
python launch_fastapi_server.py
```

The server will be available at:
- **API**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Use the API Client

```python
from api.fastapi_client import TradePulseAPIClientSync

# Create client
client = TradePulseAPIClientSync()

# Check server health
health = client.health_check()
print(f"Server health: {health}")

# Fetch market data
data = client.fetch_market_data("AAPL", "1d", data_source="yahoo")
print(f"Market data: {data}")

# Make prediction
prediction = client.make_prediction("AAPL", "linear_regression")
print(f"Prediction: {prediction}")

# Scan M3 drive for redline data
scan_result = client.scan_m3_drive("/Volumes")
print(f"M3 Drive Scan: {scan_result}")

# Import file from M3 drive
import_result = client.import_from_m3_drive("/path/to/redline_data.csv", "redline")
print(f"Import Result: {import_result}")

## API Endpoints

### Data Endpoints
- `GET /api/v1/data/symbols` - Get available symbols
- `POST /api/v1/data/fetch` - Fetch market data
- `GET /api/v1/data/{symbol}` - Get cached market data

### Model Endpoints
- `GET /api/v1/models` - Get available models
- `POST /api/v1/models/predict` - Make predictions
- `POST /api/v1/models/train` - Train models (background)

### Portfolio Endpoints
- `POST /api/v1/portfolio/optimize` - Optimize portfolio
- `GET /api/v1/portfolio/{id}` - Get portfolio details
- `GET /api/v1/portfolio` - Get all portfolios

### Alert Endpoints
- `POST /api/v1/alerts/create` - Create alerts
- `GET /api/v1/alerts` - Get all alerts
- `DELETE /api/v1/alerts/{id}` - Delete alerts

### System Endpoints
- `GET /api/v1/system/status` - Get system status
- `GET /api/v1/system/metrics` - Get system metrics
- `POST /api/v1/system/restart` - Restart system

### File Upload Endpoints
- `POST /api/v1/files/upload` - Upload file to TradePulse
- `GET /api/v1/files/m3-drive/scan` - Scan M3 hard drive for data files
- `POST /api/v1/files/m3-drive/import` - Import file from M3 hard drive
- `GET /api/v1/files/files` - List uploaded files
- `GET /api/v1/files/files/{file_id}` - Get file information
- `DELETE /api/v1/files/files/{file_id}` - Delete uploaded file

## Architecture

```
api/
├── fastapi_server.py      # Main server (under 200 lines)
├── fastapi_client.py      # API client (under 200 lines)
├── models.py              # Pydantic models
├── endpoints/             # Modular endpoints
│   ├── data_endpoints.py
│   ├── model_endpoints.py
│   ├── portfolio_endpoints.py
│   ├── alert_endpoints.py
│   ├── system_endpoints.py
│   └── file_upload_endpoints.py
├── upload_redline_data.py # Redline data upload utility
├── environment_fastapi.yml # Conda environment file
├── install_fastapi_conda.sh # Conda installation script (macOS/Linux)
├── install_fastapi_conda.bat # Conda installation script (Windows)
└── README.md
```

## Development

### Adding New Endpoints

1. Create a new endpoint module in `api/endpoints/`
2. Keep it under 200 lines
3. Add the router to `fastapi_server.py`
4. Update this README

### Testing

```bash
# Test the API
curl http://localhost:8000/health

# Test data fetching
curl -X POST http://localhost:8000/api/v1/data/fetch \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "timeframe": "1d"}'

# Test M3 drive scanning
curl http://localhost:8000/api/v1/files/m3-drive/scan?path=/Volumes

# Test file import
curl -X POST http://localhost:8000/api/v1/files/m3-drive/import \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/redline_data.csv", "file_type": "redline"}'
```

### Redline Data Upload

Use the interactive upload utility:

```bash
python upload_redline_data.py
```

This utility will:
1. Scan common M3 drive locations for data files
2. Display found files by type (CSV, JSON, Feather, etc.)
3. Allow interactive file selection and import
4. Copy files to TradePulse redline_data directory

## Integration with TradePulse

The FastAPI server can be integrated with the existing TradePulse Panel UI by:

1. Using the API client in panel components
2. Replacing direct data access with API calls
3. Adding API status monitoring to the System panel

## Production Deployment

For production deployment:

1. Use proper database instead of in-memory storage
2. Configure CORS origins appropriately
3. Add authentication and authorization
4. Use environment variables for configuration
5. Set up proper logging and monitoring
