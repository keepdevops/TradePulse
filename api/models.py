#!/usr/bin/env python3
"""
TradePulse FastAPI Models
Pydantic models for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class DataRequest(BaseModel):
    """Request model for data fetching"""
    symbol: str = Field(..., description="Stock symbol (e.g., AAPL, GOOGL)")
    timeframe: str = Field(default="1d", description="Timeframe for data")
    start_date: Optional[str] = Field(None, description="Start date (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="End date (YYYY-MM-DD)")
    data_source: str = Field(default="yahoo", description="Data source (yahoo, alpha_vantage, iex, mock)")

class ModelPredictionRequest(BaseModel):
    """Request model for model predictions"""
    symbol: str = Field(..., description="Stock symbol")
    model_name: str = Field(..., description="Model name to use")
    features: Dict[str, Any] = Field(default={}, description="Input features for prediction")

class PortfolioRequest(BaseModel):
    """Request model for portfolio operations"""
    symbols: List[str] = Field(..., description="List of stock symbols")
    weights: Optional[List[float]] = Field(None, description="Portfolio weights")
    risk_tolerance: str = Field(default="medium", description="Risk tolerance level")

class AlertRequest(BaseModel):
    """Request model for alert creation"""
    symbol: str = Field(..., description="Stock symbol")
    alert_type: str = Field(..., description="Alert type (price, volume, technical)")
    threshold: float = Field(..., description="Alert threshold value")
    condition: str = Field(..., description="Condition (above, below, equals)")

class MarketDataResponse(BaseModel):
    """Response model for market data"""
    symbol: str
    timeframe: str
    data_source: str
    records: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    symbol: str
    model_name: str
    prediction: Dict[str, Any]
    features: Dict[str, Any]
    metadata: Dict[str, Any]

class PortfolioResponse(BaseModel):
    """Response model for portfolio operations"""
    portfolio_id: str
    portfolio: Dict[str, Any]

class AlertResponse(BaseModel):
    """Response model for alerts"""
    alert_id: str
    alert: Dict[str, Any]

class SystemStatusResponse(BaseModel):
    """Response model for system status"""
    status: str
    timestamp: str
    uptime: int

class SystemMetricsResponse(BaseModel):
    """Response model for system metrics"""
    data_requests: int
    active_models: int
    portfolios: int
    active_alerts: int
    memory_usage: str
    cpu_usage: str
    disk_usage: str
