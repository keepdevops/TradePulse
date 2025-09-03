#!/usr/bin/env python3
"""
TradePulse FastAPI + Panel Advanced Integration
Advanced unified server with proper Panel embedding in FastAPI
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

# Import and include FastAPI routers
try:
    from api.endpoints import data_endpoints, model_endpoints, portfolio_endpoints, alert_endpoints, system_endpoints, file_upload_endpoints
    
    app.include_router(data_endpoints.router, prefix="/api/v1/data", tags=["data"])
    app.include_router(model_endpoints.router, prefix="/api/v1/models", tags=["models"])
    app.include_router(portfolio_endpoints.router, prefix="/api/v1/portfolio", tags=["portfolio"])
    app.include_router(alert_endpoints.router, prefix="/api/v1/alerts", tags=["alerts"])
    app.include_router(system_endpoints.router, prefix="/api/v1/system", tags=["system"])
    app.include_router(file_upload_endpoints.router, prefix="/api/v1/files", tags=["files"])
    
    logger.info("✅ FastAPI routers included successfully")
except Exception as e:
    logger.error(f"❌ Failed to include FastAPI routers: {e}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the Panel UI at the root endpoint"""
    global panel_app
    
    if panel_app is None:
        return """
        <html>
            <head>
                <title>TradePulse - Error</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .error { color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; }
                    .link { color: #1976d2; text-decoration: none; }
                    .link:hover { text-decoration: underline; }
                </style>
            </head>
            <body>
                <h1>TradePulse Panel Error</h1>
                <div class="error">
                    <p>Panel application failed to load. Please check the logs.</p>
                </div>
                <p><a href="/api/docs" class="link">API Documentation</a></p>
                <p><a href="/health" class="link">Health Check</a></p>
            </body>
        </html>
        """
    
    try:
        # Get the Panel HTML
        panel_html = panel_app.get_root()
        return HTMLResponse(content=panel_html, status_code=200)
    except Exception as e:
        logger.error(f"❌ Failed to serve Panel UI: {e}")
        return f"""
        <html>
            <head>
                <title>TradePulse - Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 40px; }}
                    .error {{ color: #d32f2f; background: #ffebee; padding: 20px; border-radius: 8px; }}
                    .link {{ color: #1976d2; text-decoration: none; }}
                    .link:hover {{ text-decoration: underline; }}
                </style>
            </head>
            <body>
                <h1>TradePulse Panel Error</h1>
                <div class="error">
                    <p>Failed to render Panel UI: {str(e)}</p>
                </div>
                <p><a href="/api/docs" class="link">API Documentation</a></p>
                <p><a href="/health" class="link">Health Check</a></p>
            </body>
        </html>
        """

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

@app.get("/api/health")
async def api_health_check():
    """API-specific health check"""
    return {
        "status": "healthy",
        "service": "TradePulse API",
        "version": "1.0.0",
        "endpoints": [
            "/api/v1/data",
            "/api/v1/models", 
            "/api/v1/portfolio",
            "/api/v1/alerts",
            "/api/v1/system",
            "/api/v1/files"
        ]
    }

@app.get("/panel")
async def panel_endpoint():
    """Direct Panel endpoint"""
    global panel_app
    
    if panel_app is None:
        return {"error": "Panel application not available"}
    
    try:
        panel_html = panel_app.get_root()
        return HTMLResponse(content=panel_html, status_code=200)
    except Exception as e:
        logger.error(f"❌ Panel endpoint error: {e}")
        return {"error": f"Panel error: {str(e)}"}

@app.get("/status")
async def status():
    """Detailed status endpoint"""
    global panel_app
    
    return {
        "service": "TradePulse Unified Server",
        "version": "1.0.0",
        "components": {
            "fastapi": "ready",
            "panel": "ready" if panel_app is not None else "error",
            "api_endpoints": "ready",
            "file_upload": "ready"
        },
        "urls": {
            "main_ui": "http://localhost:8000",
            "api_docs": "http://localhost:8000/api/docs",
            "health_check": "http://localhost:8000/health",
            "panel_direct": "http://localhost:8000/panel"
        }
    }

# Mount static files if needed
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
    logger.info("✅ Static files mounted")
except:
    logger.warning("⚠️ Static files directory not found")

if __name__ == "__main__":
    logger.info("🚀 Starting TradePulse Unified API + Panel Server...")
    logger.info("📡 API will be available at: http://localhost:8000/api")
    logger.info("📊 Panel UI will be available at: http://localhost:8000")
    logger.info("📚 API Documentation: http://localhost:8000/api/docs")
    logger.info("🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "fastapi_panel_advanced_integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
