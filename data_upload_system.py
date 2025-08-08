#!/usr/bin/env python3
"""
Data Upload System for Real Movember Data
Allows uploading real data in various formats (CSV, JSON, Excel, PDF) and automatically extracts it.
"""

import os
import json
import logging
import pandas as pd
import sqlite3
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
import shutil
from dataclasses import dataclass, asdict
import re

logger = logging.getLogger(__name__)

@dataclass
class UploadedData:
    """Represents uploaded data with metadata."""
    data_id: str
    data_type: str  # 'annual_reports', 'grants', 'projects', 'impact_metrics'
    source_file: str
    upload_date: str
    data_format: str  # 'csv', 'json', 'excel', 'pdf'
    extracted_data: Dict[str, Any]
    validation_status: str  # 'valid', 'invalid', 'pending'
    currency: str = "AUD"
    spelling_standard: str = "UK"

class MovemberDataUploadSystem:
    """Handles uploading and extracting real Movember data."""
    
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.processed_dir = Path("processed_data")
        self.backup_dir = Path("backups")
        
        # Create directories
        self.upload_dir.mkdir(exist_ok=True)
        self.processed_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize database
        self._init_database()
        logger.info("Movember Data Upload System initialised")
    
    def _init_database(self):
        """Initialize the upload tracking database."""
        conn = sqlite3.connect("movember_uploads.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uploaded_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data_id TEXT UNIQUE NOT NULL,
                data_type TEXT NOT NULL,
                source_file TEXT NOT NULL,
                upload_date TEXT NOT NULL,
                data_format TEXT NOT NULL,
                extracted_data TEXT,
                validation_status TEXT DEFAULT 'pending',
                currency TEXT DEFAULT 'AUD',
                spelling_standard TEXT DEFAULT 'UK',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def upload_file(self, file_path: str, data_type: str) -> Dict[str, Any]:
        """Upload a file and extract data from it."""
        
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate unique data ID
        data_id = f"{data_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Copy file to upload directory
        upload_path = self.upload_dir / f"{data_id}_{file_path.name}"
        shutil.copy2(file_path, upload_path)
        
        # Extract data based on file format
        extracted_data = self._extract_data_from_file(upload_path, data_type)
        
        # Validate extracted data
        validation_status = self._validate_extracted_data(extracted_data, data_type)
        
        # Save to database
        self._save_uploaded_data(data_id, data_type, str(upload_path), extracted_data, validation_status)
        
        return {
            "status": "success",
            "data_id": data_id,
            "data_type": data_type,
            "source_file": str(upload_path),
            "upload_date": datetime.now().isoformat(),
            "data_format": self._get_file_format(file_path),
            "extracted_data": extracted_data,
            "validation_status": validation_status,
            "currency": "AUD",
            "spelling_standard": "UK"
        }
    
    def _extract_data_from_file(self, file_path: Path, data_type: str) -> Dict[str, Any]:
        """Extract data from uploaded file based on format and type."""
        
        file_format = self._get_file_format(file_path)
        
        if file_format == "csv":
            return self._extract_from_csv(file_path, data_type)
        elif file_format == "json":
            return self._extract_from_json(file_path, data_type)
        elif file_format == "excel":
            return self._extract_from_excel(file_path, data_type)
        elif file_format == "pdf":
            return self._extract_from_pdf(file_path, data_type)
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    
    def _extract_from_csv(self, file_path: Path, data_type: str) -> Dict[str, Any]:
        """Extract data from CSV file."""
        
        try:
            df = pd.read_csv(file_path)
            
            if data_type == "annual_reports":
                return self._extract_annual_reports_from_csv(df)
            elif data_type == "grants":
                return self._extract_grants_from_csv(df)
            elif data_type == "projects":
                return self._extract_projects_from_csv(df)
            elif data_type == "impact_metrics":
                return self._extract_impact_metrics_from_csv(df)
            else:
                return {"raw_data": df.to_dict('records')}
                
        except Exception as e:
            logger.error(f"Error extracting from CSV: {e}")
            return {"error": str(e)}
    
    def _extract_from_json(self, file_path: Path, data_type: str) -> Dict[str, Any]:
        """Extract data from JSON file."""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data_type == "annual_reports":
                return self._extract_annual_reports_from_json(data)
            elif data_type == "grants":
                return self._extract_grants_from_json(data)
            elif data_type == "projects":
                return self._extract_projects_from_json(data)
            elif data_type == "impact_metrics":
                return self._extract_impact_metrics_from_json(data)
            else:
                return {"raw_data": data}
                
        except Exception as e:
            logger.error(f"Error extracting from JSON: {e}")
            return {"error": str(e)}
    
    def _extract_from_excel(self, file_path: Path, data_type: str) -> Dict[str, Any]:
        """Extract data from Excel file."""
        
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_data = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_data[sheet_name] = df.to_dict('records')
            
            if data_type == "annual_reports":
                return self._extract_annual_reports_from_excel(sheets_data)
            elif data_type == "grants":
                return self._extract_grants_from_excel(sheets_data)
            elif data_type == "projects":
                return self._extract_projects_from_excel(sheets_data)
            elif data_type == "impact_metrics":
                return self._extract_impact_metrics_from_excel(sheets_data)
            else:
                return {"raw_data": sheets_data}
                
        except Exception as e:
            logger.error(f"Error extracting from Excel: {e}")
            return {"error": str(e)}
    
    def _extract_from_pdf(self, file_path: Path, data_type: str) -> Dict[str, Any]:
        """Extract data from PDF file (basic text extraction)."""
        
        try:
            # For now, return a placeholder - PDF extraction would need additional libraries
            return {
                "message": "PDF extraction requires additional setup",
                "file_path": str(file_path),
                "data_type": data_type,
                "extraction_method": "text_based"
            }
        except Exception as e:
            logger.error(f"Error extracting from PDF: {e}")
            return {"error": str(e)}
    
    def _extract_annual_reports_from_csv(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract annual reports data from CSV."""
        
        extracted = {
            "funding_data": {},
            "reach_data": {},
            "impact_data": {},
            "research_data": {}
        }
        
        # Look for funding columns
        funding_cols = [col for col in df.columns if any(word in col.lower() for word in ['fund', 'budget', 'amount', 'raised'])]
        for col in funding_cols:
            if df[col].dtype in ['int64', 'float64']:
                extracted["funding_data"][col] = df[col].sum()
        
        # Look for reach columns
        reach_cols = [col for col in df.columns if any(word in col.lower() for word in ['men', 'participant', 'reach', 'country'])]
        for col in reach_cols:
            if df[col].dtype in ['int64', 'float64']:
                extracted["reach_data"][col] = df[col].sum()
        
        return extracted
    
    def _extract_grants_from_csv(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract grants data from CSV."""
        
        extracted = {
            "grants": [],
            "total_funding": 0,
            "grant_count": len(df)
        }
        
        for _, row in df.iterrows():
            grant = {
                "id": str(row.get('id', row.get('grant_id', f"GRANT_{len(extracted['grants'])}"))),
                "title": str(row.get('title', row.get('name', ''))),
                "amount": float(row.get('amount', row.get('budget', 0))),
                "currency": str(row.get('currency', 'AUD')),
                "deadline": str(row.get('deadline', row.get('due_date', ''))),
                "status": str(row.get('status', 'open')),
                "source": str(row.get('source', row.get('funding_body', '')))
            }
            extracted["grants"].append(grant)
            extracted["total_funding"] += grant["amount"]
        
        return extracted
    
    def _extract_projects_from_csv(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract projects data from CSV."""
        
        extracted = {
            "projects": [],
            "total_budget": 0,
            "project_count": len(df)
        }
        
        for _, row in df.iterrows():
            project = {
                "project_id": str(row.get('project_id', row.get('id', f"PROJ_{len(extracted['projects'])}"))),
                "title": str(row.get('title', row.get('name', ''))),
                "budget": float(row.get('budget', row.get('amount', 0))),
                "currency": str(row.get('currency', 'AUD')),
                "start_date": str(row.get('start_date', '')),
                "end_date": str(row.get('end_date', '')),
                "status": str(row.get('status', 'active'))
            }
            extracted["projects"].append(project)
            extracted["total_budget"] += project["budget"]
        
        return extracted
    
    def _extract_impact_metrics_from_csv(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Extract impact metrics data from CSV."""
        
        extracted = {
            "metrics": {},
            "regions": {},
            "time_series": {}
        }
        
        # Extract metrics by column type
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                extracted["metrics"][col] = {
                    "total": df[col].sum(),
                    "average": df[col].mean(),
                    "count": len(df[col].dropna())
                }
        
        return extracted
    
    def _extract_annual_reports_from_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract annual reports data from JSON."""
        
        extracted = {
            "funding_data": data.get("funding", {}),
            "reach_data": data.get("reach", {}),
            "impact_data": data.get("impact", {}),
            "research_data": data.get("research", {})
        }
        
        return extracted
    
    def _extract_grants_from_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract grants data from JSON."""
        
        grants = data.get("grants", [])
        if isinstance(grants, list):
            return {
                "grants": grants,
                "total_funding": sum(g.get("amount", 0) for g in grants),
                "grant_count": len(grants)
            }
        else:
            return {"grants": [], "total_funding": 0, "grant_count": 0}
    
    def _extract_projects_from_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract projects data from JSON."""
        
        projects = data.get("projects", [])
        if isinstance(projects, list):
            return {
                "projects": projects,
                "total_budget": sum(p.get("budget", 0) for p in projects),
                "project_count": len(projects)
            }
        else:
            return {"projects": [], "total_budget": 0, "project_count": 0}
    
    def _extract_impact_metrics_from_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract impact metrics data from JSON."""
        
        return {
            "metrics": data.get("metrics", {}),
            "regions": data.get("regions", {}),
            "time_series": data.get("time_series", {})
        }
    
    def _extract_annual_reports_from_excel(self, sheets_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Extract annual reports data from Excel."""
        
        extracted = {
            "funding_data": {},
            "reach_data": {},
            "impact_data": {},
            "research_data": {}
        }
        
        for sheet_name, data in sheets_data.items():
            if "fund" in sheet_name.lower() or "budget" in sheet_name.lower():
                extracted["funding_data"][sheet_name] = data
            elif "reach" in sheet_name.lower() or "men" in sheet_name.lower():
                extracted["reach_data"][sheet_name] = data
            elif "impact" in sheet_name.lower():
                extracted["impact_data"][sheet_name] = data
            elif "research" in sheet_name.lower():
                extracted["research_data"][sheet_name] = data
        
        return extracted
    
    def _extract_grants_from_excel(self, sheets_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Extract grants data from Excel."""
        
        grants = []
        total_funding = 0
        
        for sheet_name, data in sheets_data.items():
            if "grant" in sheet_name.lower():
                for row in data:
                    if isinstance(row, dict):
                        grant = {
                            "id": str(row.get("id", f"GRANT_{len(grants)}")),
                            "title": str(row.get("title", "")),
                            "amount": float(row.get("amount", 0)),
                            "currency": str(row.get("currency", "AUD")),
                            "deadline": str(row.get("deadline", "")),
                            "status": str(row.get("status", "open"))
                        }
                        grants.append(grant)
                        total_funding += grant["amount"]
        
        return {
            "grants": grants,
            "total_funding": total_funding,
            "grant_count": len(grants)
        }
    
    def _extract_projects_from_excel(self, sheets_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Extract projects data from Excel."""
        
        projects = []
        total_budget = 0
        
        for sheet_name, data in sheets_data.items():
            if "project" in sheet_name.lower():
                for row in data:
                    if isinstance(row, dict):
                        project = {
                            "project_id": str(row.get("project_id", f"PROJ_{len(projects)}")),
                            "title": str(row.get("title", "")),
                            "budget": float(row.get("budget", 0)),
                            "currency": str(row.get("currency", "AUD")),
                            "start_date": str(row.get("start_date", "")),
                            "end_date": str(row.get("end_date", "")),
                            "status": str(row.get("status", "active"))
                        }
                        projects.append(project)
                        total_budget += project["budget"]
        
        return {
            "projects": projects,
            "total_budget": total_budget,
            "project_count": len(projects)
        }
    
    def _extract_impact_metrics_from_excel(self, sheets_data: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Extract impact metrics data from Excel."""
        
        extracted = {
            "metrics": {},
            "regions": {},
            "time_series": {}
        }
        
        for sheet_name, data in sheets_data.items():
            if "metric" in sheet_name.lower():
                extracted["metrics"][sheet_name] = data
            elif "region" in sheet_name.lower():
                extracted["regions"][sheet_name] = data
            elif "time" in sheet_name.lower() or "year" in sheet_name.lower():
                extracted["time_series"][sheet_name] = data
        
        return extracted
    
    def _get_file_format(self, file_path: Path) -> str:
        """Determine file format from extension."""
        
        extension = file_path.suffix.lower()
        
        if extension == ".csv":
            return "csv"
        elif extension == ".json":
            return "json"
        elif extension in [".xlsx", ".xls"]:
            return "excel"
        elif extension == ".pdf":
            return "pdf"
        else:
            return "unknown"
    
    def _validate_extracted_data(self, data: Dict[str, Any], data_type: str) -> str:
        """Validate extracted data based on type."""
        
        if "error" in data:
            return "invalid"
        
        if data_type == "annual_reports":
            return "valid" if any(key in data for key in ["funding_data", "reach_data"]) else "invalid"
        elif data_type == "grants":
            return "valid" if "grants" in data and len(data["grants"]) > 0 else "invalid"
        elif data_type == "projects":
            return "valid" if "projects" in data and len(data["projects"]) > 0 else "invalid"
        elif data_type == "impact_metrics":
            return "valid" if any(key in data for key in ["metrics", "regions", "time_series"]) else "invalid"
        else:
            return "valid"
    
    def _save_uploaded_data(self, data_id: str, data_type: str, source_file: str, extracted_data: Dict[str, Any], validation_status: str):
        """Save uploaded data to database."""
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy_types(obj):
            if hasattr(obj, 'item'):
                return obj.item()
            elif isinstance(obj, dict):
                return {k: convert_numpy_types(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy_types(item) for item in obj]
            else:
                return obj
        
        # Convert extracted data
        serializable_data = convert_numpy_types(extracted_data)
        
        conn = sqlite3.connect("movember_uploads.db")
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO uploaded_data
            (data_id, data_type, source_file, upload_date, data_format, extracted_data, validation_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data_id,
            data_type,
            source_file,
            datetime.now().isoformat(),
            self._get_file_format(Path(source_file)),
            json.dumps(serializable_data),
            validation_status
        ))
        
        conn.commit()
        conn.close()
    
    def get_uploaded_data(self, data_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all uploaded data, optionally filtered by type."""
        
        conn = sqlite3.connect("movember_uploads.db")
        cursor = conn.cursor()
        
        if data_type:
            cursor.execute("""
                SELECT * FROM uploaded_data WHERE data_type = ? ORDER BY created_at DESC
            """, (data_type,))
        else:
            cursor.execute("""
                SELECT * FROM uploaded_data ORDER BY created_at DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        columns = ["id", "data_id", "data_type", "source_file", "upload_date", "data_format", "extracted_data", "validation_status", "currency", "spelling_standard", "created_at"]
        
        result = []
        for row in rows:
            data_dict = dict(zip(columns, row))
            if data_dict["extracted_data"]:
                data_dict["extracted_data"] = json.loads(data_dict["extracted_data"])
            result.append(data_dict)
        
        return result
    
    def get_data_summary(self) -> Dict[str, Any]:
        """Get summary of all uploaded data."""
        
        all_data = self.get_uploaded_data()
        
        summary = {
            "total_uploads": len(all_data),
            "by_type": {},
            "by_status": {},
            "by_format": {},
            "recent_uploads": []
        }
        
        for data in all_data:
            # Count by type
            data_type = data["data_type"]
            summary["by_type"][data_type] = summary["by_type"].get(data_type, 0) + 1
            
            # Count by status
            status = data["validation_status"]
            summary["by_status"][status] = summary["by_status"].get(status, 0) + 1
            
            # Count by format
            format_type = data["data_format"]
            summary["by_format"][format_type] = summary["by_format"].get(format_type, 0) + 1
        
        # Get recent uploads (last 5)
        summary["recent_uploads"] = all_data[:5]
        
        return summary

# Global instance
upload_system = MovemberDataUploadSystem()

def main():
    """Test the upload system."""
    
    print("📤 Movember Data Upload System")
    print("=" * 50)
    
    # Show current uploads
    summary = upload_system.get_data_summary()
    print(f"📊 Total uploads: {summary['total_uploads']}")
    print(f"📁 By type: {summary['by_type']}")
    print(f"✅ By status: {summary['by_status']}")
    print(f"📄 By format: {summary['by_format']}")
    
    print("\n📋 Upload Instructions:")
    print("1. Place your data files in the 'uploads' directory")
    print("2. Supported formats: CSV, JSON, Excel, PDF")
    print("3. Supported data types: annual_reports, grants, projects, impact_metrics")
    print("4. Use the upload_file() method to process your data")
    
    print("\n📁 Upload Directory Structure:")
    print("uploads/")
    print("├── annual_reports/")
    print("├── grants/")
    print("├── projects/")
    print("└── impact_metrics/")

if __name__ == "__main__":
    main() 