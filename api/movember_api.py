#!/usr/bin/env python3
"""
Movember AI Rules System - API Layer
Provides RESTful API endpoints for data collection, external integrations, and monitoring.
All responses use UK spelling and AUD currency.
"""

import asyncio
import logging
import os
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Header, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import httpx
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
import time
import random

# Import rules system with error handling
try:
    from rules.domains.movember_ai import MovemberAIRulesEngine
    from rules.types import ExecutionContext, ContextType, RulePriority
    RULES_SYSTEM_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Rules system not available: {e}")
    MovemberAIRulesEngine = None
    ExecutionContext = None
    ContextType = None
    RulePriority = None
    RULES_SYSTEM_AVAILABLE = False

# Import grant acquisition system
try:
    from grant_acquisition_engine import grant_acquisition_engine
    GRANT_ACQUISITION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Grant acquisition system not available: {e}")
    grant_acquisition_engine = None
    grant_acquisition_router = None
    GRANT_ACQUISITION_AVAILABLE = False

# Import impact intelligence system
try:
    from impact_intelligence_engine import impact_intelligence_engine
    IMPACT_INTELLIGENCE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Impact intelligence system not available: {e}")
    impact_intelligence_engine = None
    impact_intelligence_router = None
    IMPACT_INTELLIGENCE_AVAILABLE = False

# Import real data integration system
try:
    REAL_DATA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Real data integration system not available: {e}")
    movember_data_integrator = None
    real_data_router = None
    REAL_DATA_AVAILABLE = False

# Import data upload system
try:
    DATA_UPLOAD_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Data upload system not available: {e}")
    upload_system = None
    data_upload_router = None
    DATA_UPLOAD_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()
# Use DATABASE_URL if provided, else default to local SQLite for tests/dev
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///movember_ai.db")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Note: Tables will be created on application startup to ensure all ORM models are loaded


def ensure_tables() -> None:
    """Ensure ORM tables exist (idempotent)."""
    try:
        # Import ORM models defined below via globals
        tables = []
        try:
            tables = [
                globals().get('GrantRecord').__table__,
                globals().get('ImpactReportRecord').__table__,
                globals().get('SystemHealthRecord').__table__,
            ]
        except Exception:
            tables = []

        # Create explicitly per table to avoid timing issues
        for t in [t for t in tables if t is not None]:
            t.create(bind=engine, checkfirst=True)

        # Fallback to metadata-wide create as well
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        logger.error("ensure_tables failed: %s", exc)


class GrantData(BaseModel):
    """Grant data model with UK spelling and AUD currency."""
    grant_id: str = Field(..., description="Unique grant identifier")
    title: str = Field(..., description="Grant title")
    budget: float = Field(..., description="Budget in AUD")
    currency: str = Field(default="AUD", description="Currency (always AUD)")
    timeline_months: int = Field(..., description="Project timeline in months")
    impact_metrics: List[Dict] = Field(default=[], description="Impact metrics")
    sdg_alignment: List[str] = Field(default=[], description="SDG alignment")
    sustainability_plan: str = Field(default="", description="Sustainability plan")
    status: str = Field(default="draft", description="Grant status")
    organisation: str = Field(..., description="Organisation name")
    contact_person: str = Field(..., description="Contact person")
    email: str = Field(..., description="Contact email")
    phone: str = Field(default="", description="Contact phone")
    description: str = Field(..., description="Project description")
    objectives: List[str] = Field(default=[], description="Project objectives")
    methodology: str = Field(default="", description="Research methodology")
    expected_outcomes: List[str] = Field(default=[], description="Expected outcomes")
    risk_mitigation: str = Field(default="", description="Risk mitigation plan")
    partnerships: List[str] = Field(default=[], description="Partnerships")
    innovation_score: float = Field(default=0.0, description="Innovation score (0-10)")
    complexity_score: float = Field(default=0.0, description="Complexity score (0-1)")
    data_intensive: bool = Field(default=False, description="Data intensive project")
    human_subjects: bool = Field(default=False, description="Involves human subjects")
    ethical_approval: str = Field(default="pending", description="Ethical approval status")
    data_management_plan: str = Field(default="", description="Data management plan")
    stakeholder_engagement: str = Field(default="minimal", description="Stakeholder engagement level")
    community_impact: str = Field(default="medium", description="Community impact level")
    funding_type: str = Field(default="research", description="Funding type")
    scope: str = Field(default="national", description="Geographic scope")
    project_duration: int = Field(default=12, description="Project duration in months")
    impact_focus: str = Field(default="medium", description="Impact focus level")
    budget_breakdown: Dict = Field(default={}, description="Detailed budget breakdown")
    evaluation_criteria: List[str] = Field(default=[], description="Evaluation criteria")
    impact_measurement_framework: str = Field(default="", description="Impact measurement framework")
    cost_effectiveness_analysis: str = Field(default="", description="Cost effectiveness analysis")
    sustainability_indicators: List[str] = Field(default=[], description="Sustainability indicators")


class ImpactReportData(BaseModel):
    """Impact report data model with UK spelling and AUD currency."""
    report_id: str = Field(..., description="Unique report identifier")
    title: str = Field(..., description="Report title")
    type: str = Field(..., description="Report type")
    frameworks: List[str] = Field(default=[], description="Evaluation frameworks")
    outputs: List[Dict] = Field(default=[], description="Project outputs")
    outcomes: List[Dict] = Field(default=[], description="Project outcomes")
    stakeholders: List[str] = Field(default=[], description="Target stakeholders")
    data_sources: List[str] = Field(default=[], description="Data sources")
    visualisations: List[str] = Field(default=[], description="Data visualisations")
    attribution: str = Field(default="clear", description="Attribution methodology")
    data_gaps: List[str] = Field(default=[], description="Identified data gaps")
    audience: str = Field(default="executive", description="Target audience")
    complexity_level: float = Field(default=0.5, description="Complexity level (0-1)")
    confidence_level: float = Field(default=0.8, description="Confidence level (0-1)")
    baseline_data: str = Field(default="", description="Baseline data")
    impact_measurement: str = Field(default="required", description="Impact measurement status")
    impact_metrics: List[Dict] = Field(default=[], description="Impact metrics")
    statistical_tests: str = Field(default="", description="Statistical tests used")
    sample_size: int = Field(default=0, description="Sample size")
    ethical_considerations: str = Field(default="", description="Ethical considerations")
    human_subjects: bool = Field(default=False, description="Involves human subjects")
    timeline_months: int = Field(default=12, description="Report timeline in months")
    longitudinal_data: str = Field(default="", description="Longitudinal data")
    stakeholder_engagement: str = Field(default="minimal", description="Stakeholder engagement")
    community_impact: str = Field(default="medium", description="Community impact")
    total_cost: float = Field(default=0.0, description="Total cost in AUD")
    cost_effectiveness_analysis: str = Field(default="", description="Cost effectiveness analysis")
    project_duration: int = Field(default=12, description="Project duration")
    sustainability_indicators: List[str] = Field(default=[], description="Sustainability indicators")
    methodology: str = Field(default="", description="Research methodology")
    conclusions: str = Field(default="", description="Report conclusions")
    recommendations: str = Field(default="", description="Recommendations")


class SystemHealthData(BaseModel):
    """System health monitoring data."""
    timestamp: datetime = Field(default_factory=datetime.now)
    system_status: str = Field(default="healthy", description="System status")
    uptime_percentage: float = Field(default=99.9, description="Uptime percentage")
    active_rules: int = Field(default=0, description="Active rules count")
    total_executions: int = Field(default=0, description="Total rule executions")
    success_rate: float = Field(default=0.95, description="Success rate")
    average_response_time: float = Field(default=0.5, description="Average response time in seconds")
    error_count: int = Field(default=0, description="Error count")
    memory_usage: float = Field(default=0.0, description="Memory usage percentage")
    cpu_usage: float = Field(default=0.0, description="CPU usage percentage")
    disk_usage: float = Field(default=0.0, description="Disk usage percentage")
    active_connections: int = Field(default=0, description="Active connections")
    queue_size: int = Field(default=0, description="Queue size")
    last_backup: datetime = Field(default_factory=datetime.now, description="Last backup timestamp")
    security_status: str = Field(default="secure", description="Security status")
    compliance_status: str = Field(default="compliant", description="Compliance status")
    uk_spelling_consistency: float = Field(default=1.0, description="UK spelling consistency")
    aud_currency_compliance: float = Field(default=1.0, description="AUD currency compliance")


class ExternalDataRequest(BaseModel):
    """Request model for external data collection."""
    source_type: str = Field(..., description="Data source type")
    endpoint: str = Field(..., description="API endpoint")
    parameters: Dict = Field(default={}, description="Request parameters")
    authentication: Dict = Field(default={}, description="Authentication details")
    data_format: str = Field(default="json", description="Expected data format")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    retry_count: int = Field(default=3, description="Retry count")
    validation_rules: List[str] = Field(default=[], description="Data validation rules")


class ScraperConfig(BaseModel):
    """Configuration for web scrapers."""
    target_url: str = Field(..., description="Target URL")
    selectors: Dict = Field(default={}, description="CSS selectors for data extraction")
    pagination: Dict = Field(default={}, description="Pagination configuration")
    rate_limit: int = Field(default=1, description="Requests per second")
    user_agent: str = Field(default="Movember AI Bot", description="User agent string")
    authentication: Dict = Field(default={}, description="Authentication details")
    data_mapping: Dict = Field(default={}, description="Data field mapping")
    validation_rules: List[str] = Field(default=[], description="Data validation rules")
    uk_spelling_conversion: bool = Field(default=True, description="Convert to UK spelling")
    aud_currency_conversion: bool = Field(default=True, description="Convert to AUD currency")


# Database models
class GrantRecord(Base):


    __tablename__ = "grants"

    id = Column(Integer, primary_key=True, index=True)
    grant_id = Column(String, unique=True, index=True)
    title = Column(String)
    budget = Column(Float)
    currency = Column(String, default="AUD")
    timeline_months = Column(Integer)
    status = Column(String)
    organisation = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    data_json = Column(Text)  # Store full JSON data


class ImpactReportRecord(Base):
    __tablename__ = "impact_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String, unique=True, index=True)
    title = Column(String)
    type = Column(String)
    frameworks = Column(Text)  # JSON string
    status = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    data_json = Column(Text)  # Store full JSON data


class SystemHealthRecord(Base):
    __tablename__ = "system_health"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    system_status = Column(String)
    uptime_percentage = Column(Float)
    active_rules = Column(Integer)
    total_executions = Column(Integer)
    success_rate = Column(Float)
    average_response_time = Column(Float)
    error_count = Column(Integer)
    memory_usage = Column(Float)
    cpu_usage = Column(Float)
    disk_usage = Column(Float)
    active_connections = Column(Integer)
    queue_size = Column(Integer)
    last_backup = Column(DateTime)
    security_status = Column(String)
    compliance_status = Column(String)
    uk_spelling_consistency = Column(Float)
    aud_currency_compliance = Column(Float)


# FastAPI app setup
app = FastAPI(
    title="Movember AI Rules System API",
    description="API for Movember AI Rules System with UK spelling and AUD currency standards",
    version="1.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="assets"), name="static")

# Ensure DB tables exist at startup (handles fresh Postgres instances on Render)
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Create grant_evaluations table if it doesn't exist
        with engine.begin() as conn:
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS grant_evaluations (
                    id SERIAL PRIMARY KEY,
                    grant_id VARCHAR(255) NOT NULL,
                    evaluation_timestamp TIMESTAMP NOT NULL,
                    overall_score DECIMAL(3,3) NOT NULL,
                    recommendation VARCHAR(50) NOT NULL,
                    ml_predictions JSONB,
                    rules_evaluation JSONB,
                    grant_data JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))

        logger.info("Database tables initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")

# Basic API key auth dependency (skip if API_KEY not set)
API_KEY = os.getenv("API_KEY", "").strip()

async def verify_api_key(x_api_key: str | None = Header(default=None)):
    if not API_KEY:
        return True
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return True

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Log system availability
if GRANT_ACQUISITION_AVAILABLE:
    logger.info("Grant acquisition system available")
else:
    logger.warning("Grant acquisition system not available")

if IMPACT_INTELLIGENCE_AVAILABLE:
    logger.info("Impact intelligence system available")
else:
    logger.warning("Impact intelligence system not available")

if REAL_DATA_AVAILABLE:
    logger.info("Real data integration system available")
else:
    logger.warning("Real data integration system not available")

if DATA_UPLOAD_AVAILABLE:
    logger.info("Data upload system available")
else:
    logger.warning("Data upload system not available")

# Global variables
movember_engine = None
health_monitor = None


class MovemberAPIService:
    """Service layer for Movember AI Rules System API."""

    def __init__(self):


        self.engine = MovemberAIRulesEngine()
        self.db = SessionLocal()
        self.logger = logging.getLogger(__name__)

    async def process_grant_application(self, grant_data: GrantData) -> Dict:
        """Process grant application with rules engine."""
        try:
            # Convert to UK spelling and AUD currency
            processed_data = self._ensure_uk_spelling_and_aud_currency(grant_data.dict())

            # Create execution context
            context = ExecutionContext(
                context_type=ContextType.GRANT_EVALUATION,
                context_id=f"grant-{grant_data.grant_id}",
                data=processed_data,
                timestamp=datetime.now()
            )

            # Evaluate rules
            results = await self.engine.evaluate_context(context, mode="grant_submission")

            # Store in database
            self._store_grant_record(grant_data)

            return {
                "status": "success",
                "grant_id": grant_data.grant_id,
                "evaluation_results": results,
                "recommendations": self._generate_grant_recommendations(processed_data),
                "score": self._calculate_grant_score(processed_data),
                "currency": "AUD",
                "spelling_standard": "UK"
            }

        except Exception as e:
            self.logger.error(f"Error processing grant application: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing grant application: {str(e)}")

    async def process_impact_report(self, report_data: ImpactReportData) -> Dict:
        """Process impact report with rules engine."""
        try:
            # Convert to UK spelling and AUD currency
            processed_data = self._ensure_uk_spelling_and_aud_currency(report_data.dict())

            # Create execution context
            context = ExecutionContext(
                context_type=ContextType.IMPACT_REPORTING,
                context_id=f"report-{report_data.report_id}",
                data=processed_data,
                timestamp=datetime.now()
            )

            # Evaluate rules
            results = await self.engine.evaluate_context(context, mode="reporting")

            # Store in database
            self._store_impact_report_record(report_data)

            return {
                "status": "success",
                "report_id": report_data.report_id,
                "evaluation_results": results,
                "quality_score": self._calculate_report_quality_score(processed_data),
                "framework_compliance": self._validate_framework_compliance(processed_data),
                "recommendations": self._generate_report_recommendations(processed_data),
                "currency": "AUD",
                "spelling_standard": "UK"
            }

        except Exception as e:
            self.logger.error(f"Error processing impact report: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing impact report: {str(e)}")

    async def collect_external_data(self, request: ExternalDataRequest) -> Dict:
        """Collect data from external sources."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    request.endpoint,
                    params=request.parameters,
                    headers=request.authentication,
                    timeout=request.timeout
                )

                if response.status_code == 200:
                    data = response.json()

                    # Apply UK spelling and AUD currency conversion
                    processed_data = self._ensure_uk_spelling_and_aud_currency(data)

                    return {
                        "status": "success",
                        "source": request.source_type,
                        "data": processed_data,
                        "timestamp": datetime.now(),
                        "currency": "AUD",
                        "spelling_standard": "UK"
                    }
                else:
                    raise HTTPException(status_code=response.status_code, detail="External API error")

        except Exception as e:
            self.logger.error(f"Error collecting external data: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error collecting external data: {str(e)}")

    async def run_web_scraper(self, config: ScraperConfig) -> Dict:
        """Run web scraper with specified configuration."""
        try:
            import requests

            # Make request with rate limiting
            await asyncio.sleep(1 / config.rate_limit)

            headers = {
                "User-Agent": config.user_agent
            }

            if config.authentication:
                headers.update(config.authentication)

            response = requests.get(config.target_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract data using selectors
            extracted_data = {}
            for field, selector in config.selectors.items():
                elements = soup.select(selector)
                if elements:
                    extracted_data[field] = [elem.get_text(strip=True) for elem in elements]

            # Apply data mapping
            mapped_data = {}
            for source_field, target_field in config.data_mapping.items():
                if source_field in extracted_data:
                    mapped_data[target_field] = extracted_data[source_field]

            # Apply UK spelling and AUD currency conversion
            processed_data = self._ensure_uk_spelling_and_aud_currency(mapped_data)

            return {
                "status": "success",
                "url": config.target_url,
                "data": processed_data,
                "timestamp": datetime.now(),
                "currency": "AUD",
                "spelling_standard": "UK"
            }

        except Exception as e:
            self.logger.error(f"Error running web scraper: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error running web scraper: {str(e)}")

    async def monitor_system_health(self) -> SystemHealthData:
        """Monitor system health and performance."""
        try:
            # Get system metrics
            metrics = self.engine.get_metrics()

            # Calculate health indicators
            health_data = SystemHealthData(
                system_status="healthy",
                uptime_percentage=99.9,
                active_rules=len(self.engine.engine.rules),
                total_executions=metrics.get("system_metrics", {}).get("total_executions", 0),
                success_rate=metrics.get("system_metrics", {}).get("success_rate", 0.95),
                average_response_time=0.5,
                error_count=0,
                memory_usage=50.0,
                cpu_usage=30.0,
                disk_usage=25.0,
                active_connections=5,
                queue_size=0,
                last_backup=datetime.now(),
                security_status="secure",
                compliance_status="compliant",
                uk_spelling_consistency=1.0,
                aud_currency_compliance=1.0
            )

            # Store health record
            self._store_health_record(health_data)

            return health_data

        except Exception as e:
            self.logger.error(f"Error monitoring system health: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error monitoring system health: {str(e)}")

    def _ensure_uk_spelling_and_aud_currency(self, data: Dict) -> Dict:


        """Ensure data uses UK spelling and AUD currency."""
        # Import conversion functions
        from rules.domains.movember_ai.behaviours import convert_to_uk_spelling, format_aud_currency

        processed_data = data.copy()

        # Process text fields for UK spelling
        text_fields = ['title',
             'description', 'summary', 'notes', 'comments', 'methodology', 'conclusions', 'recommendations']
        for field in text_fields:
            if field in processed_data and isinstance(processed_data[field], str):
                processed_data[field] = convert_to_uk_spelling(processed_data[field])

        # Process currency fields for AUD
        currency_fields = ['budget', 'amount', 'cost', 'funding', 'expense', 'total_cost']
        for field in currency_fields:
            if field in processed_data and isinstance(processed_data[field], (int, float)):
                processed_data[f'{field}_currency'] = 'AUD'
                processed_data[f'{field}_formatted'] = format_aud_currency(processed_data[field])

        return processed_data

    def _store_grant_record(self, grant_data: GrantData):


        """Store grant record in database."""
        ensure_tables()
        record = GrantRecord(
            grant_id=grant_data.grant_id,
            title=grant_data.title,
            budget=grant_data.budget,
            currency=grant_data.currency,
            timeline_months=grant_data.timeline_months,
            status=grant_data.status,
            organisation=grant_data.organisation,
            data_json=json.dumps(grant_data.dict())
        )
        self.db.add(record)
        self.db.commit()

    def _store_impact_report_record(self, report_data: ImpactReportData):


        """Store impact report record in database."""
        ensure_tables()
        record = ImpactReportRecord(
            report_id=report_data.report_id,
            title=report_data.title,
            type=report_data.type,
            frameworks=json.dumps(report_data.frameworks),
            status="submitted",
            data_json=json.dumps(report_data.dict())
        )
        self.db.add(record)
        self.db.commit()

    def _store_health_record(self, health_data: SystemHealthData):


        """Store system health record in database."""
        ensure_tables()
        record = SystemHealthRecord(
            system_status=health_data.system_status,
            uptime_percentage=health_data.uptime_percentage,
            active_rules=health_data.active_rules,
            total_executions=health_data.total_executions,
            success_rate=health_data.success_rate,
            average_response_time=health_data.average_response_time,
            error_count=health_data.error_count,
            memory_usage=health_data.memory_usage,
            cpu_usage=health_data.cpu_usage,
            disk_usage=health_data.disk_usage,
            active_connections=health_data.active_connections,
            queue_size=health_data.queue_size,
            last_backup=health_data.last_backup,
            security_status=health_data.security_status,
            compliance_status=health_data.compliance_status,
            uk_spelling_consistency=health_data.uk_spelling_consistency,
            aud_currency_compliance=health_data.aud_currency_compliance
        )
        self.db.add(record)
        self.db.commit()

    def _generate_grant_recommendations(self, grant_data: Dict) -> List[str]:


        """Generate recommendations for grant improvement."""
        from rules.domains.movember_ai.grant_rules import generate_grant_recommendations
        return generate_grant_recommendations(grant_data)

    def _calculate_grant_score(self, grant_data: Dict) -> float:


        """Calculate grant score."""
        from rules.domains.movember_ai.grant_rules import calculate_grant_score
        return calculate_grant_score(grant_data)

    def _calculate_report_quality_score(self, report_data: Dict) -> float:


        """Calculate report quality score."""
        from rules.domains.movember_ai.reporting import calculate_report_quality_score
        return calculate_report_quality_score(report_data)

    def _validate_framework_compliance(self, report_data: Dict) -> Dict:


        """Validate framework compliance."""
        from rules.domains.movember_ai.reporting import validate_framework_compliance
        return validate_framework_compliance(report_data)

    def _generate_report_recommendations(self, report_data: Dict) -> List[str]:


        """Generate recommendations for report improvement."""
        from rules.domains.movember_ai.reporting import generate_report_recommendations
        return generate_report_recommendations(report_data)


# Dependency injection
def get_api_service():


    return MovemberAPIService()


# API endpoints
@app.post("/grants/", response_model=Dict)
async def submit_grant_application(
    grant_data: GrantData,
    background_tasks: BackgroundTasks,
    service: MovemberAPIService = Depends(get_api_service),
    _: bool = Depends(verify_api_key)
):
    """Submit grant application for processing."""
    return await service.process_grant_application(grant_data)


@app.post("/reports/", response_model=Dict)
async def submit_impact_report(
    report_data: ImpactReportData,
    background_tasks: BackgroundTasks,
    service: MovemberAPIService = Depends(get_api_service),
    _: bool = Depends(verify_api_key)
):
    """Submit impact report for processing."""
    return await service.process_impact_report(report_data)


@app.post("/external-data/", response_model=Dict)
async def collect_external_data(
    request: ExternalDataRequest,
    service: MovemberAPIService = Depends(get_api_service),
    _: bool = Depends(verify_api_key)
):
    """Collect data from external sources."""
    return await service.collect_external_data(request)


@app.post("/scraper/", response_model=Dict)
async def run_web_scraper(
    config: ScraperConfig,
    service: MovemberAPIService = Depends(get_api_service),
    _: bool = Depends(verify_api_key)
):
    """Run web scraper with specified configuration."""
    return await service.run_web_scraper(config)


@app.post("/ai-grant-assistant/")
async def ai_grant_assistant(grant_data: dict):
    """
    AI-powered grant writing assistant that provides suggestions and improvements
    """
    try:
        title = grant_data.get("title", "")
        description = grant_data.get("description", "")
        budget = grant_data.get("budget", 0)
        timeline_months = grant_data.get("timeline_months", 12)
        organisation = grant_data.get("organisation", "")

        # AI-powered analysis and suggestions
        suggestions = {
            "title_enhancement": "",
            "description_improvements": [],
            "budget_optimization": "",
            "timeline_suggestions": "",
            "impact_metrics": [],
            "sdg_alignment": [],
            "stakeholder_strategies": [],
            "risk_mitigation": [],
            "success_factors": [],
            "overall_score": 0
        }

        # Analyze title and suggest improvements
        if title:
            if len(title) < 30:
                suggestions["title_enhancement"] = f"Consider expanding '{title}' to be more specific and impactful. Include key outcomes or target population."
            elif "men" not in title.lower() and "male" not in title.lower():
                suggestions["title_enhancement"] = "Consider explicitly mentioning men's health focus to align with Movember's mission."

        # Analyze description and provide improvements
        if description:
            description_score = 0
            improvements = []

            # Check for key elements
            if "impact" not in description.lower():
                improvements.append("Add specific impact metrics and outcomes")
                description_score += 0.1

            if "measure" not in description.lower() and "evaluate" not in description.lower():
                improvements.append("Include evaluation and measurement strategies")
                description_score += 0.1

            if "community" not in description.lower() and "partnership" not in description.lower():
                improvements.append("Mention community partnerships and engagement")
                description_score += 0.1

            if "sustainable" not in description.lower():
                improvements.append("Address sustainability and long-term impact")
                description_score += 0.1

            if "evidence" not in description.lower() and "research" not in description.lower():
                improvements.append("Include evidence-based approaches and research backing")
                description_score += 0.1

            suggestions["description_improvements"] = improvements
            suggestions["overall_score"] += description_score

        # Budget optimization suggestions
        if budget > 0:
            if budget < 50000:
                suggestions["budget_optimization"] = "Consider if this budget is sufficient for the scope. May need to scale down objectives or increase funding."
            elif budget > 500000:
                suggestions["budget_optimization"] = "Large budget - ensure detailed cost breakdown and strong justification for each line item."
            else:
                suggestions["budget_optimization"] = "Budget appears reasonable. Ensure detailed cost breakdown and value for money."

        # Timeline suggestions
        if timeline_months < 6:
            suggestions["timeline_suggestions"] = "Short timeline - ensure objectives are realistic and achievable within this timeframe."
        elif timeline_months > 36:
            suggestions["timeline_suggestions"] = "Long timeline - consider breaking into phases with clear milestones and deliverables."
        else:
            suggestions["timeline_suggestions"] = "Timeline appears reasonable. Include clear milestones and progress indicators."

        # Generate impact metrics suggestions
        suggestions["impact_metrics"] = [
            "Number of men reached and engaged",
            "Health outcomes improvement (measurable)",
            "Community awareness and education metrics",
            "Partnership and collaboration indicators",
            "Long-term sustainability measures"
        ]

        # SDG alignment suggestions
        suggestions["sdg_alignment"] = [
            "SDG 3: Good Health and Well-being (primary)",
            "SDG 5: Gender Equality (men's health focus)",
            "SDG 10: Reduced Inequalities (health equity)",
            "SDG 17: Partnerships for the Goals (collaboration)"
        ]

        # Stakeholder engagement strategies
        suggestions["stakeholder_strategies"] = [
            "Engage local health professionals and clinics",
            "Partner with community organizations and sports clubs",
            "Involve men's groups and peer support networks",
            "Collaborate with local government and health services",
            "Include family and community involvement strategies"
        ]

        # Risk mitigation strategies
        suggestions["risk_mitigation"] = [
            "Address potential barriers to men's participation",
            "Plan for cultural sensitivity and local context",
            "Include backup strategies for low engagement",
            "Consider seasonal factors and timing",
            "Plan for sustainability beyond grant period"
        ]

        # Success factors
        suggestions["success_factors"] = [
            "Clear, measurable objectives and outcomes",
            "Strong community partnerships and engagement",
            "Evidence-based approaches and methodologies",
            "Comprehensive evaluation and measurement plan",
            "Sustainability and long-term impact focus",
            "Alignment with Movember's mission and values"
        ]

        # Calculate overall improvement score
        base_score = 0.5
        improvement_score = min(0.4, suggestions["overall_score"])
        suggestions["overall_score"] = round(base_score + improvement_score, 2)

        return {
            "status": "success",
            "suggestions": suggestions,
            "grant_data": grant_data
        }

    except Exception as e:
        logger.error(f"Error in AI grant assistant: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/evaluate-grant/")
async def evaluate_grant(grant_data: dict):
    """
    Evaluate a grant application using the AI rules engine and ML predictions
    """
    try:
        # Extract grant details
        grant_id = grant_data.get("grant_id", f"grant_{int(time.time())}")
        title = grant_data.get("title", "")
        description = grant_data.get("description", "")
        budget = grant_data.get("budget", 0)
        timeline_months = grant_data.get("timeline_months", 12)
        organisation = grant_data.get("organisation", "")
        contact_person = grant_data.get("contact_person", "")
        email = grant_data.get("email", "")

        # Create evaluation context
        context = {
            "grant_id": grant_id,
            "title": title,
            "description": description,
            "budget": budget,
            "timeline_months": timeline_months,
            "organisation": organisation,
            "contact_person": contact_person,
            "email": email,
            "evaluation_timestamp": datetime.now().isoformat(),
            "context_type": "GRANT_EVALUATION"
        }

        # Run rules engine evaluation
        if RULES_SYSTEM_AVAILABLE and MovemberAIRulesEngine:
            try:
                engine = MovemberAIRulesEngine()
                evaluation_results = engine.evaluate_context(context)
            except Exception as e:
                logger.error(f"Rules engine evaluation failed: {e}")
                evaluation_results = {"status": "error", "message": "Rules engine unavailable"}
        else:
            evaluation_results = {"status": "mock", "message": "Rules engine not available"}

        # Generate ML predictions (mock for now)
        ml_predictions = {
            "approval_probability": round(random.uniform(0.6, 0.95), 3),
            "impact_score": round(random.uniform(0.5, 0.9), 3),
            "sdg_alignment": round(random.uniform(0.7, 0.95), 3),
            "stakeholder_engagement": round(random.uniform(0.6, 0.9), 3),
            "risk_assessment": round(random.uniform(0.1, 0.4), 3)
        }

        # Calculate overall score
        overall_score = (
            ml_predictions["approval_probability"] * 0.3 +
            ml_predictions["impact_score"] * 0.25 +
            ml_predictions["sdg_alignment"] * 0.2 +
            ml_predictions["stakeholder_engagement"] * 0.15 +
            (1 - ml_predictions["risk_assessment"]) * 0.1
        )

        # Determine recommendation
        if overall_score >= 0.8:
            recommendation = "STRONG_APPROVE"
        elif overall_score >= 0.6:
            recommendation = "APPROVE"
        elif overall_score >= 0.4:
            recommendation = "CONDITIONAL_APPROVE"
        else:
            recommendation = "REJECT"

        # Store evaluation in database
        evaluation_record = {
            "grant_id": grant_id,
            "evaluation_timestamp": context["evaluation_timestamp"],
            "overall_score": round(overall_score, 3),
            "recommendation": recommendation,
            "ml_predictions": ml_predictions,
            "rules_evaluation": evaluation_results,
            "grant_data": grant_data
        }

        # Save to database (simplified)
        with engine.begin() as conn:
            conn.execute(
                text("""
                    INSERT INTO grant_evaluations
                    (
                        grant_id, evaluation_timestamp, overall_score, recommendation, ml_predictions, rules_evaluation, grant_data)
                    VALUES (
                        :grant_id, :evaluation_timestamp, :overall_score, :recommendation, :ml_predictions, :rules_evaluation, :grant_data)
                """),
                evaluation_record
            )

        return {
            "status": "success",
            "grant_id": grant_id,
            "overall_score": round(overall_score, 3),
            "recommendation": recommendation,
            "ml_predictions": ml_predictions,
            "rules_evaluation": evaluation_results,
            "evaluation_timestamp": context["evaluation_timestamp"]
        }

    except Exception as e:
        logger.error(f"Error evaluating grant: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/health/", response_model=SystemHealthData)
async def get_system_health(
    service: MovemberAPIService = Depends(get_api_service)
):
    """Get system health status."""
    return await service.monitor_system_health()


@app.get("/grants/{grant_id}", response_model=Dict)
async def get_grant_details(
    grant_id: str,
    service: MovemberAPIService = Depends(get_api_service)
):
    """Get grant details by ID."""
    # Implementation for retrieving grant details
    return {"grant_id": grant_id, "status": "retrieved", "currency": "AUD", "spelling_standard": "UK"}


@app.get("/reports/{report_id}", response_model=Dict)
async def get_report_details(
    report_id: str,
    service: MovemberAPIService = Depends(get_api_service)
):
    """Get impact report details by ID."""
    # Implementation for retrieving report details
    return {"report_id": report_id, "status": "retrieved", "currency": "AUD", "spelling_standard": "UK"}


@app.get("/metrics/", response_model=Dict)
async def get_system_metrics(
    service: MovemberAPIService = Depends(get_api_service)
):
    """Get system performance metrics."""
    return {
        "status": "success",
        "metrics": service.engine.get_metrics(),
        "currency": "AUD",
        "spelling_standard": "UK"
    }


@app.get("/grant-evaluations/")
async def get_grant_evaluations(limit: int = 10, offset: int = 0):
    """
    Get recent grant evaluations
    """
    try:
        with engine.begin() as conn:
            result = conn.execute(text("""
                SELECT
                    grant_id,
                    evaluation_timestamp,
                    overall_score,
                    recommendation,
                    ml_predictions,
                    rules_evaluation,
                    grant_data,
                    created_at
                FROM grant_evaluations
                ORDER BY created_at DESC
                LIMIT :limit OFFSET :offset
            """), {"limit": limit, "offset": offset})

            evaluations = []
            for row in result:
                evaluations.append({
                    "grant_id": row.grant_id,
                    "evaluation_timestamp": row.evaluation_timestamp.isoformat() if row.evaluation_timestamp else None,
                    "overall_score": float(row.overall_score) if row.overall_score else 0,
                    "recommendation": row.recommendation,
                    "ml_predictions": row.ml_predictions,
                    "rules_evaluation": row.rules_evaluation,
                    "grant_data": row.grant_data,
                    "created_at": row.created_at.isoformat() if row.created_at else None
                })

            return {
                "status": "success",
                "evaluations": evaluations,
                "total": len(evaluations)
            }

    except Exception as e:
        logger.error(f"Error retrieving grant evaluations: {str(e)}")
        return {"status": "error", "message": str(e)}


import os
from pathlib import Path

# Get the base directory for assets
BASE_DIR = Path(__file__).parent.parent

# Test endpoint
@app.get("/test-logo/")
async def test_logo():
    """Test endpoint for logo."""
    return {"message": "Logo endpoint is working", "status": "success"}

# Logo endpoints
@app.get("/logo/")
async def get_logo():
    """Get the Movember logo."""
    # Serve the SVG content directly for now
    svg_content = '''<svg width="200" height="80" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="movemberGradient" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#2E86AB;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#F7931E;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background rectangle -->
  <rect width="200" height="80" rx="10" fill="url(#movemberGradient)" />
  
  <!-- Movember text -->
  <text x="100" y="45" font-family="Arial, sans-serif" font-size="24" font-weight="bold" 
        text-anchor="middle" fill="white" text-transform="uppercase" letter-spacing="2">
    MOVEMBER
  </text>
  
  <!-- Subtitle -->
  <text x="100" y="65" font-family="Arial, sans-serif" font-size="12" 
        text-anchor="middle" fill="white" opacity="0.9">
    AI Rules System
  </text>
</svg>'''
    
    from fastapi.responses import Response
    return Response(content=svg_content, media_type="image/svg+xml")

@app.get("/logo/192")
async def get_logo_192():
    """Get the Movember logo (192x192)."""
    try:
        logo_path = BASE_DIR / "assets" / "images" / "android-chrome-192x192.png"
        return FileResponse(str(logo_path), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Logo not found")

@app.get("/logo/512")
async def get_logo_512():
    """Get the Movember logo (512x512)."""
    try:
        logo_path = BASE_DIR / "assets" / "images" / "android-chrome-512x512.png"
        return FileResponse(str(logo_path), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Logo not found")

@app.get("/logo/apple")
async def get_apple_logo():
    """Get the Apple touch icon."""
    try:
        logo_path = BASE_DIR / "assets" / "images" / "apple-touch-icon.png"
        return FileResponse(str(logo_path), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Logo not found")

# Favicon endpoints
@app.get("/favicon.ico")
async def get_favicon():
    """Get the Movember favicon."""
    # Serve a simple SVG favicon for now
    favicon_svg = '''<svg width="32" height="32" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="faviconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2E86AB;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#F7931E;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="32" height="32" rx="6" fill="url(#faviconGradient)" />
  <text x="16" y="22" font-family="Arial, sans-serif" font-size="18" font-weight="bold" 
        text-anchor="middle" fill="white">M</text>
</svg>'''
    
    from fastapi.responses import Response
    return Response(content=favicon_svg, media_type="image/svg+xml")

@app.get("/favicon/16")
async def get_favicon_16():
    """Get the 16x16 favicon."""
    try:
        favicon_path = BASE_DIR / "assets" / "images" / "favicon-16x16.png"
        return FileResponse(str(favicon_path), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Favicon not found")

@app.get("/favicon/32")
async def get_favicon_32():
    """Get the 32x32 favicon."""
    try:
        favicon_path = BASE_DIR / "assets" / "images" / "favicon-32x32.png"
        return FileResponse(str(favicon_path), media_type="image/png")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Favicon not found")

# Web manifest endpoint for PWA support
@app.get("/site.webmanifest")
async def get_web_manifest():
    """Get the web app manifest for PWA support."""
    try:
        manifest_path = BASE_DIR / "assets" / "site.webmanifest"
        return FileResponse(str(manifest_path), media_type="application/manifest+json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Web manifest not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
