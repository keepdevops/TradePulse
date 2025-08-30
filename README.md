# TradePulse

A comprehensive desktop application for stock market analysis, trading, and portfolio management designed for day traders and financial analysts.

## Features

- **Data Grid**: Historical data from Redline utility and live feed data
- **Models Grid**: ML models (ADM, CIPO, BICIPO) with performance metrics
- **AI Module**: AI-driven trading strategies and risk management
- **Message Bus**: ZeroMQ-based inter-module communication
- **Multi-asset Support**: Stocks, currencies, cryptocurrencies, and commodities

## Architecture

- Modular, multi-process architecture
- Each module operates as standalone application
- Centralized Message Bus for communication
- Grid-based UI with interactive visualizations
- M3 Silicon (ARM64) optimized

## Quick Start

### Prerequisites

- Python 3.12+
- Conda or Mamba
- PostgreSQL (optional, for remote storage)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd TradePulse
```

2. Create conda environment:
```bash
mamba env create -f environment.yml
conda activate tradepulse
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure the application:
```bash
# Edit config.json with your settings
```

5. Run the application:
```bash
python main.py
```

## Module Structure

```
TradePulse/
├── main.py                 # Main application entry point
├── module_manager.py       # Module management and orchestration
├── config.json            # Configuration file
├── data_grid/            # Data collection and visualization
├── models_grid/          # ML models and predictions
├── ai_module/            # AI trading strategies
├── utils/                # Shared utilities
├── tests/                # Test suite
└── docker-compose.yml    # Docker orchestration
```

## Running Modules

### 🚀 **Full Application (Recommended)**
```bash
python main.py
```
This launches the complete TradePulse system with all modules running.

### 📊 **Individual Modules**

#### **Data Grid** (Data Fetching & Visualization)
```bash
python -m data_grid
```
**What it does:**
- Fetches historical and live market data
- Creates interactive charts (candlestick, line, volume)
- Exports data to various formats (CSV, Excel, JSON)
- Manages data sources and caching

#### **Models Grid** (Machine Learning Models)
```bash
python -m models_grid
```
**What it does:**
- Trains and evaluates ML models (ADM, CIPO, BICIPO)
- Generates predictions and performance metrics
- Manages model selection and feature importance
- Provides model comparison and analysis

#### **AI Module** (Trading Strategies)
```bash
python -m ai_module
```
**What it does:**
- Generates AI-driven trading strategies
- Manages risk assessment and position sizing
- Optimizes portfolio allocation
- Analyzes market conditions and confidence scores

### 🧪 **Testing**

#### **Run All Tests**
```bash
python -m pytest tests/
```

#### **Run Specific Test Files**
```bash
python -m pytest tests/test_integration.py
python -m pytest tests/test_components.py
python -m pytest tests/test_utilities.py
```

#### **Run Tests with Coverage**
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

### 🐳 **Docker (Alternative)**

#### **Start All Services**
```bash
docker-compose up
```

#### **Start Specific Services**
```bash
docker-compose up data_grid models_grid ai_module
```

#### **Run in Background**
```bash
docker-compose up -d
```

#### **View Logs**
```bash
docker-compose logs -f
```

## Configuration

Edit `config.json` to configure:
- Database connections (SQLite, PostgreSQL, DuckDB)
- API keys and data sources
- ML model parameters
- Trading parameters
- Visualization preferences
- Alert thresholds

## Module Communication

All modules communicate through the Message Bus:
- **Publish/Subscribe** pattern using ZeroMQ
- **Heartbeat monitoring** for health checks
- **Automatic reconnection** on failures
- **Message queuing** for reliability

## Development

### **Code Structure**
- Maximum 200 lines per file (enforced)
- Shared utilities in `utils/` directory
- Consolidated performance metrics
- No duplicate code across modules

### **Adding New Modules**
1. Create module directory with `__init__.py`
2. Implement `__main__.py` entry point
3. Add to `module_manager.py`
4. Update `config.json` if needed

### **Running in Development Mode**
```bash
# Set environment variable for development
export TRADEPULSE_DEV=1

# Run with debug logging
python -m data_grid --debug
```

## Troubleshooting

### **Common Issues**

1. **Module Connection Failed**
   - Check Message Bus is running
   - Verify network ports (default: 5555-5560)
   - Check firewall settings

2. **Database Connection Error**
   - Verify database credentials in `config.json`
   - Check database service is running
   - Test connection manually

3. **ML Model Training Fails**
   - Check available memory
   - Verify data quality and format
   - Check model parameters in config

### **Logs and Debugging**
```bash
# View application logs
tail -f logs/tradepulse.log

# Run with verbose output
python main.py --verbose

# Check module health
python module_manager.py --health-check
```

## Performance

### **System Requirements**
- **Minimum**: 8GB RAM, 4 CPU cores
- **Recommended**: 16GB RAM, 8 CPU cores
- **Storage**: 10GB+ for data and models
- **Network**: Stable internet for live data

### **Optimization Tips**
- Use SSD storage for database
- Enable data caching in config
- Adjust ML model complexity
- Monitor memory usage

## License

[License information]

## Support

For issues and questions, please refer to the documentation or create an issue in the repository.
