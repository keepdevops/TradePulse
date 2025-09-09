#!/usr/bin/env python3
"""
TradePulse FastAPI + Panel - Core
Core FastAPI Panel integration functionality
"""

import panel as pn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from pathlib import Path
import sys
import asyncio
from contextlib import asynccontextmanager

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global Panel app instance
panel_app = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    global panel_app
    
    # Startup
    logger.info("🚀 Starting TradePulse Unified Server...")
    
    try:
        # Import Panel components
        from modular_panel_ui_main_refactored import create_refactored_modular_ui
        
        # Create Panel app
        logger.info("🔧 Creating Panel application...")
        panel_app = create_refactored_modular_ui()
        
        # Configure Panel
        panel_app.config.console_output = "disable"
        panel_app.config.raw_css = """
        .bk-root {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .bk-panel-models-widgets-box {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 10px;
            margin: 5px;
        }
        .bk-panel-models-widgets-button {
            background-color: #007bff;
            border-color: #007bff;
            color: white;
            border-radius: 4px;
            padding: 8px 16px;
        }
        .bk-panel-models-widgets-button:hover {
            background-color: #0056b3;
            border-color: #0056b3;
        }
        .bk-panel-models-widgets-select {
            border-radius: 4px;
            border: 1px solid #ced4da;
            padding: 6px 12px;
        }
        """
        
        logger.info("✅ Panel application created successfully")
        
    except Exception as e:
        logger.error(f"❌ Failed to create Panel application: {e}")
        panel_app = None
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down TradePulse Unified Server...")

# Create the main FastAPI app
app = FastAPI(
    title="TradePulse Unified API + Panel",
    description="High-performance unified server for TradePulse modular trading system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
try:
    from api.endpoints import data_endpoints, model_endpoints, portfolio_endpoints, alert_endpoints, system_endpoints, file_upload_endpoints
    
    app.include_router(data_endpoints.router, prefix="/api/v1/data", tags=["data"])
    app.include_router(model_endpoints.router, prefix="/api/v1/models", tags=["models"])
    app.include_router(portfolio_endpoints.router, prefix="/api/v1/portfolio", tags=["portfolio"])
    app.include_router(alert_endpoints.router, prefix="/api/v1/alerts", tags=["alerts"])
    app.include_router(system_endpoints.router, prefix="/api/v1/system", tags=["system"])
    app.include_router(file_upload_endpoints.router, prefix="/api/v1/files", tags=["files"])
    
    logger.info("✅ API routers included successfully")
except Exception as e:
    logger.error(f"❌ Failed to include API routers: {e}")

@app.get("/")
async def root():
    """Root endpoint serving Panel UI"""
    global panel_app
    
    if panel_app is None:
        return {"error": "Panel application not available"}
    
    try:
        panel_html = panel_app.get_root()
        return HTMLResponse(content=panel_html, status_code=200)
    except Exception as e:
        logger.error(f"❌ Root endpoint error: {e}")
        return {"error": f"Panel error: {str(e)}"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global panel_app
    
    return {
        "status": "healthy",
        "service": "TradePulse Unified API + Panel",
        "version": "1.0.0",
        "panel_status": "ready" if panel_app is not None else "error",
        "endpoints": {
            "panel_ui": "/",
            "api_docs": "/api/docs",
            "api_health": "/api/health",
            "data_api": "/api/v1/data",
            "models_api": "/api/v1/models",
            "portfolio_api": "/api/v1/portfolio",
            "alerts_api": "/api/v1/alerts",
            "system_api": "/api/v1/system",
            "files_api": "/api/v1/files"
        }
    }

# Global app instance
fastapi_panel_core_app = app
