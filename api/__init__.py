#!/usr/bin/env python3
"""
TradePulse API Package
FastAPI server and client for TradePulse modular system
"""

from .fastapi_server import app
from .fastapi_client import TradePulseAPIClient, TradePulseAPIClientSync

__all__ = [
    'app',
    'TradePulseAPIClient',
    'TradePulseAPIClientSync'
]
