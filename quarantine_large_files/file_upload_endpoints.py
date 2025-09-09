#!/usr/bin/env python3
"""
TradePulse File Upload Endpoints
FastAPI endpoints for file upload and M3 hard drive access
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Dict, List, Optional
import logging
import os
import shutil
from pathlib import Path
from datetime import datetime
import glob

logger = logging.getLogger(__name__)
router = APIRouter()

# Global data store reference
data_store = {
    "market_data": {},
    "models": {},
    "portfolios": {},
    "alerts": {},
    "uploaded_files": {},
    "system_status": {
        "status": "operational",
        "last_update": datetime.now().isoformat(),
        "uptime": 0
    }
}

# Configure upload directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DATA_DIR = Path("upload_data")
M3_ACCESS_DIR = Path("/Volumes")  # M3 hard drive mount point

# Create directories if they don't exist
UPLOAD_DIR.mkdir(exist_ok=True)
UPLOAD_DATA_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), file_type: str = Form("data")):
    """Upload a file to TradePulse"""
    try:
        logger.info(f"📁 Uploading file: {file.filename} (type: {file_type})")
        
        # Validate file type
        allowed_types = ["csv", "json", "feather", "parquet", "duckdb", "h5", "xlsx"]
        file_extension = file.filename.split(".")[-1].lower()
        
        if file_extension not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_extension} not supported. Allowed: {allowed_types}"
            )
        
        # Save file to appropriate directory
        if file_type == "upload":
            save_dir = UPLOAD_DATA_DIR
        else:
            save_dir = UPLOAD_DIR / file_type
        
        save_dir.mkdir(exist_ok=True)
        file_path = save_dir / file.filename
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Store file metadata
        file_id = f"file_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        data_store["uploaded_files"][file_id] = {
            "filename": file.filename,
            "file_type": file_type,
            "file_extension": file_extension,
            "file_path": str(file_path),
            "uploaded_at": datetime.now().isoformat(),
            "file_size": file_path.stat().st_size
        }
        
        logger.info(f"✅ File uploaded successfully: {file_path}")
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_type": file_type,
            "file_path": str(file_path),
            "uploaded_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ File upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@router.get("/m3-drive/scan")
async def scan_m3_drive(path: str = "/Volumes"):
    """Scan M3 hard drive for data files"""
    try:
        logger.info(f"🔍 Scanning M3 drive at: {path}")
        
        if not os.path.exists(path):
            raise HTTPException(status_code=404, detail=f"Path not found: {path}")
        
        # Define file patterns to look for
        file_patterns = {
            "csv": "**/*.csv",
            "json": "**/*.json", 
            "feather": "**/*.feather",
            "parquet": "**/*.parquet",
            "duckdb": "**/*.duckdb",
            "keras": "**/*.h5",
            "excel": "**/*.xlsx"
        }
        
        found_files = {}
        
        for file_type, pattern in file_patterns.items():
            files = glob.glob(os.path.join(path, pattern), recursive=True)
            if files:
                found_files[file_type] = [
                    {
                        "path": f,
                        "filename": os.path.basename(f),
                        "size": os.path.getsize(f),
                        "modified": datetime.fromtimestamp(os.path.getmtime(f)).isoformat()
                    }
                    for f in files[:50]  # Limit to 50 files per type
                ]
        
        logger.info(f"✅ Found {sum(len(files) for files in found_files.values())} files")
        
        return {
            "scan_path": path,
            "found_files": found_files,
            "total_files": sum(len(files) for files in found_files.values()),
            "scanned_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ M3 drive scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")

@router.post("/m3-drive/import")
async def import_from_m3_drive(file_path: str, file_type: str = "upload"):
    """Import file from M3 hard drive to TradePulse"""
    try:
        logger.info(f"📥 Importing file from M3: {file_path}")
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File not found: {file_path}")
        
        # Validate file exists and is readable
        if not os.path.isfile(file_path):
            raise HTTPException(status_code=400, detail=f"Path is not a file: {file_path}")
        
        # Copy file to TradePulse directory
        filename = os.path.basename(file_path)
        
        if file_type == "upload":
            dest_dir = UPLOAD_DATA_DIR
        else:
            dest_dir = UPLOAD_DIR / file_type
        
        dest_dir.mkdir(exist_ok=True)
        dest_path = dest_dir / filename
        
        # Copy file
        shutil.copy2(file_path, dest_path)
        
        # Store metadata
        file_id = f"m3_import_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        data_store["uploaded_files"][file_id] = {
            "filename": filename,
            "file_type": file_type,
            "original_path": file_path,
            "file_path": str(dest_path),
            "imported_at": datetime.now().isoformat(),
            "file_size": dest_path.stat().st_size,
            "source": "m3_drive"
        }
        
        logger.info(f"✅ File imported successfully: {dest_path}")
        
        return {
            "file_id": file_id,
            "filename": filename,
            "file_type": file_type,
            "original_path": file_path,
            "imported_path": str(dest_path),
            "imported_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ M3 import failed: {e}")
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")

@router.get("/files")
async def list_uploaded_files(file_type: Optional[str] = None):
    """List all uploaded files"""
    files = data_store["uploaded_files"]
    
    if file_type:
        files = {k: v for k, v in files.items() if v["file_type"] == file_type}
    
    return {
        "files": files,
        "count": len(files),
        "file_types": list(set(f["file_type"] for f in files.values()))
    }

@router.get("/files/{file_id}")
async def get_file_info(file_id: str):
    """Get information about a specific file"""
    if file_id not in data_store["uploaded_files"]:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")
    
    return data_store["uploaded_files"][file_id]

@router.delete("/files/{file_id}")
async def delete_file(file_id: str):
    """Delete an uploaded file"""
    if file_id not in data_store["uploaded_files"]:
        raise HTTPException(status_code=404, detail=f"File {file_id} not found")
    
    file_info = data_store["uploaded_files"][file_id]
    file_path = Path(file_info["file_path"])
    
    try:
        if file_path.exists():
            file_path.unlink()
            logger.info(f"🗑️ Deleted file: {file_path}")
        
        del data_store["uploaded_files"][file_id]
        
        return {"message": f"File {file_id} deleted successfully"}
        
    except Exception as e:
        logger.error(f"❌ File deletion failed: {e}")
        raise HTTPException(status_code=500, detail=f"Deletion failed: {str(e)}")
