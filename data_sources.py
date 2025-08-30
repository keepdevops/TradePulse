"""
Data Sources
Contains the implementation logic for different data sources.
"""

import pandas as pd
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from utils.logger import LoggerMixin
from utils.database import Database
from utils.config_loader import ConfigLoader


class DataSources(LoggerMixin):
    """
    Implementation class for different data sources.
    
    This class contains all the data source-specific logic that was moved
    from the main DataFetcher to keep files under 400 lines.
    """
    
    def __init__(self, config: ConfigLoader, database: Database):
        """
        Initialize the data sources.
        
        Args:
            config: Configuration loader instance
            database: Database instance
        """
        super().__init__()
        self.config = config
        self.database = database
        
        # Redline configuration
        self.redline_path = config.get('redline.data_path', './data/redline_data.duckdb')
        self.redline_format = config.get('redline.output_format', 'duckdb')
        
        self.log_info("Data Sources initialized")
    
    def fetch_from_redline(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[pd.DataFrame]:
        """Fetch data from Redline utility."""
        try:
            if self.redline_format == 'duckdb':
                return self._fetch_from_duckdb(ticker, start_date, end_date)
            elif self.redline_format == 'sqlite':
                return self._fetch_from_sqlite(ticker, start_date, end_date)
            elif self.redline_format == 'json':
                return self._fetch_from_json(ticker, start_date, end_date)
            else:
                self.log_warning(f"Unsupported Redline format: {self.redline_format}")
                return None
                
        except Exception as e:
            self.log_error(f"Error fetching from Redline: {e}")
            return None
    
    def _fetch_from_duckdb(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[pd.DataFrame]:
        """Fetch data from DuckDB (Redline output)."""
        try:
            # Build query
            query = f"SELECT * FROM stock_data WHERE ticker = '{ticker}'"
            
            if start_date:
                query += f" AND date >= '{start_date}'"
            if end_date:
                query += f" AND date <= '{end_date}'"
            
            query += " ORDER BY date"
            
            # Execute query
            data = self.database.execute_query(query)
            
            if not data.empty:
                # Ensure required columns exist
                required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
                missing_columns = [col for col in required_columns if col not in data.columns]
                
                if missing_columns:
                    self.log_warning(f"Missing columns for {ticker}: {missing_columns}")
                
                # Convert date column to datetime if needed
                if 'date' in data.columns:
                    data['date'] = pd.to_datetime(data['date'])
                
                return data
            
            return None
            
        except Exception as e:
            self.log_error(f"Error fetching from DuckDB: {e}")
            return None
    
    def _fetch_from_sqlite(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[pd.DataFrame]:
        """Fetch data from SQLite (Redline output)."""
        # Similar to DuckDB but with SQLite-specific handling
        return self._fetch_from_duckdb(ticker, start_date, end_date)
    
    def _fetch_from_json(self, ticker: str, start_date: Optional[str], end_date: Optional[str]) -> Optional[pd.DataFrame]:
        """Fetch data from JSON (Redline output)."""
        try:
            # Read JSON file
            json_path = Path(self.redline_path)
            if not json_path.exists():
                self.log_warning(f"JSON file not found: {json_path}")
                return None
            
            with open(json_path, 'r') as f:
                json_data = json.load(f)
            
            # Filter data for ticker
            ticker_data = [row for row in json_data if row.get('ticker') == ticker]
            
            if not ticker_data:
                return None
            
            # Convert to DataFrame
            data = pd.DataFrame(ticker_data)
            
            # Filter by date if specified
            if start_date or end_date:
                if 'date' in data.columns:
                    data['date'] = pd.to_datetime(data['date'])
                    
                    if start_date:
                        data = data[data['date'] >= start_date]
                    if end_date:
                        data = data[data['date'] <= end_date]
            
            return data.sort_values('date') if not data.empty else None
            
        except Exception as e:
            self.log_error(f"Error fetching from JSON: {e}")
            return None
    
    def fetch_from_live_feed(self, ticker: str) -> Optional[pd.DataFrame]:
        """Fetch live data from configured API endpoint."""
        try:
            # This is a placeholder for actual API integration
            # In a real implementation, you would connect to the configured API
            
            # Mock live data for demonstration
            current_time = datetime.now()
            mock_data = pd.DataFrame({
                'timestamp': [current_time],
                'ticker': [ticker],
                'price': [100.0 + (hash(ticker) % 100)],  # Mock price
                'volume': [1000],
                'bid': [99.5],
                'ask': [100.5]
            })
            
            return mock_data
            
        except Exception as e:
            self.log_error(f"Error fetching live data for {ticker}: {e}")
            return None
    
    def get_available_tickers(self) -> List[str]:
        """Get list of available tickers from Redline data."""
        try:
            if self.redline_format == 'duckdb':
                query = "SELECT DISTINCT ticker FROM stock_data ORDER BY ticker"
            else:
                # For other formats, we'd need to implement accordingly
                return []
            
            result = self.database.execute_query(query)
            return result['ticker'].tolist() if not result.empty else []
            
        except Exception as e:
            self.log_error(f"Error getting available tickers: {e}")
            return []
