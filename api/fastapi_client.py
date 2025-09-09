#!/usr/bin/env python3
"""
TradePulse FastAPI Client
Client for connecting to TradePulse FastAPI server
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from .fastapi_client_core import fastapi_client_core
from .fastapi_client_sync import fastapi_client_sync

logger = logging.getLogger(__name__)

class TradePulseAPIClient:
    """FastAPI client for TradePulse API server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.core = fastapi_client_core
        self.core.base_url = base_url
        self.sync = fastapi_client_sync
        self.sync.client.base_url = base_url
    
    async def __aenter__(self):
        """Async context manager entry"""
        return await self.core.__aenter__()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        return await self.core.__aexit__(exc_type, exc_val, exc_tb)
    
    # Delegate all async methods to core
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        return await self.core._make_request(method, endpoint, data)
    
    async def health_check(self) -> Dict:
        return await self.core.health_check()
    
    async def get_system_status(self) -> Dict:
        return await self.core.get_system_status()
    
    async def get_system_metrics(self) -> Dict:
        return await self.core.get_system_metrics()
    
    async def get_available_symbols(self) -> Dict:
        return await self.core.get_available_symbols()
    
    async def fetch_market_data(self, symbol: str, timeframe: str = "1d", 
                              start_date: Optional[str] = None, end_date: Optional[str] = None,
                              data_source: str = "yahoo") -> Dict:
        return await self.core.fetch_market_data(symbol, timeframe, start_date, end_date, data_source)
    
    async def get_market_data(self, symbol: str, timeframe: str = "1d") -> Dict:
        return await self.core.get_market_data(symbol, timeframe)
    
    async def get_available_models(self) -> Dict:
        return await self.core.get_available_models()
    
    async def train_model(self, model_name: str, symbol: str, parameters: Optional[Dict] = None) -> Dict:
        return await self.core.train_model(model_name, symbol, parameters)
    
    async def make_prediction(self, symbol: str, model_name: str, features: Optional[Dict] = None) -> Dict:
        return await self.core.make_prediction(symbol, model_name, features)
    
    async def get_portfolio_status(self) -> Dict:
        return await self.core.get_portfolio_status()
    
    async def optimize_portfolio(self, symbols: List[str], weights: Optional[List[float]] = None,
                               risk_tolerance: str = "medium") -> Dict:
        return await self.core.optimize_portfolio(symbols, weights, risk_tolerance)
    
    async def get_alerts(self) -> Dict:
        return await self.core.get_alerts()
    
    async def create_alert(self, symbol: str, alert_type: str, threshold: float, condition: str) -> Dict:
        return await self.core.create_alert(symbol, alert_type, threshold, condition)
    
    async def delete_alert(self, alert_id: str) -> Dict:
        return await self.core.delete_alert(alert_id)

# Example usage
async def example_usage():
    """Example of how to use the FastAPI client"""
    async with TradePulseAPIClient() as client:
        try:
            # Check health
            health = await client.health_check()
            logger.info(f"API Health: {health}")
            
            # Fetch market data
            data = await client.fetch_market_data("AAPL", "1d", data_source="yahoo")
            logger.info(f"Market Data: {data}")
            
            # Make prediction
            prediction = await client.make_prediction("AAPL", "linear_regression")
            logger.info(f"Prediction: {prediction}")
            
            # Optimize portfolio
            portfolio = await client.optimize_portfolio(["AAPL", "GOOGL", "MSFT"])
            logger.info(f"Portfolio: {portfolio}")
            
            # Create alert
            alert = await client.create_alert("AAPL", "price", 150.0, "above")
            logger.info(f"Alert: {alert}")
            
        except Exception as e:
            logger.error(f"Example usage failed: {e}")

# Export the sync client class
TradePulseAPIClientSync = fastapi_client_sync.__class__

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
