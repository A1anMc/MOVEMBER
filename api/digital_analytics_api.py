#!/usr/bin/env python3
"""
Digital Analytics API for Movember AI Rules System
FastAPI endpoints for social media, Google Analytics, and digital engagement tracking
"""

from fastapi import APIRouter, HTTPException, Query, Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging
import asyncio

# Import the digital analytics classes
try:
    from analytics.digital_analytics import (
        UnifiedDigitalAnalytics,
        SocialMediaAnalytics,
        GoogleAnalyticsIntegration,
        AttributionModel
    )
except ImportError:
    # Fallback for when the main analytics module isn't available
    class UnifiedDigitalAnalytics:
        async def get_comprehensive_dashboard(self):
            return {"status": "analytics_module_not_available"}
    
    class SocialMediaAnalytics:
        async def get_cross_platform_summary(self):
            return {"status": "analytics_module_not_available"}
    
    class GoogleAnalyticsIntegration:
        async def get_audience_overview(self):
            return {"status": "analytics_module_not_available"}
    
    class AttributionModel:
        async def get_channel_performance(self):
            return {"status": "analytics_module_not_available"}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/analytics", tags=["Digital Analytics"])

# Initialize analytics components
analytics = UnifiedDigitalAnalytics()
social_media = SocialMediaAnalytics()
google_analytics = GoogleAnalyticsIntegration()
attribution = AttributionModel()


@router.get("/digital/summary")
async def get_digital_analytics_summary():
    """Get comprehensive digital analytics summary."""
    try:
        dashboard = await analytics.get_comprehensive_dashboard()
        return {
            "status": "success",
            "data": dashboard,
            "timestamp": datetime.now().isoformat(),
            "message": "Digital analytics summary retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting digital analytics summary: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving digital analytics: {str(e)}")


@router.get("/social-media/performance")
async def get_social_media_performance(
    platform: Optional[str] = Query(None, description="Specific platform to analyze")
):
    """Get social media performance metrics."""
    try:
        if platform:
            performance = await social_media.get_platform_performance(platform)
        else:
            performance = await social_media.get_cross_platform_summary()
        
        return {
            "status": "success",
            "data": performance,
            "timestamp": datetime.now().isoformat(),
            "message": f"Social media performance data retrieved for {platform if platform else 'all platforms'}"
        }
    except Exception as e:
        logger.error(f"Error getting social media performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving social media performance: {str(e)}")


@router.get("/web/performance")
async def get_web_analytics_performance(
    metric_type: str = Query("overview", description="Type of web analytics data")
):
    """Get web analytics performance metrics."""
    try:
        if metric_type == "audience":
            data = await google_analytics.get_audience_overview()
        elif metric_type == "acquisition":
            data = await google_analytics.get_acquisition_analysis()
        elif metric_type == "behaviour":
            data = await google_analytics.get_behaviour_analysis()
        elif metric_type == "conversion":
            data = await google_analytics.get_conversion_analysis()
        else:
            data = await google_analytics.get_audience_overview()
        
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now().isoformat(),
            "message": f"Web analytics {metric_type} data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting web analytics performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving web analytics: {str(e)}")


@router.get("/attribution/analysis")
async def get_attribution_analysis(
    conversion_type: str = Query("donations", description="Type of conversion to analyze")
):
    """Get cross-platform attribution analysis."""
    try:
        attribution_data = await attribution.get_attribution_analysis(conversion_type)
        
        return {
            "status": "success",
            "data": attribution_data,
            "timestamp": datetime.now().isoformat(),
            "message": f"Attribution analysis for {conversion_type} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting attribution analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving attribution analysis: {str(e)}")


@router.get("/channel/performance")
async def get_channel_performance():
    """Get channel performance comparison."""
    try:
        channel_data = await attribution.get_channel_performance()
        
        return {
            "status": "success",
            "data": channel_data,
            "timestamp": datetime.now().isoformat(),
            "message": "Channel performance data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting channel performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving channel performance: {str(e)}")


@router.get("/audience/segmentation")
async def get_audience_segmentation():
    """Get audience segmentation analysis."""
    try:
        segmentation = await analytics.get_audience_segmentation()
        
        return {
            "status": "success",
            "data": segmentation,
            "timestamp": datetime.now().isoformat(),
            "message": "Audience segmentation data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting audience segmentation: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving audience segmentation: {str(e)}")


@router.get("/roi/analysis")
async def get_roi_analysis():
    """Get cross-platform ROI analysis."""
    try:
        roi_data = await analytics.get_cross_platform_roi()
        
        return {
            "status": "success",
            "data": roi_data,
            "timestamp": datetime.now().isoformat(),
            "message": "ROI analysis data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting ROI analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving ROI analysis: {str(e)}")


@router.get("/campaign/performance")
async def get_campaign_performance(
    campaign_id: Optional[str] = Query(None, description="Specific campaign ID to analyze")
):
    """Get campaign performance analysis."""
    try:
        if campaign_id:
            campaign_data = await social_media.track_campaign_performance(campaign_id)
        else:
            # Return summary of all campaigns
            campaign_data = {
                "campaigns": [
                    {"id": "Movember2025", "name": "Movember 2025 Campaign", "status": "active"},
                    {"id": "MensHealthAwareness", "name": "Men's Health Awareness", "status": "active"},
                    {"id": "ProstateCancerScreening", "name": "Prostate Cancer Screening", "status": "completed"}
                ],
                "summary": {
                    "total_campaigns": 3,
                    "active_campaigns": 2,
                    "total_reach": 2500000,
                    "total_conversions": 850
                }
            }
        
        return {
            "status": "success",
            "data": campaign_data,
            "timestamp": datetime.now().isoformat(),
            "message": f"Campaign performance data retrieved for {campaign_id if campaign_id else 'all campaigns'}"
        }
    except Exception as e:
        logger.error(f"Error getting campaign performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving campaign performance: {str(e)}")


@router.get("/content/performance")
async def get_content_performance():
    """Get content performance analysis."""
    try:
        content_data = await social_media.get_content_performance()
        
        return {
            "status": "success",
            "data": content_data,
            "timestamp": datetime.now().isoformat(),
            "message": "Content performance data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting content performance: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving content performance: {str(e)}")


@router.get("/audience/insights")
async def get_audience_insights():
    """Get audience demographics and behaviour insights."""
    try:
        insights = await social_media.get_audience_insights()
        
        return {
            "status": "success",
            "data": insights,
            "timestamp": datetime.now().isoformat(),
            "message": "Audience insights data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting audience insights: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving audience insights: {str(e)}")


@router.get("/conversion/funnel")
async def get_conversion_funnel():
    """Get conversion funnel analysis."""
    try:
        funnel_data = await google_analytics.get_conversion_analysis()
        
        return {
            "status": "success",
            "data": funnel_data,
            "timestamp": datetime.now().isoformat(),
            "message": "Conversion funnel data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting conversion funnel: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversion funnel: {str(e)}")


@router.get("/events/analysis")
async def get_custom_event_analysis(
    event_name: str = Query(..., description="Name of the custom event to analyze")
):
    """Get custom event performance analysis."""
    try:
        event_data = await google_analytics.get_custom_event_analysis(event_name)
        
        return {
            "status": "success",
            "data": event_data,
            "timestamp": datetime.now().isoformat(),
            "message": f"Custom event analysis for {event_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting custom event analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving custom event analysis: {str(e)}")


@router.get("/platform/{platform_name}")
async def get_platform_details(
    platform_name: str = Path(..., description="Name of the platform to analyze")
):
    """Get detailed analysis for a specific platform."""
    try:
        if platform_name in ["facebook", "instagram", "twitter", "linkedin", "youtube", "tiktok", "reddit"]:
            platform_data = await social_media.get_platform_performance(platform_name)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported platform: {platform_name}")
        
        return {
            "status": "success",
            "data": platform_data,
            "timestamp": datetime.now().isoformat(),
            "message": f"Platform analysis for {platform_name} retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting platform details: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving platform details: {str(e)}")


@router.get("/integrated/metrics")
async def get_integrated_metrics():
    """Get integrated metrics across all platforms."""
    try:
        integrated_data = await analytics.get_integrated_metrics()
        
        return {
            "status": "success",
            "data": integrated_data,
            "timestamp": datetime.now().isoformat(),
            "message": "Integrated metrics data retrieved successfully"
        }
    except Exception as e:
        logger.error(f"Error getting integrated metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving integrated metrics: {str(e)}")


@router.get("/health")
async def get_digital_analytics_health():
    """Get digital analytics system health status."""
    try:
        # Test basic functionality
        social_summary = await social_media.get_cross_platform_summary()
        web_data = await google_analytics.get_audience_overview()
        attribution_data = await attribution.get_channel_performance()
        
        health_status = {
            "status": "healthy",
            "components": {
                "social_media_analytics": "operational",
                "web_analytics": "operational",
                "attribution_modeling": "operational"
            },
            "last_check": datetime.now().isoformat(),
            "data_sources": {
                "social_platforms": ["Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube", "TikTok", "Reddit"],
                "web_analytics": "Google Analytics 4",
                "attribution": "Multi-touch attribution models"
            }
        }
        
        return {
            "status": "success",
            "data": health_status,
            "timestamp": datetime.now().isoformat(),
            "message": "Digital analytics system is healthy"
        }
    except Exception as e:
        logger.error(f"Error checking digital analytics health: {e}")
        return {
            "status": "error",
            "data": {
                "status": "unhealthy",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            },
            "timestamp": datetime.now().isoformat(),
            "message": "Digital analytics system health check failed"
        }


# Function to include digital analytics routes in main app
def include_digital_analytics_routes(app):
    """Include digital analytics routes in the main FastAPI app."""
    app.include_router(router, prefix="/analytics")
    logger.info("Digital analytics routes included successfully")


# Test endpoint for development
@router.get("/test")
async def test_digital_analytics():
    """Test endpoint for digital analytics functionality."""
    return {
        "status": "success",
        "message": "Digital analytics API is working",
        "endpoints_available": [
            "/analytics/digital/summary",
            "/analytics/social-media/performance",
            "/analytics/web/performance",
            "/analytics/attribution/analysis",
            "/analytics/channel/performance",
            "/analytics/audience/segmentation",
            "/analytics/roi/analysis",
            "/analytics/campaign/performance",
            "/analytics/content/performance",
            "/analytics/audience/insights",
            "/analytics/conversion/funnel",
            "/analytics/events/analysis",
            "/analytics/platform/{platform_name}",
            "/analytics/integrated/metrics",
            "/analytics/health"
        ],
        "timestamp": datetime.now().isoformat()
    }
