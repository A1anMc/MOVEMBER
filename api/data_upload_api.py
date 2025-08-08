#!/usr/bin/env python3
"""
Data Upload API for Movember
Provides endpoints for uploading real Movember data in various formats.
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import shutil
from pathlib import Path
import json

from data_upload_system import upload_system

logger = logging.getLogger(__name__)

# Create router for data upload endpoints
data_upload_router = APIRouter(prefix="/data-upload", tags=["Data Upload"])

# Pydantic models
class UploadResponse(BaseModel):
    status: str
    data_id: str
    data_type: str
    source_file: str
    upload_date: str
    data_format: str
    validation_status: str
    currency: str = "AUD"
    spelling_standard: str = "UK"

class DataSummaryResponse(BaseModel):
    total_uploads: int
    by_type: Dict[str, int]
    by_status: Dict[str, int]
    by_format: Dict[str, int]
    recent_uploads: List[Dict[str, Any]]

class UploadInstructionsResponse(BaseModel):
    supported_formats: List[str]
    supported_data_types: List[str]
    upload_directory: str
    instructions: List[str]

# File upload endpoint
@data_upload_router.post("/upload-file/", response_model=UploadResponse)
async def upload_data_file(
    file: UploadFile = File(...),
    data_type: str = Form(..., description="Type of data: annual_reports, grants, projects, impact_metrics")
):
    """
    Upload a data file for processing.
    
    Supported formats:
    - CSV: Comma-separated values
    - JSON: JavaScript Object Notation
    - Excel: .xlsx or .xls files
    - PDF: Portable Document Format (basic text extraction)
    
    Supported data types:
    - annual_reports: Funding, reach, and impact data
    - grants: Grant opportunities and applications
    - projects: Project budgets and timelines
    - impact_metrics: Impact measurement data
    """
    
    logger.info(f"File upload request: {file.filename}, type: {data_type}")
    
    # Validate data type
    valid_types = ["annual_reports", "grants", "projects", "impact_metrics"]
    if data_type not in valid_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid data type. Must be one of: {valid_types}"
        )
    
    # Validate file format
    file_extension = Path(file.filename).suffix.lower()
    valid_extensions = [".csv", ".json", ".xlsx", ".xls", ".pdf"]
    if file_extension not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Supported formats: {valid_extensions}"
        )
    
    try:
        # Save uploaded file temporarily
        temp_file_path = f"temp_upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the uploaded file
        result = upload_system.upload_file(temp_file_path, data_type)
        
        # Clean up temp file
        os.remove(temp_file_path)
        
        return UploadResponse(**result)
        
    except Exception as e:
        logger.error(f"File upload failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"File upload failed: {str(e)}"
        )

# Get upload summary
@data_upload_router.get("/summary/", response_model=DataSummaryResponse)
async def get_upload_summary():
    """
    Get summary of all uploaded data.
    
    Returns:
    - Total number of uploads
    - Breakdown by data type
    - Breakdown by validation status
    - Breakdown by file format
    - Recent uploads
    """
    
    logger.info("Upload summary request")
    
    try:
        summary = upload_system.get_data_summary()
        return DataSummaryResponse(**summary)
        
    except Exception as e:
        logger.error(f"Summary retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Summary retrieval failed: {str(e)}"
        )

# Get uploaded data by type
@data_upload_router.get("/data/{data_type}/")
async def get_uploaded_data_by_type(data_type: str):
    """
    Get all uploaded data of a specific type.
    
    Parameters:
    - data_type: Type of data to retrieve (annual_reports, grants, projects, impact_metrics)
    """
    
    logger.info(f"Data retrieval request for type: {data_type}")
    
    try:
        data = upload_system.get_uploaded_data(data_type)
        return {
            "status": "success",
            "data_type": data_type,
            "count": len(data),
            "data": data,
            "currency": "AUD",
            "spelling_standard": "UK"
        }
        
    except Exception as e:
        logger.error(f"Data retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Data retrieval failed: {str(e)}"
        )

# Get upload instructions
@data_upload_router.get("/instructions/", response_model=UploadInstructionsResponse)
async def get_upload_instructions():
    """
    Get detailed instructions for uploading data.
    
    Returns:
    - Supported file formats
    - Supported data types
    - Upload directory structure
    - Step-by-step instructions
    """
    
    logger.info("Upload instructions request")
    
    instructions = UploadInstructionsResponse(
        supported_formats=["CSV", "JSON", "Excel (.xlsx/.xls)", "PDF"],
        supported_data_types=["annual_reports", "grants", "projects", "impact_metrics"],
        upload_directory="uploads/",
        instructions=[
            "1. Prepare your data file in one of the supported formats",
            "2. Ensure your data matches the expected structure for the data type",
            "3. Use the /upload-file/ endpoint to upload your data",
            "4. Check the validation status of your uploaded data",
            "5. Access your processed data through the API endpoints"
        ]
    )
    
    return instructions

# Get data structure templates
@data_upload_router.get("/templates/{data_type}/")
async def get_data_template(data_type: str):
    """
    Get template structure for a specific data type.
    
    Parameters:
    - data_type: Type of data template to retrieve
    """
    
    logger.info(f"Template request for type: {data_type}")
    
    templates = {
        "annual_reports": {
            "description": "Annual reports data structure",
            "csv_columns": [
                "year", "funding_raised", "men_reached", "countries_reached", 
                "research_funding", "lives_saved", "awareness_increase"
            ],
            "json_structure": {
                "funding": {
                    "total_raised": "AUD amount",
                    "research_funding": "AUD amount",
                    "year": "YYYY"
                },
                "reach": {
                    "men_reached": "number",
                    "countries_reached": "number",
                    "year": "YYYY"
                },
                "impact": {
                    "lives_saved": "number",
                    "awareness_increase": "percentage",
                    "year": "YYYY"
                }
            }
        },
        "grants": {
            "description": "Grant opportunities data structure",
            "csv_columns": [
                "id", "title", "amount", "currency", "deadline", "status", 
                "funding_body", "focus_areas", "geographic_scope"
            ],
            "json_structure": {
                "grants": [
                    {
                        "id": "unique identifier",
                        "title": "grant title",
                        "amount": "funding amount",
                        "currency": "AUD",
                        "deadline": "YYYY-MM-DD",
                        "status": "open/closed/approved/rejected",
                        "funding_body": "granting organisation",
                        "focus_areas": ["area1", "area2"],
                        "geographic_scope": ["country1", "country2"]
                    }
                ]
            }
        },
        "projects": {
            "description": "Project data structure",
            "csv_columns": [
                "project_id", "title", "budget", "currency", "start_date", 
                "end_date", "status", "geographic_scope", "target_audience"
            ],
            "json_structure": {
                "projects": [
                    {
                        "project_id": "unique identifier",
                        "title": "project title",
                        "budget": "total budget",
                        "currency": "AUD",
                        "start_date": "YYYY-MM-DD",
                        "end_date": "YYYY-MM-DD",
                        "status": "active/completed/planned",
                        "geographic_scope": ["country1", "country2"],
                        "target_audience": ["audience1", "audience2"]
                    }
                ]
            }
        },
        "impact_metrics": {
            "description": "Impact metrics data structure",
            "csv_columns": [
                "metric_name", "value", "unit", "region", "year", 
                "target", "actual", "percentage_achieved"
            ],
            "json_structure": {
                "metrics": {
                    "men_reached": {
                        "value": "number",
                        "region": "country/region",
                        "year": "YYYY"
                    },
                    "awareness_increase": {
                        "value": "percentage",
                        "region": "country/region",
                        "year": "YYYY"
                    },
                    "lives_saved": {
                        "value": "number",
                        "cause": "cancer/mental_health/etc",
                        "year": "YYYY"
                    }
                }
            }
        }
    }
    
    if data_type not in templates:
        raise HTTPException(
            status_code=404,
            detail=f"Template not found for data type: {data_type}"
        )
    
    return {
        "status": "success",
        "data_type": data_type,
        "template": templates[data_type],
        "currency": "AUD",
        "spelling_standard": "UK"
    }

# Download processed data
@data_upload_router.get("/download/{data_id}/")
async def download_processed_data(data_id: str):
    """
    Download processed data by data ID.
    
    Parameters:
    - data_id: Unique identifier for the uploaded data
    """
    
    logger.info(f"Download request for data ID: {data_id}")
    
    try:
        # Get the uploaded data
        all_data = upload_system.get_uploaded_data()
        target_data = None
        
        for data in all_data:
            if data["data_id"] == data_id:
                target_data = data
                break
        
        if not target_data:
            raise HTTPException(
                status_code=404,
                detail=f"Data not found with ID: {data_id}"
            )
        
        # Create a JSON file for download
        download_file = f"processed_data_{data_id}.json"
        with open(download_file, "w") as f:
            json.dump(target_data, f, indent=2)
        
        return FileResponse(
            path=download_file,
            filename=f"movember_data_{data_id}.json",
            media_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Download failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Download failed: {str(e)}"
        )

# Validate uploaded data
@data_upload_router.post("/validate/{data_id}/")
async def validate_uploaded_data(data_id: str):
    """
    Re-validate uploaded data by data ID.
    
    Parameters:
    - data_id: Unique identifier for the uploaded data
    """
    
    logger.info(f"Validation request for data ID: {data_id}")
    
    try:
        # Get the uploaded data
        all_data = upload_system.get_uploaded_data()
        target_data = None
        
        for data in all_data:
            if data["data_id"] == data_id:
                target_data = data
                break
        
        if not target_data:
            raise HTTPException(
                status_code=404,
                detail=f"Data not found with ID: {data_id}"
            )
        
        # Re-validate the data
        validation_status = upload_system._validate_extracted_data(
            target_data["extracted_data"], 
            target_data["data_type"]
        )
        
        # Update the validation status in database
        upload_system._save_uploaded_data(
            data_id,
            target_data["data_type"],
            target_data["source_file"],
            target_data["extracted_data"],
            validation_status
        )
        
        return {
            "status": "success",
            "data_id": data_id,
            "validation_status": validation_status,
            "message": f"Data re-validated. Status: {validation_status}",
            "currency": "AUD",
            "spelling_standard": "UK"
        }
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Validation failed: {str(e)}"
        )

# Health check for upload system
@data_upload_router.get("/health/")
async def upload_system_health():
    """
    Health check for the data upload system.
    """
    
    return {
        "status": "healthy",
        "service": "data_upload_system",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "file_upload",
            "data_extraction",
            "validation",
            "templates",
            "download"
        ],
        "currency": "AUD",
        "spelling_standard": "UK"
    }

# Export the router for inclusion in main API
__all__ = ["data_upload_router"] 