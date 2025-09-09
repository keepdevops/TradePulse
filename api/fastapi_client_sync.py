#!/usr/bin/env python3
"""
TradePulse FastAPI Client - Sync Wrapper
Synchronous wrapper for FastAPI client
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any

from .fastapi_client_core import fastapi_client_core

logger = logging.getLogger(__name__)

class TradePulseAPIClientSync:
    """Synchronous wrapper for TradePulse FastAPI client"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.client = fastapi_client_core
        self.client.base_url = base_url
    
    def _run_async(self, coro):
        """Run async coroutine in sync context"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If we're already in an async context, create a new task
                return asyncio.create_task(coro)
            else:
                # If we're in sync context, run the coroutine
                return loop.run_until_complete(coro)
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(coro)
    
    # Health and status sync methods
    def health_check(self) -> Dict:
        """Check API server health"""
        async def _health():
            async with self.client as client:
                return await client.health_check()
        return self._run_async(_health())
    
    def get_system_status(self) -> Dict:
        """Get system status"""
        async def _status():
            async with self.client as client:
                return await client.get_system_status()
        return self._run_async(_status())
    
    def get_system_metrics(self) -> Dict:
        """Get system metrics"""
        async def _metrics():
            async with self.client as client:
                return await client.get_system_metrics()
        return self._run_async(_metrics())
    
    # Data sync methods
    def get_available_symbols(self) -> Dict:
        """Get list of available symbols"""
        async def _symbols():
            async with self.client as client:
                return await client.get_available_symbols()
        return self._run_async(_symbols())
    
    def fetch_market_data(self, symbol: str, timeframe: str = "1d", 
                         start_date: Optional[str] = None, end_date: Optional[str] = None,
                         data_source: str = "yahoo") -> Dict:
        """Fetch market data for a symbol"""
        async def _fetch():
            async with self.client as client:
                return await client.fetch_market_data(symbol, timeframe, start_date, end_date, data_source)
        return self._run_async(_fetch())
    
    def get_market_data(self, symbol: str, timeframe: str = "1d") -> Dict:
        """Get cached market data for a symbol"""
        async def _get():
            async with self.client as client:
                return await client.get_market_data(symbol, timeframe)
        return self._run_async(_get())
    
    # Model sync methods
    def get_available_models(self) -> Dict:
        """Get list of available models"""
        async def _models():
            async with self.client as client:
                return await client.get_available_models()
        return self._run_async(_models())
    
    def train_model(self, model_name: str, symbol: str, parameters: Optional[Dict] = None) -> Dict:
        """Train a model"""
        async def _train():
            async with self.client as client:
                return await client.train_model(model_name, symbol, parameters)
        return self._run_async(_train())
    
    def make_prediction(self, symbol: str, model_name: str, features: Optional[Dict] = None) -> Dict:
        """Make a prediction using a model"""
        async def _predict():
            async with self.client as client:
                return await client.make_prediction(symbol, model_name, features)
        return self._run_async(_predict())
    
    # Portfolio sync methods
    def get_portfolio_status(self) -> Dict:
        """Get current portfolio status"""
        async def _portfolio():
            async with self.client as client:
                return await client.get_portfolio_status()
        return self._run_async(_portfolio())
    
    def optimize_portfolio(self, symbols: List[str], weights: Optional[List[float]] = None,
                         risk_tolerance: str = "medium") -> Dict:
        """Optimize portfolio allocation"""
        async def _optimize():
            async with self.client as client:
                return await client.optimize_portfolio(symbols, weights, risk_tolerance)
        return self._run_async(_optimize())
    
    # Alert sync methods
    def get_alerts(self) -> Dict:
        """Get all alerts"""
        async def _alerts():
            async with self.client as client:
                return await client.get_alerts()
        return self._run_async(_alerts())
    
    def create_alert(self, symbol: str, alert_type: str, threshold: float, condition: str) -> Dict:
        """Create a new alert"""
        async def _create():
            async with self.client as client:
                return await client.create_alert(symbol, alert_type, threshold, condition)
        return self._run_async(_create())
    
    def delete_alert(self, alert_id: str) -> Dict:
        """Delete an alert"""
        async def _delete():
            async with self.client as client:
                return await client.delete_alert(alert_id)
        return self._run_async(_delete())
    
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

# Global sync instance
fastapi_client_sync = TradePulseAPIClientSync()
