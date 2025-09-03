#!/usr/bin/env python3
"""
TradePulse FastAPI Server
High-performance API server for TradePulse modular system
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import uvicorn
import logging
from datetime import datetime

# Import modular endpoints
from api.endpoints import data_endpoints, model_endpoints, portfolio_endpoints, alert_endpoints, system_endpoints, file_upload_endpoints
from api.models import DataRequest, ModelPredictionRequest, PortfolioRequest, AlertRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="TradePulse API",
    description="High-performance API for TradePulse modular trading system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data store (in production, use proper database)
data_store = {
    "market_data": {},
    "models": {},
    "portfolios": {},
    "alerts": {},
    "system_status": {
        "status": "operational",
        "last_update": datetime.now().isoformat(),
        "uptime": 0
    }
}

@app.on_event("startup")
async def startup_event():
    """Initialize FastAPI server"""
    logger.info("🚀 TradePulse FastAPI server starting...")
    data_store["system_status"]["startup_time"] = datetime.now().isoformat()

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on server shutdown"""
    logger.info("🛑 TradePulse FastAPI server shutting down...")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "TradePulse API Server",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "data": "/api/v1/data",
            "models": "/api/v1/models",
            "portfolio": "/api/v1/portfolio",
            "alerts": "/api/v1/alerts",
            "system": "/api/v1/system"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": data_store["system_status"].get("uptime", 0)
    }

# Include modular endpoints
app.include_router(data_endpoints.router, prefix="/api/v1/data", tags=["data"])
app.include_router(model_endpoints.router, prefix="/api/v1/models", tags=["models"])
app.include_router(portfolio_endpoints.router, prefix="/api/v1/portfolio", tags=["portfolio"])
app.include_router(alert_endpoints.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(system_endpoints.router, prefix="/api/v1/system", tags=["system"])
app.include_router(file_upload_endpoints.router, prefix="/api/v1/files", tags=["files"])

# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"❌ Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

if __name__ == "__main__":
    # Run the FastAPI server
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
