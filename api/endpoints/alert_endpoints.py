#!/usr/bin/env python3
"""
TradePulse Alert Endpoints
FastAPI endpoints for alert operations
"""

from fastapi import APIRouter, HTTPException
from api.models import AlertRequest, AlertResponse
from typing import Dict, List, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()

# Global data store reference (in production, use proper database)
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

@router.post("/create")
async def create_alert(request: AlertRequest):
    """Create a new alert"""
    try:
        logger.info(f"🚨 Creating alert for {request.symbol}")
        
        alert = {
            "symbol": request.symbol,
            "alert_type": request.alert_type,
            "threshold": request.threshold,
            "condition": request.condition,
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "triggered": False
        }
        
        # Store alert
        alert_id = f"alert_{request.symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        data_store["alerts"][alert_id] = alert
        
        return {
            "alert_id": alert_id,
            "alert": alert
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to create alert: {e}")
        raise HTTPException(status_code=500, detail=f"Alert creation failed: {str(e)}")

@router.get("/")
async def get_alerts(status: Optional[str] = None):
    """Get all alerts"""
    alerts = data_store["alerts"]
    
    if status:
        alerts = {k: v for k, v in alerts.items() if v["status"] == status}
    
    return {"alerts": alerts, "count": len(alerts)}

@router.get("/{alert_id}")
async def get_alert(alert_id: str):
    """Get specific alert"""
    if alert_id not in data_store["alerts"]:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    return data_store["alerts"][alert_id]

@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    """Delete an alert"""
    if alert_id not in data_store["alerts"]:
        raise HTTPException(status_code=404, detail=f"Alert {alert_id} not found")
    
    del data_store["alerts"][alert_id]
    return {"message": f"Alert {alert_id} deleted successfully"}
