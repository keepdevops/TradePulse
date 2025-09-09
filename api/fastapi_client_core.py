#!/usr/bin/env python3
"""
TradePulse FastAPI Client - Core
Core FastAPI client functionality
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
        return await self._make_request("GET", "/api/v1/models/list")
    
    async def train_model(self, model_name: str, symbol: str, parameters: Optional[Dict] = None) -> Dict:
        """Train a model"""
        data = {
            "model_name": model_name,
            "symbol": symbol
        }
        if parameters:
            data["parameters"] = parameters
        
        return await self._make_request("POST", "/api/v1/models/train", data)
    
    async def make_prediction(self, symbol: str, model_name: str, features: Optional[Dict] = None) -> Dict:
        """Make a prediction using a model"""
        data = {
            "symbol": symbol,
            "model_name": model_name
        }
        if features:
            data["features"] = features
        
        return await self._make_request("POST", "/api/v1/models/predict", data)
    
    # Portfolio endpoints
    async def get_portfolio_status(self) -> Dict:
        """Get current portfolio status"""
        return await self._make_request("GET", "/api/v1/portfolio/status")
    
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
    
    # Alert endpoints
    async def get_alerts(self) -> Dict:
        """Get all alerts"""
        return await self._make_request("GET", "/api/v1/alerts/list")
    
    async def create_alert(self, symbol: str, alert_type: str, threshold: float, condition: str) -> Dict:
        """Create a new alert"""
        data = {
            "symbol": symbol,
            "alert_type": alert_type,
            "threshold": threshold,
            "condition": condition
        }
        return await self._make_request("POST", "/api/v1/alerts/create", data)
    
    async def delete_alert(self, alert_id: str) -> Dict:
        """Delete an alert"""
        return await self._make_request("DELETE", f"/api/v1/alerts/{alert_id}")

# Global instance
fastapi_client_core = TradePulseAPIClient()
