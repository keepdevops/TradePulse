#!/usr/bin/env python3
"""
TradePulse FastAPI + Panel - Endpoints
Additional endpoints and server startup functionality
"""

import panel as pn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

logger = logging.getLogger(__name__)

# Global Panel app instance (shared with core)
panel_app = None

def setup_additional_endpoints(app: FastAPI):
    """Setup additional endpoints for the FastAPI app"""
    
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

def start_server():
    """Start the unified server"""
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

def set_panel_app(app_instance):
    """Set the global panel app instance"""
    global panel_app
    panel_app = app_instance
