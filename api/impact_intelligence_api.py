#!/usr/bin/env python3
"""
Impact Intelligence API for Movember
Provides endpoints for impact measurement, reporting, and analysis.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from impact_intelligence_engine import (
    impact_intelligence_engine,
    ImpactCategory,
    ImpactMetric
)

logger = logging.getLogger(__name__)

# Create router for impact intelligence endpoints
impact_intelligence_router = APIRouter(prefix="/impact-intelligence", tags=["Impact Intelligence"])

# Pydantic models for request/response
class ImpactMeasurementRequest(BaseModel):


    project_id: str = Field(..., description="Project ID to measure impact for")
    include_visualisations: bool = Field(default=True, description="Include visualisation data")

class ImpactReportRequest(BaseModel):


    report_type: str = Field(default="comprehensive", description="Type of impact report")
    time_period: str = Field(default="annual", description="Time period for report")
    include_sdg_alignment: bool = Field(default=True, description="Include SDG alignment analysis")

class SROICalculationRequest(BaseModel):


    project_id: str = Field(..., description="Project ID for SROI calculation")
    include_breakdown: bool = Field(default=True, description="Include detailed breakdown")

class ImpactVisualisationRequest(BaseModel):


    visualisation_type: str = Field(..., description="Type of visualisation")
    filters: Optional[Dict[str, Any]] = Field(default=None, description="Filters for data")

class ImpactMeasurementResponse(BaseModel):


    status: str
    project_impact: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class ImpactReportResponse(BaseModel):


    status: str
    impact_report: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class SROICalculationResponse(BaseModel):


    status: str
    sroi_result: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class ImpactVisualisationResponse(BaseModel):


    status: str
    visualisation_data: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

# Project Impact Measurement Endpoint
@impact_intelligence_router.post("/measure-project-impact/", response_model=ImpactMeasurementResponse)
async def measure_project_impact(request: ImpactMeasurementRequest):
    """
    Measure comprehensive impact for a specific project.

    This endpoint provides detailed impact measurements including:
    - Men reached
    - Awareness increase
    - Health outcomes
    - Research impact
    - Funding impact
    """

    logger.info(f"Project impact measurement request for project: {request.project_id}")

    try:
        # Call the impact intelligence engine
        project_impact = await impact_intelligence_engine.measure_project_impact(
            request.project_id
        )

        if "error" in project_impact:
            raise HTTPException(
                status_code=404,
                detail=project_impact["error"]
            )

        return ImpactMeasurementResponse(
            status="success",
            project_impact=project_impact
        )

    except Exception as e:
        logger.error(f"Project impact measurement failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Project impact measurement failed: {str(e)}"
        )

# Comprehensive Impact Report Endpoint
@impact_intelligence_router.post("/generate-impact-report/", response_model=ImpactReportResponse)
async def generate_impact_report(request: ImpactReportRequest):
    """
    Generate comprehensive impact report for Movember.

    This endpoint provides:
    - Executive summary with key metrics
    - Impact by category (awareness, health outcomes, research, funding)
    - SDG alignment analysis
    - Strategic recommendations
    """

    logger.info(f"Impact report generation request: {request.report_type}")

    try:
        # Call the impact intelligence engine
        impact_report = await impact_intelligence_engine.generate_impact_report(
            report_type=request.report_type,
            time_period=request.time_period
        )

        return ImpactReportResponse(
            status="success",
            impact_report=impact_report
        )

    except Exception as e:
        logger.error(f"Impact report generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impact report generation failed: {str(e)}"
        )

# SROI Calculation Endpoint
@impact_intelligence_router.post("/calculate-sroi/", response_model=SROICalculationResponse)
async def calculate_sroi(request: SROICalculationRequest):
    """
    Calculate Social Return on Investment (SROI) for a project.

    This endpoint provides:
    - Investment amount
    - Social value created
    - SROI ratio
    - Detailed breakdown
    """

    logger.info(f"SROI calculation request for project: {request.project_id}")

    try:
        # Call the impact intelligence engine
        sroi_result = await impact_intelligence_engine.calculate_social_return_on_investment(
            request.project_id
        )

        if "error" in sroi_result:
            raise HTTPException(
                status_code=404,
                detail=sroi_result["error"]
            )

        return SROICalculationResponse(
            status="success",
            sroi_result=sroi_result
        )

    except Exception as e:
        logger.error(f"SROI calculation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"SROI calculation failed: {str(e)}"
        )

# Impact Visualisation Data Endpoint
@impact_intelligence_router.post("/visualisation-data/", response_model=ImpactVisualisationResponse)
async def get_visualisation_data(request: ImpactVisualisationRequest):
    """
    Get data for impact visualisations.

    This endpoint provides:
    - Global reach data
    - Health outcomes data
    - Research impact data
    - Funding impact data
    """

    logger.info(f"Visualisation data request: {request.visualisation_type}")

    try:
        # Call the impact intelligence engine
        visualisation_data = await impact_intelligence_engine.generate_impact_visualisation_data()

        return ImpactVisualisationResponse(
            status="success",
            visualisation_data=visualisation_data
        )

    except Exception as e:
        logger.error(f"Visualisation data generation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Visualisation data generation failed: {str(e)}"
        )

# Projects List Endpoint
@impact_intelligence_router.get("/projects/")
async def get_impact_projects():
    """
    Get all Movember impact projects.

    Returns comprehensive list of impact projects with:
    - Project details
    - Budget information
    - Geographic scope
    - Target audience
    - SDG alignment
    """

    logger.info("Impact projects request")

    try:
        projects = []

        for project in impact_intelligence_engine.projects:
            projects.append({
                "project_id": project.project_id,
                "title": project.title,
                "description": project.description,
                "start_date": project.start_date.isoformat(),
                "end_date": project.end_date.isoformat() if project.end_date else None,
                "budget": project.budget,
                "currency": project.currency,
                "geographic_scope": project.geographic_scope,
                "target_audience": project.target_audience,
                "sdg_alignment": project.sdg_alignment,
                "stakeholders": project.stakeholders,
                "status": project.status
            })

        return {
            "status": "success",
            "projects": projects,
            "total_projects": len(projects),
            "total_budget": sum(p["budget"] for p in projects),
            "currency": "AUD",
            "spelling_standard": "UK"
        }

    except Exception as e:
        logger.error(f"Impact projects retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impact projects retrieval failed: {str(e)}"
        )

# Impact Metrics Endpoint
@impact_intelligence_router.get("/metrics/")
async def get_impact_metrics():
    """
    Get all available impact metrics.

    Returns:
    - List of impact metrics
    - Metric categories
    - Measurement units
    """

    logger.info("Impact metrics request")

    try:
        metrics = [
            {
                "metric": metric.value,
                "name": metric.name.replace("_", " ").title(),
                "category": "quantitative",
                "unit": "varies",
                "description": f"Measurement of {metric.value.replace('_', ' ')}"
            }
            for metric in ImpactMetric
        ]

        categories = [
            {
                "category": category.value,
                "name": category.name.replace("_", " ").title(),
                "description": f"Impact category for {category.value}"
            }
            for category in ImpactCategory
        ]

        return {
            "status": "success",
            "metrics": metrics,
            "categories": categories,
            "total_metrics": len(metrics),
            "total_categories": len(categories),
            "currency": "AUD",
            "spelling_standard": "UK"
        }

    except Exception as e:
        logger.error(f"Impact metrics retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impact metrics retrieval failed: {str(e)}"
        )

# SDG Alignment Endpoint
@impact_intelligence_router.get("/sdg-alignment/")
async def get_sdg_alignment():
    """
    Get SDG alignment analysis for Movember's impact.

    Returns:
    - SDG contributions
    - Target alignment
    - Impact scores
    """

    logger.info("SDG alignment request")

    try:
        sdg_data = impact_intelligence_engine.sdg_framework

        return {
            "status": "success",
            "sdg_alignment": sdg_data,
            "total_sdgs": len(sdg_data),
            "average_impact_score": sum(
                sdg.get("impact_score", 0) for sdg in sdg_data.values()
            ) / len(sdg_data) if sdg_data else 0,
            "currency": "AUD",
            "spelling_standard": "UK"
        }

    except Exception as e:
        logger.error(f"SDG alignment retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"SDG alignment retrieval failed: {str(e)}"
        )

# Impact Summary Endpoint
@impact_intelligence_router.get("/summary/")
async def get_impact_summary():
    """
    Get high-level impact summary for Movember.

    Returns:
    - Key impact metrics
    - Global reach
    - Health outcomes
    - Research impact
    """

    logger.info("Impact summary request")

    try:
        impact_data = impact_intelligence_engine.impact_data

        summary = {
            "global_reach": {
                "men_reached": impact_data["global_reach"]["men_reached"],
                "countries_reached": impact_data["global_reach"]["countries_reached"],
                "awareness_increase": impact_data["global_reach"]["awareness_increase"],
                "engagement_rate": impact_data["global_reach"]["engagement_rate"]
            },
            "health_outcomes": {
                "screenings_conducted": impact_data["health_outcomes"]["screenings_conducted"],
                "lives_saved": impact_data["health_outcomes"]["lives_saved"],
                "early_detections": impact_data["health_outcomes"]["early_detections"],
                "treatment_initiations": impact_data["health_outcomes"]["treatment_initiations"]
            },
            "research_impact": {
                "research_publications": impact_data["research_impact"]["research_publications"],
                "clinical_trials": impact_data["research_impact"]["clinical_trials"],
                "policy_influence": impact_data["research_impact"]["policy_influence"],
                "partnerships_formed": impact_data["research_impact"]["partnerships_formed"]
            },
            "funding_impact": {
                "total_funding_raised": impact_data["funding_impact"]["total_funding_raised"],
                "funding_invested": impact_data["funding_impact"]["funding_invested"],
                "return_on_investment": impact_data["funding_impact"]["return_on_investment"],
                "sustainability_score": impact_data["funding_impact"]["sustainability_score"]
            }
        }

        return {
            "status": "success",
            "impact_summary": summary,
            "currency": "AUD",
            "spelling_standard": "UK"
        }

    except Exception as e:
        logger.error(f"Impact summary retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Impact summary retrieval failed: {str(e)}"
        )

# Health Check for Impact Intelligence
@impact_intelligence_router.get("/health/")
async def impact_intelligence_health():
    """
    Health check for the impact intelligence system.
    """

    return {
        "status": "healthy",
        "service": "impact_intelligence",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "project_impact_measurement",
            "comprehensive_reporting",
            "sroi_calculation",
            "visualisation_data",
            "sdg_alignment"
        ],
        "currency": "AUD",
        "spelling_standard": "UK"
    }

# Export the router for inclusion in main API
__all__ = ["impact_intelligence_router"]
