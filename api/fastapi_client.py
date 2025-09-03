#!/usr/bin/env python3
"""
TradePulse FastAPI Client
Client for connecting to TradePulse FastAPI server
"""

import aiohttp
import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class TradePulseAPIClient:
    """FastAPI client for TradePulse API server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession(headers=self.headers)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                async with self.session.get(url) as response:
                    return await response.json()
            elif method.upper() == "POST":
                async with self.session.post(url, json=data) as response:
                    return await response.json()
            elif method.upper() == "DELETE":
                async with self.session.delete(url) as response:
                    return await response.json()
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
        except aiohttp.ClientError as e:
            logger.error(f"❌ API request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e}")
            raise
    
    # Health and status endpoints
    async def health_check(self) -> Dict:
        """Check API server health"""
        return await self._make_request("GET", "/health")
    
    async def get_system_status(self) -> Dict:
        """Get system status"""
        return await self._make_request("GET", "/api/v1/system/status")
    
    async def get_system_metrics(self) -> Dict:
        """Get system metrics"""
        return await self._make_request("GET", "/api/v1/system/metrics")
    
    # Data endpoints
    async def get_available_symbols(self) -> Dict:
        """Get list of available symbols"""
        return await self._make_request("GET", "/api/v1/data/symbols")
    
    async def fetch_market_data(self, symbol: str, timeframe: str = "1d", 
                              start_date: Optional[str] = None, end_date: Optional[str] = None,
                              data_source: str = "yahoo") -> Dict:
        """Fetch market data for a symbol"""
        data = {
            "symbol": symbol,
            "timeframe": timeframe,
            "data_source": data_source
        }
        
        if start_date:
            data["start_date"] = start_date
        if end_date:
            data["end_date"] = end_date
        
        return await self._make_request("POST", "/api/v1/data/fetch", data)
    
    async def get_market_data(self, symbol: str, timeframe: str = "1d") -> Dict:
        """Get cached market data for a symbol"""
        return await self._make_request("GET", f"/api/v1/data/{symbol}?timeframe={timeframe}")
    
    # Model endpoints
    async def get_available_models(self) -> Dict:
        """Get list of available models"""
        return await self._make_request("GET", "/api/v1/models")
    
    async def make_prediction(self, symbol: str, model_name: str, features: Optional[Dict] = None) -> Dict:
        """Make a prediction using a model"""
        data = {
            "symbol": symbol,
            "model_name": model_name,
            "features": features or {}
        }
        
        return await self._make_request("POST", "/api/v1/models/predict", data)
    
    async def train_model(self, model_name: str) -> Dict:
        """Train a model"""
        return await self._make_request("POST", f"/api/v1/models/train?model_name={model_name}")
    
    # Portfolio endpoints
    async def optimize_portfolio(self, symbols: List[str], weights: Optional[List[float]] = None,
                               risk_tolerance: str = "medium") -> Dict:
        """Optimize portfolio allocation"""
        data = {
            "symbols": symbols,
            "risk_tolerance": risk_tolerance
        }
        
        if weights:
            data["weights"] = weights
        
        return await self._make_request("POST", "/api/v1/portfolio/optimize", data)
    
    async def get_portfolio(self, portfolio_id: str) -> Dict:
        """Get portfolio details"""
        return await self._make_request("GET", f"/api/v1/portfolio/{portfolio_id}")
    
    # Alert endpoints
    async def create_alert(self, symbol: str, alert_type: str, threshold: float, condition: str) -> Dict:
        """Create a new alert"""
        data = {
            "symbol": symbol,
            "alert_type": alert_type,
            "threshold": threshold,
            "condition": condition
        }
        
        return await self._make_request("POST", "/api/v1/alerts/create", data)
    
    async def get_alerts(self, status: Optional[str] = None) -> Dict:
        """Get all alerts"""
        endpoint = "/api/v1/alerts"
        if status:
            endpoint += f"?status={status}"
        
        return await self._make_request("GET", endpoint)
    
    async def delete_alert(self, alert_id: str) -> Dict:
        """Delete an alert"""
        return await self._make_request("DELETE", f"/api/v1/alerts/{alert_id}")
    
    # File upload endpoints
    async def scan_m3_drive(self, path: str = "/Volumes") -> Dict:
        """Scan M3 hard drive for data files"""
        return await self._make_request("GET", f"/api/v1/files/m3-drive/scan?path={path}")
    
    async def import_from_m3_drive(self, file_path: str, file_type: str = "upload") -> Dict:
        """Import file from M3 hard drive"""
        data = {
            "file_path": file_path,
            "file_type": file_type
        }
        return await self._make_request("POST", "/api/v1/files/m3-drive/import", data)
    
    async def list_uploaded_files(self, file_type: Optional[str] = None) -> Dict:
        """List uploaded files"""
        endpoint = "/api/v1/files/files"
        if file_type:
            endpoint += f"?file_type={file_type}"
        return await self._make_request("GET", endpoint)
    
    async def get_file_info(self, file_id: str) -> Dict:
        """Get file information"""
        return await self._make_request("GET", f"/api/v1/files/files/{file_id}")
    
    async def delete_file(self, file_id: str) -> Dict:
        """Delete uploaded file"""
        return await self._make_request("DELETE", f"/api/v1/files/files/{file_id}")

# Utility functions for synchronous usage
class TradePulseAPIClientSync:
    """Synchronous wrapper for TradePulse API client"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = TradePulseAPIClient(base_url)
    
    def _run_async(self, coro):
        """Run async coroutine in sync context"""
        return asyncio.run(coro)
    
    def health_check(self) -> Dict:
        """Check API server health"""
        async def _health():
            async with self.client as client:
                return await client.health_check()
        return self._run_async(_health())
    
    def fetch_market_data(self, symbol: str, timeframe: str = "1d", 
                         start_date: Optional[str] = None, end_date: Optional[str] = None,
                         data_source: str = "yahoo") -> Dict:
        """Fetch market data for a symbol"""
        async def _fetch():
            async with self.client as client:
                return await client.fetch_market_data(symbol, timeframe, start_date, end_date, data_source)
        return self._run_async(_fetch())
    
    def make_prediction(self, symbol: str, model_name: str, features: Optional[Dict] = None) -> Dict:
        """Make a prediction using a model"""
        async def _predict():
            async with self.client as client:
                return await client.make_prediction(symbol, model_name, features)
        return self._run_async(_predict())
    
    def optimize_portfolio(self, symbols: List[str], weights: Optional[List[float]] = None,
                         risk_tolerance: str = "medium") -> Dict:
        """Optimize portfolio allocation"""
        async def _optimize():
            async with self.client as client:
                return await client.optimize_portfolio(symbols, weights, risk_tolerance)
        return self._run_async(_optimize())
    
    def create_alert(self, symbol: str, alert_type: str, threshold: float, condition: str) -> Dict:
        """Create a new alert"""
        async def _create():
            async with self.client as client:
                return await client.create_alert(symbol, alert_type, threshold, condition)
        return self._run_async(_create())
    
    # File upload sync methods
    def scan_m3_drive(self, path: str = "/Volumes") -> Dict:
        """Scan M3 hard drive for data files"""
        async def _scan():
            async with self.client as client:
                return await client.scan_m3_drive(path)
        return self._run_async(_scan())
    
    def import_from_m3_drive(self, file_path: str, file_type: str = "upload") -> Dict:
        """Import file from M3 hard drive"""
        async def _import():
            async with self.client as client:
                return await client.import_from_m3_drive(file_path, file_type)
        return self._run_async(_import())
    
    def list_uploaded_files(self, file_type: Optional[str] = None) -> Dict:
        """List uploaded files"""
        async def _list():
            async with self.client as client:
                return await client.list_uploaded_files(file_type)
        return self._run_async(_list())
    
    def get_file_info(self, file_id: str) -> Dict:
        """Get file information"""
        async def _info():
            async with self.client as client:
                return await client.get_file_info(file_id)
        return self._run_async(_info())
    
    def delete_file(self, file_id: str) -> Dict:
        """Delete uploaded file"""
        async def _delete():
            async with self.client as client:
                return await client.delete_file(file_id)
        return self._run_async(_delete())

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

if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())
