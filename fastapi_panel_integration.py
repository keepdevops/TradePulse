#!/usr/bin/env python3
"""
TradePulse FastAPI + Panel Integration
Unified server that serves both FastAPI endpoints and Panel UI
"""

import panel as pn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from pathlib import Path
import sys

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import FastAPI components
from api.fastapi_server import app as fastapi_app
from api.endpoints import data_endpoints, model_endpoints, portfolio_endpoints, alert_endpoints, system_endpoints, file_upload_endpoints

# Import Panel components
from modular_panel_ui_main_refactored import create_refactored_modular_ui

# Create the main FastAPI app
app = FastAPI(
    title="TradePulse Unified API + Panel",
    description="High-performance unified server for TradePulse modular trading system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all FastAPI routers
app.include_router(data_endpoints.router, prefix="/api/v1/data", tags=["data"])
app.include_router(model_endpoints.router, prefix="/api/v1/models", tags=["models"])
app.include_router(portfolio_endpoints.router, prefix="/api/v1/portfolio", tags=["portfolio"])
app.include_router(alert_endpoints.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(system_endpoints.router, prefix="/api/v1/system", tags=["system"])
app.include_router(file_upload_endpoints.router, prefix="/api/v1/files", tags=["files"])

# Create Panel app
def create_panel_app():
    """Create the Panel application"""
    try:
        logger.info("🔧 Creating Panel application...")
        
        # Create the Panel UI
        panel_app = create_refactored_modular_ui()
        
        # Configure Panel for embedding
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
        return panel_app
        
    except Exception as e:
        logger.error(f"❌ Failed to create Panel application: {e}")
        return None

# Create Panel app instance
panel_app = create_panel_app()

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the Panel UI at the root endpoint"""
    if panel_app is None:
        return """
        <html>
            <head><title>TradePulse - Error</title></head>
            <body>
                <h1>TradePulse Panel Error</h1>
                <p>Panel application failed to load. Please check the logs.</p>
                <p><a href="/api/docs">API Documentation</a></p>
            </body>
        </html>
        """
    
    try:
        # Get the Panel HTML
        panel_html = panel_app.get_root()
        return HTMLResponse(content=panel_html, status_code=200)
    except Exception as e:
        logger.error(f"❌ Failed to serve Panel UI: {e}")
        return """
        <html>
            <head><title>TradePulse - Error</title></head>
            <body>
                <h1>TradePulse Panel Error</h1>
                <p>Failed to render Panel UI: {error}</p>
                <p><a href="/api/docs">API Documentation</a></p>
            </body>
        </html>
        """.format(error=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "TradePulse Unified API + Panel",
        "version": "1.0.0",
        "panel_status": "ready" if panel_app is not None else "error"
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
    if panel_app is None:
        return {"error": "Panel application not available"}
    
    try:
        panel_html = panel_app.get_root()
        return HTMLResponse(content=panel_html, status_code=200)
    except Exception as e:
        logger.error(f"❌ Panel endpoint error: {e}")
        return {"error": f"Panel error: {str(e)}"}

# Mount static files if needed
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except:
    logger.warning("⚠️ Static files directory not found")

if __name__ == "__main__":
    logger.info("🚀 Starting TradePulse Unified API + Panel Server...")
    logger.info("📡 API will be available at: http://localhost:8000/api")
    logger.info("📊 Panel UI will be available at: http://localhost:8000")
    logger.info("📚 API Documentation: http://localhost:8000/api/docs")
    
    uvicorn.run(
        "fastapi_panel_integration:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
