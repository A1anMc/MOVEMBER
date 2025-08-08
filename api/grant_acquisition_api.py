#!/usr/bin/env python3
"""
Grant Acquisition API for Movember
Provides endpoints for grant discovery, application enhancement, and success tracking.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
import asyncio

from grant_acquisition_engine import (
    grant_acquisition_engine,
    GrantStatus,
    FundingBody
)

logger = logging.getLogger(__name__)

# Create router for grant acquisition endpoints
grant_acquisition_router = APIRouter(prefix="/grant-acquisition", tags=["Grant Acquisition"])

# Pydantic models for request/response
class GrantDiscoveryRequest(BaseModel):
    focus_areas: Optional[List[str]] = Field(
        default=None,
        description="Specific focus areas for grant discovery"
    )
    budget_range: Optional[Dict[str, float]] = Field(
        default=None,
        description="Budget range for grant opportunities"
    )
    timeline_range: Optional[Dict[str, int]] = Field(
        default=None,
        description="Timeline range in months"
    )

class GrantDiscoveryResponse(BaseModel):
    status: str
    discovery_results: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class ApplicationEnhancementRequest(BaseModel):
    grant_id: str = Field(..., description="ID of the grant opportunity")
    current_draft: Dict[str, Any] = Field(..., description="Current application draft")
    movember_strengths: Optional[List[str]] = Field(
        default=None,
        description="Movember's specific strengths to highlight"
    )

class ApplicationEnhancementResponse(BaseModel):
    status: str
    enhanced_application: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class SuccessTrackingRequest(BaseModel):
    grant_id: str = Field(..., description="ID of the grant")
    application_data: Dict[str, Any] = Field(..., description="Application data")
    status: str = Field(..., description="Current application status")

class SuccessTrackingResponse(BaseModel):
    status: str
    tracking_result: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

class SuccessStrategyRequest(BaseModel):
    grant_id: str = Field(..., description="ID of the grant opportunity")
    competitors: Optional[List[str]] = Field(
        default=None,
        description="Known competitors for this grant"
    )
    movember_advantages: Optional[List[str]] = Field(
        default=None,
        description="Movember's specific advantages"
    )

class SuccessStrategyResponse(BaseModel):
    status: str
    strategy: Dict[str, Any]
    currency: str = "AUD"
    spelling_standard: str = "UK"

# Grant Discovery Endpoint
@grant_acquisition_router.post("/discover-grants/", response_model=GrantDiscoveryResponse)
async def discover_grants(request: GrantDiscoveryRequest):
    """
    Discover grant opportunities that match Movember's profile.
    
    This endpoint helps Movember find relevant grant opportunities based on:
    - Focus areas (men's health, mental health, etc.)
    - Budget requirements
    - Timeline needs
    - Geographic scope
    """
    
    logger.info(f"Grant discovery request: {request}")
    
    try:
        # Use default Movember profile if not specified
        focus_areas = request.focus_areas or [
            "men's mental health",
            "prostate cancer", 
            "testicular cancer",
            "suicide prevention",
            "physical health awareness"
        ]
        
        budget_range = request.budget_range or {"min": 50000, "max": 5000000}
        
        # Call the grant acquisition engine
        discovery_results = await grant_acquisition_engine.discover_grants(
            focus_areas=focus_areas,
            budget_range=budget_range
        )
        
        return GrantDiscoveryResponse(
            status="success",
            discovery_results=discovery_results
        )
        
    except Exception as e:
        logger.error(f"Grant discovery failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Grant discovery failed: {str(e)}"
        )

# Application Enhancement Endpoint
@grant_acquisition_router.post("/enhance-application/", response_model=ApplicationEnhancementResponse)
async def enhance_application(request: ApplicationEnhancementRequest):
    """
    Enhance a grant application for better success probability.
    
    This endpoint helps Movember improve grant applications by:
    - Highlighting Movember's unique strengths
    - Optimising budget allocation
    - Providing strategic recommendations
    - Suggesting risk mitigation strategies
    """
    
    logger.info(f"Application enhancement request for grant: {request.grant_id}")
    
    try:
        # Call the grant acquisition engine
        enhancement_results = await grant_acquisition_engine.enhance_application(
            request.grant_id,
            request.current_draft
        )
        
        return ApplicationEnhancementResponse(
            status="success",
            enhanced_application=enhancement_results
        )
        
    except Exception as e:
        logger.error(f"Application enhancement failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Application enhancement failed: {str(e)}"
        )

# Success Tracking Endpoint
@grant_acquisition_router.post("/track-success/", response_model=SuccessTrackingResponse)
async def track_success(request: SuccessTrackingRequest):
    """
    Track grant application success and provide analytics.
    
    This endpoint helps Movember:
    - Track application status
    - Monitor success rates
    - Analyse funding obtained
    - Generate improvement recommendations
    """
    
    logger.info(f"Success tracking request for grant: {request.grant_id}")
    
    try:
        # Convert status string to enum
        status_enum = GrantStatus(request.status)
        
        # Call the grant acquisition engine
        tracking_results = await grant_acquisition_engine.track_success(
            request.grant_id,
            request.application_data,
            status_enum
        )
        
        return SuccessTrackingResponse(
            status="success",
            tracking_result=tracking_results
        )
        
    except Exception as e:
        logger.error(f"Success tracking failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Success tracking failed: {str(e)}"
        )

# Success Analytics Endpoint
@grant_acquisition_router.get("/success-analytics/")
async def get_success_analytics():
    """
    Get comprehensive success analytics for Movember's grant applications.
    
    Returns:
    - Overall success rates
    - Total funding obtained
    - Average grant size
    - Success trends over time
    - Strategic recommendations
    """
    
    logger.info("Success analytics request")
    
    try:
        # Call the grant acquisition engine
        analytics_results = await grant_acquisition_engine.get_success_analytics()
        
        return {
            "status": "success",
            "analytics": analytics_results,
            "currency": "AUD",
            "spelling_standard": "UK"
        }
        
    except Exception as e:
        logger.error(f"Success analytics failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Success analytics failed: {str(e)}"
        )

# Success Strategy Endpoint
@grant_acquisition_router.post("/success-strategy/", response_model=SuccessStrategyResponse)
async def develop_success_strategy(request: SuccessStrategyRequest):
    """
    Develop a winning strategy for a specific grant opportunity.
    
    This endpoint helps Movember:
    - Analyse competitive positioning
    - Identify unique advantages
    - Develop strategic partnerships
    - Plan risk mitigation
    """
    
    logger.info(f"Success strategy request for grant: {request.grant_id}")
    
    try:
        # Find the grant opportunity
        grant_opportunity = next(
            (g for g in grant_acquisition_engine.discovery_engine.grant_database 
             if g.id == request.grant_id),
            None
        )
        
        if not grant_opportunity:
            raise HTTPException(
                status_code=404,
                detail=f"Grant opportunity {request.grant_id} not found"
            )
        
        # Generate success strategy
        strategy = {
            "grant_id": request.grant_id,
            "grant_title": grant_opportunity.title,
            "funding_body": grant_opportunity.funding_body.value,
            "amount": grant_opportunity.amount,
            "deadline": grant_opportunity.deadline.isoformat(),
            "competitive_advantage": [
                "Movember's global network and proven track record",
                "Strong research partnerships and academic collaborations",
                "Innovative and evidence-based approach",
                "Clear methodology and measurable outcomes"
            ],
            "partnerships": [
                "University of Sydney research partnership",
                "Mental Health Foundation collaboration",
                "Global men's health network engagement",
                "Government and NGO partnerships"
            ],
            "risk_mitigation": [
                "Phased implementation approach with clear milestones",
                "Regular stakeholder communication and progress updates",
                "Flexible methodology to adapt to changing circumstances",
                "Strong governance and oversight structures"
            ],
            "success_metrics": [
                "Direct engagement with target audience",
                "Measurable improvements in health awareness",
                "Sustainable long-term health outcomes",
                "Policy influence and systemic change"
            ],
            "recommendations": [
                "Emphasise Movember's unique global reach",
                "Highlight evidence-based approach and measurable outcomes",
                "Include strong research partnerships and collaborations",
                "Demonstrate clear methodology and implementation plan",
                "Show commitment to long-term impact and sustainability"
            ]
        }
        
        return SuccessStrategyResponse(
            status="success",
            strategy=strategy
        )
        
    except Exception as e:
        logger.error(f"Success strategy development failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Success strategy development failed: {str(e)}"
        )

# Grant Opportunities List Endpoint
@grant_acquisition_router.get("/grant-opportunities/")
async def get_grant_opportunities():
    """
    Get all available grant opportunities for Movember.
    
    Returns a comprehensive list of grant opportunities with:
    - Match scores
    - Success probabilities
    - Funding amounts
    - Deadlines
    - Requirements
    """
    
    logger.info("Grant opportunities request")
    
    try:
        opportunities = []
        
        for grant in grant_acquisition_engine.discovery_engine.grant_database:
            opportunities.append({
                "id": grant.id,
                "title": grant.title,
                "funding_body": grant.funding_body.value,
                "amount": grant.amount,
                "currency": grant.currency,
                "deadline": grant.deadline.isoformat(),
                "focus_areas": grant.focus_areas,
                "geographic_scope": grant.geographic_scope,
                "match_score": grant.match_score,
                "success_probability": grant.success_probability,
                "status": grant.status.value,
                "description": grant.description,
                "requirements": grant.requirements or []
            })
        
        # Sort by match score and success probability
        opportunities.sort(key=lambda x: (x["match_score"], x["success_probability"]), reverse=True)
        
        return {
            "status": "success",
            "opportunities": opportunities,
            "total_opportunities": len(opportunities),
            "total_potential_funding": sum(g["amount"] for g in opportunities),
            "average_success_probability": sum(g["success_probability"] for g in opportunities) / len(opportunities) if opportunities else 0,
            "currency": "AUD",
            "spelling_standard": "UK"
        }
        
    except Exception as e:
        logger.error(f"Grant opportunities retrieval failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Grant opportunities retrieval failed: {str(e)}"
        )

# Application Status Update Endpoint
@grant_acquisition_router.put("/application-status/{grant_id}")
async def update_application_status(
    grant_id: str,
    status: str,
    application_data: Dict[str, Any]
):
    """
    Update the status of a grant application.
    
    Status options:
    - discovered: Grant opportunity found
    - draft: Application in progress
    - submitted: Application submitted
    - approved: Grant approved
    - rejected: Grant rejected
    """
    
    logger.info(f"Application status update for grant: {grant_id} -> {status}")
    
    try:
        # Validate status
        valid_statuses = [s.value for s in GrantStatus]
        if status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Must be one of: {valid_statuses}"
            )
        
        # Track the status update
        tracking_results = await grant_acquisition_engine.track_success(
            grant_id,
            application_data,
            GrantStatus(status)
        )
        
        return {
            "status": "success",
            "grant_id": grant_id,
            "new_status": status,
            "tracking_result": tracking_results,
            "currency": "AUD",
            "spelling_standard": "UK"
        }
        
    except Exception as e:
        logger.error(f"Application status update failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Application status update failed: {str(e)}"
        )

# Health Check for Grant Acquisition
@grant_acquisition_router.get("/health/")
async def grant_acquisition_health():
    """
    Health check for the grant acquisition system.
    """
    
    return {
        "status": "healthy",
        "service": "grant_acquisition",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "grant_discovery",
            "application_enhancement", 
            "success_tracking",
            "success_analytics",
            "success_strategy"
        ],
        "currency": "AUD",
        "spelling_standard": "UK"
    }

# Export the router for inclusion in main API
__all__ = ["grant_acquisition_router"] 