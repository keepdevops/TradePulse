"""
Data Operations
Handles live data fetching and multiple ticker operations for the Data Fetcher.
"""

import time
from typing import Dict, List, Optional
import pandas as pd
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DataOperations:
    """Handles live data fetching and multiple ticker operations."""
    
    def __init__(self, fetcher, message_bus, config):
        """Initialize the data operations."""
        self.fetcher = fetcher
        self.message_bus = message_bus
        self.config = config
        
        # Live feed configuration
        self.live_feed_enabled = config.get('live_feed.enabled', True)
        self.live_feed_endpoint = config.get('live_feed.api_endpoint', '')
        self.update_interval = config.get('live_feed.update_interval', 5)
        self.max_tickers = config.get('live_feed.max_tickers', 100)
    
    def fetch_live_data(self, tickers: List[str]) -> Dict[str, pd.DataFrame]:
        """
        Fetch live data for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
        
        Returns:
            Dictionary mapping tickers to live data DataFrames
        """
        if not self.live_feed_enabled:
            self.fetcher.log_warning("Live feed is disabled")
            return {}
        
        if len(tickers) > self.max_tickers:
            self.fetcher.log_warning(f"Too many tickers requested ({len(tickers)} > {self.max_tickers})")
            tickers = tickers[:self.max_tickers]
        
        live_data = {}
        
        try:
            for ticker in tickers:
                data = self.fetcher.data_sources.fetch_from_live_feed(ticker)
                if data is not None:
                    live_data[ticker] = data
                    
                    # Publish live data update
                    self.message_bus.publish("live_data_updated", {
                        'ticker': ticker,
                        'timestamp': time.time(),
                        'price': data.get('price', {}).iloc[-1] if not data.empty else None
                    })
            
            self.fetcher.log_info(f"Fetched live data for {len(live_data)} tickers")
            
        except Exception as e:
            self.fetcher.log_error(f"Error fetching live data: {e}")
        
        return live_data
    
    def fetch_multiple_tickers(
        self,
        tickers: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple tickers.
        
        Args:
            tickers: List of ticker symbols
            start_date: Start date for historical data
            end_date: End date for historical data
        
        Returns:
            Dictionary mapping tickers to DataFrames
        """
        results = {}
        
        for ticker in tickers:
            data = self.fetcher.fetch_historical_data(ticker, start_date, end_date)
            if data is not None:
                results[ticker] = data
        
        return results
